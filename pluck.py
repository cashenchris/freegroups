import freegroup
import group
import whiteheadgraph.build.wgraph as wg
import whiteheadgraph.build.whiteheadreduce as wr
import whiteheadgraph.split.split as split
from fish import ProgressFish
import networkx as nx

def pluckGently(F,wordlist):
    """
    Return minimal sublist of wl such that decomposition space is connected.
    """
    assert(not F.splitsFreelyRel(wordlist))
    minwl=[]
    for i in range(len(wordlist)):
        if F.splitsFreelyRel(minwl+wordlist[i+1:]):
            minwl.append(wordlist[i])
    return minwl

    if verbose:
        print "Finding smallest initial wordlist that is connected. Current guess is words up to index:"
    totallen=len(wordlist)
    low=-1
    high=totallen+1
    nextguess=(low+high)/2
    if verbose:
        fish=ProgressFish(total=totallen)
        fish.animate(amount=nextguess)
    while low<nextguess:
        if F.splitsFreelyRel(wordlist[:nextguess+1]):
            low=nextguess
        else:
            high=nextguess
        nextguess=(low+high)/2
        if verbose:
            fish.animate(amount=nextguess)
    condensationpoint=nextguess+1
    return wordlist[:condensationpoint+1]

def pluckHard(F,wordlist, startingindex=None,startinglow=None,startinghigh=None,verbose=False):
    """
    Return a non-cyclic free factor of F and a list of words in the free factor coming from conjugates of elements of wordlist so that the decomposition space for the free factor is connected.
    """

    totallen=len(wordlist)
    if startinglow is None:
        low=-1
    else:
        low=startinglow
    if startinghigh is None:
        high=totallen+1
    else:
        high=startinghigh
    if startingindex is None:
        nextguess=(low+high)/2
    else:
        nextguess=startingindex
    assert(nextguess<=high)
    assert(low<=nextguess)
    if verbose:
        print "Finding smallest initial wordlist that is not basic. Current guess is words up to index:"+str(nextguess)
    while low<nextguess:
        if verbose:
            print "Trying words up to index "+str(nextguess)
        graphisconnected,newwordlist=wr.blindCutvertFreeWhiteheadMinimal(F,wordlist[:nextguess+1],simplified=True,verbose=verbose)
        if graphisconnected:
            high=nextguess
            nextguess=(low+high)/2
        else:
            if sum(len(w) for w in newwordlist)>nextguess+1:# this subwordlist is not basic/ decomposition space is not totally disconnected
                high=nextguess
            else:
                low=nextguess
        nextguess=(low+high)/2
    condensationpoint=nextguess+1
    if verbose:
        print "wordlist[:"+str(condensationpoint)+"] is longest basic initial wordlist."
        print "Finding free factor"
    fsplit,wordmap=F.getFreeSplittingRel(wordlist[:condensationpoint+1], withwordmap=True,simplified=True, blind=True,verbose=verbose)
    minrank=min([fsplit.localgroup(v).rank for v in fsplit if fsplit.localgroup(v).rank>1])
    assert(minrank>1)
    for v in fsplit.nodes():
        if fsplit.localgroup(v).rank==minrank:
            break
    else:
        raise RuntimeError("couldn't find the smallest nonabelian vertex group")
    G=fsplit.localgroup(v)
    wl=[wordmap[i][1] for i in range(condensationpoint+1) if wordmap[i][0]==v]
    return G, wl
    
    
            
        
