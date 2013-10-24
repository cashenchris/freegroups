import group
import freegroup
import whiteheadgraph.split.split as split
import old_python.liftsearch2 as ls2
import old_python.heegaard as heegaard
import whiteheadgraph.build.wgraph as wg

# F=freegroup.FGFreeGroup(numgens=3)
# wordlist1=[F.word('aabbccacb')]
# wordlist2=[F.word([1]), F.word([2]), F.word([3]), F.word([1,3,-2,1,-3,2])]
# isVirtuallyGeometric(F,wordlist1)=False
# isVirtuallyGeometric(F,wordlist2)=True


def isVirtuallyGeometric(F,wordlist, Heegaardwaittime=10, tellmeifitsrigid=False):
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
    freesplitting,wmap=F.getFreeSplittingRel(wordlist, withwordmap=True, minimized=True, simplified=True)
    if freesplitting.edges():
        rigid=False
    wheredidmywordsgo=[(wmap[wordmap[i][0]][0], wmap[wordmap[i][0]][1],wmap[wordmap[i][0]][2]*wordmap[i][1]) for i in range(len(wordmap))]
    higherrankverticestobechecked=set([v for v in freesplitting.nodes() if freesplitting.localgroup(v).rank>1])
    higherrankverticesthatarevg=set([])
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
    while higherrankverticestobechecked and maybevirtuallygeometric:
        thisvert=higherrankverticestobechecked.pop()
        thisgroup=freesplitting.localgroup(thisvert)
        thiswordlist=[w[1] for w in wheredidmywordsgo if w[0]==thisvert]
        thissplitting, thiswordmap=thisgroup.getRJSJ(thiswordlist, withmap=True)
        if thissplitting.edges():
            rigid=False
        unchecked=[v for v in thissplitting.nodes() if thissplitting.localgroup(v).rank>1]
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
                    raise RuntimeError
                if not newvertgeometric:
                    foundsomethinggood=ls2.look_for_good_cover(newwordlist,newgroup.rank,2,verbose=False, Heegaardwaittime=Heegaardwaittime)
                    if not foundsomethinggood:
                        maybevirtuallygeometric=False

    if tellmeifitsrigid:
        return maybevirtuallygeometric, rigid
    else:
        return maybevirtuallygeometric
                    
                                                                      
