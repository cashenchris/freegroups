import group
import freegroup
import whiteheadgraph.split.split as split
import old_python.liftsearch2 as ls2
import old_python.heegaard as heegaard

# F=freegroup.FGFreeGroup(numgens=3)
# wordlist1=[F.word('aabbccacb')]
# wordlist2=[F.word([1]), F.word([2]), F.word([3]), F.word([1,3,-2,1,-3,2])]
# isVirtuallyGeometric(F,wordlist1)=False
# isVirtuallyGeometric(F,wordlist2)=True


def isVirtuallyGeometric(F,wordlist):
    """
    Decides if a multiword is virtually geometric.
    F is a free group. wordlist is a list of words in F.
    """
    maybevirtuallygeometric=True
    splitting, wordmap=F.getMaxFreeAndCyclicSplittingRel(wordlist, withmap=True)
    unchecked=[v for v in splitting.nodes() if splitting.localgroup(v).rank>1]
    while unchecked and maybevirtuallygeometric:
        thisvert=unchecked.pop()
        thisgroup=splitting.localgroup(thisvert)
        thiswordlist=split.getInducedMultiword(splitting,thisvert,wordmap,simplifyandminimize=True)
        if not thisgroup.isCircle(thiswordlist): # if it's a circle it is geometric, otherwise this is a rigid vertex, and it is virtually geometric if and only if it is geometric
                                                 # We check geometricity via the program Heegaard. The catch is that Heegaard only checks for geometricity in orientable handlebodies
                                                 # To check non-orienatable geometricity we need to check double covers as well.
            try:
                thisvertgeometric=heegaard.is_realizable([w() for w in thiswordlist])
            except RuntimeError:
                print "The program Heegaard failed to determine if input was realizable", thiswordlist
                raise RuntimeError
            if not thisvertgeometric:
                foundsomethinggood=ls2.look_for_good_cover(thiswordlist,thisgroup.rank,2,verbose=False)
                if not foundsomethinggood:
                    maybevirtuallygeometric=False
    return maybevirtuallygeometric
                    
                                                                      
