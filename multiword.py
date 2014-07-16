import re
import group
import freegroup
import whiteheadgraph.split.split as split
import old_python.gengraphs as gengraphs
import old_python.heegaard as heegaard
import old_python.subgroup as subgroup
import whiteheadgraph.build.wgraph as wg

# F=freegroup.FGFreeGroup(numgens=3)
# wordlist1=[F.word('aabbccacb')]
# wordlist2=[F.word([1]), F.word([2]), F.word([3]), F.word([1,3,-2,1,-3,2])]
# isVirtuallyGeometric(F,wordlist1)=False
# isVirtuallyGeometric(F,wordlist2)=True


def isVirtuallyGeometric(F,wordlist, Heegaardwaittime=10, tellmeifitsrigid=False,cutpairsearchrecursionlimit=None, maxnumberof2componentcutstoconsider=None):
    """
    Decides if a multiword is virtually geometric.
    F is a free group. wordlist is a list of words in F.
    """
    maybevirtuallygeometric=True
    rigid=True

    wgp=wg.wgparse(F,wordlist,simplifyandminimize=True)
    W=wgp['WhiteheadGraph']
    wordlist=wgp['wordlist']
    wordmap=wgp['wordmap']
    # first check if F splits freely rel wordlist
    freesplitting,wmap=F.getFreeSplittingRel(wordlist, withwordmap=True, minimized=True, simplified=True)
    if freesplitting.edges(): # if splits freely then is not rigid
        rigid=False
    wheredidmywordsgo=[(wmap[wordmap[i][0]][0], wmap[wordmap[i][0]][1],wmap[wordmap[i][0]][2]*wordmap[i][1]) for i in range(len(wordmap))]
    higherrankverticestobechecked=set([v for v in freesplitting.nodes() if freesplitting.localgroup(v).rank>1])
    higherrankverticesthatarevg=set([])
    # now check each non-cyclic vertex in maximal free splitting
    # first do quick check if any of them are bounded surfaces
    for thisvert in higherrankverticestobechecked: 
        thisgroup=freesplitting.localgroup(thisvert)
        indexofthiswordlistintomainwordlist=[]
        thiswordlist=[]
        for i in range(len(wheredidmywordsgo)):
            if wheredidmywordsgo[i][0]==thisvert:
                indexofthiswordlistintomainwordlist.append(i)
                thiswordlist.append(wheredidmywordsgo[i][1])
        if thisgroup.isCircle(thiswordlist):
            higherrankverticesthatarevg.add(thisvert)
    higherrankverticestobechecked-=higherrankverticesthatarevg
    # remaining higherrankverticestobechecked are either rigid or have non-trivial rJSJ
    while higherrankverticestobechecked and maybevirtuallygeometric:
        thisvert=higherrankverticestobechecked.pop()
        thisgroup=freesplitting.localgroup(thisvert)
        thiswordlist=[w[1] for w in wheredidmywordsgo if w[0]==thisvert]
        # quick pre-check: if thiswordlist contins every 3-letter subword in thisgroup then it is not vg
        if split.containsAll3LetterSubwords(*thiswordlist):
            maybevirtuallygeometric=False
            break
        # get the rJSJ for thisvert with respect to thiswordlist
        thissplitting, thiswordmap=thisgroup.getRJSJ(thiswordlist, withmap=True, cutpairsearchrecursionlimit=cutpairsearchrecursionlimit, maxnumberof2componentcutstoconsider=maxnumberof2componentcutstoconsider)
        if thissplitting.edges(): # if the rSJ has edges then it is a non-trivial decomposition
            rigid=False
        unchecked=[v for v in thissplitting.nodes() if thissplitting.localgroup(v).rank>1]
        # now check each vertex in the rJSJ to see if it is vg
        # maybevirtuallygeometric means we have not found any non-vg vertices anywhere. If we ever find one we can stop immediately.
        while unchecked and maybevirtuallygeometric:
            newvert=unchecked.pop()
            newgroup=thissplitting.localgroup(newvert)
            newwordlist=split.getInducedMultiword(thissplitting,newvert,thiswordmap,simplifyandminimize=True)
            if not newgroup.isCircle(newwordlist): # if it's a circle it is geometric, otherwise this is a rigid vertex, and it is virtually geometric if and only if it is geometric
                                                 # We check geometricity via the program Heegaard. The catch is that Heegaard only checks for geometricity in orientable handlebodies
                                                 # To check non-orienatable geometricity we need to check double covers as well.
                try:
                    newvertgeometric=heegaard.is_realizable([w() for w in newwordlist], maxtime=Heegaardwaittime)
                except RuntimeError:
                    print "The program Heegaard failed to determine if input was realizable", newwordlist
                    raise RuntimeError('Heegaard failed')
                if not newvertgeometric:
                    foundsomethinggood=geometric_2_cover(newwordlist,newgroup.rank,Heegaardwaittime=Heegaardwaittime)
                    if foundsomethinggood==None:
                        raise RuntimeError('Heegaard failed')
                    else:
                        if not foundsomethinggood:
                            maybevirtuallygeometric=False
    # At this point either we have found a non-vg vertex and broken out of the loop, or we have checked every vertex group and found everything to be vg, in which case the whole thing is vg
    if tellmeifitsrigid:
        return maybevirtuallygeometric, rigid
    else:
        return maybevirtuallygeometric
                    


def geometric_2_cover(wordlist,rank,Heegaardwaittime=10):
    """
    Try to find a 2-covering in which lifts of things in wordlist are embedded.
    Return True if found one, False if no 2-covering is geometric, or None if no geometric 2-covers are found but Heegaard fails to give an answer on at least one covering.
    
    """
    working = []
    ambiguous_answer=False
    for graph in gengraphs.graphs(rank,2):
        lifts = []
        H = subgroup.subgroup(graph)
        for theword in wordlist:
            lifts = lifts+H.lifts(theword)
        strlifts = map(lambda x: x.alpha(), lifts)
        try:
            (yesno, fulltext) = heegaard.is_realizable(strlifts,full_answer=True, maxtime=Heegaardwaittime)
        except RuntimeError:
            ambiguous_answer=True
            continue
        if yesno:
            if re.search("Unable to determine",fulltext)==None:
                return True
            else:
                ambiguous_answer=True
    if not ambiguous_answer:
        return False
    else:
        return None
