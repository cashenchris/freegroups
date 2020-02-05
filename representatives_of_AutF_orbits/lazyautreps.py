import freegroups.freegroup as fg
import freegroups.enumeratefreegroupwords as enum
from collections import deque
import freegroups.whiteheadgraph as wg

def generatelazyrep(rank,length,compress=False,noinversion=False):
    """
    Generator of elements of given length of free group of given rank that are Whitehead minimal and are minimal in lexicographic ordering among elements of the orbit of a conjugate of the word or its inverse by perutations of the generators and inversion.
    If compress=False then return object is a tuple of nonzero integers where n represents the nth generator of a free group and -n represents its inverse.
    If compress=True then return object is an integer encoding the tuple.
    If noinversion=True then remove "or its inverse" from the first sentence. 
    """
    if length==0:
        if not compress:
            yield tuple()
        else:
            yield fg.intencode(rank,[])
        return
    if length==1:
        if not compress:
            yield tuple([-rank])
        else:
            yield fg.intencode(rank,tuple([-rank]))
        return
    F=fg.FGFreeGroup(numgens=rank)
    thelazyreps=set([])
    thewords=generate_words_lexy(rank,length,noinversion) # generator for candidate words
    for v in thewords: # for each candidate, check if it is Whitehead minimal. If not, discard.
        w=F.word(v)
        if not wg.is_minimal(F,[w]):
            continue
        if compress:
            yield fg.intencode(rank,w.letters)
        else:
            yield tuple(w.letters)


    

def shortlexleq(w,v):
    """
    Compare words w and v in shortlex ordering.
    """
    if len(w)<len(v):
        return True
    elif len(v)<len(w):
        return False
    else:
        try:
            return w.letters<=v.letters
        except AttributeError:
            return list(w)<=list(v)

def shortlexmin(w,v):
    """
    Return whichever of words w or v is shortlex less than the other.
    """
    if shortlexleq(w,v):
        return w
    else:
        return v


def lexleq(w,v):
    """
    Compare words w and v in shortlex ordering.
    """
    try:
        return w.letters<=v.letters
    except AttributeError:
        return list(w)<=list(v)

def lexmin(w,v):
    """
    Return whichever of words w or v is shortlex less than the other.
    """
    if lexleq(w,v):
        return w
    else:
        return v
    
def shortlexpermutationrep(w):
    """
    Return the shortlex minimal word that can be obtained from w by permuting or inverting generators.
    """
    try:
        theletters=[x for x in w.letters]
    except AttributeError:
        theletters=[x for x in w]
    theperm=dict()
    nextvalue=[x for x in range(-(w.group).rank,0)]
    for x in theletters:
        if x in theperm or -x in theperm:
            continue
        else:
            theperm[x]=nextvalue.pop(0)
            theperm[-x]=-theperm[x]
    return (w.group).word([theperm[x] for x in theletters])

def SLPCIrep(w,isw=False,noinversion=False):
    """
    Return the shortlex minimal word that can be obtained from a conjugate of w or its inverse by permuting or inverting generators. 
    If isw=True return bool(the SLPCIrep of w is w)
    If noinversion=True then only apply permutation and inversion of gernators to w, not to inverse of w.
    """
    F=w.group
    theletters=deque([x for x in (F.cyclic_reduce(w)).letters])
    inverseletters=deque([x for x in ((F.cyclic_reduce(w))**(-1)).letters])
    themin=w
    for i in range(len(themin)):
        themin=shortlexmin(themin,shortlexpermutationrep(F.word(theletters)))
        if not noinversion:
            themin=shortlexmin(themin,shortlexpermutationrep(F.word(inverseletters)))
        theletters.rotate()
        inverseletters.rotate()
        if isw and themin!=w:
            return False
    if isw:
        if themin==w:
            return True
        else:
            return False
    else:
        return themin



def generate_words_lexy(rank,length,noinversion):
    if length==0:
        yield []
        return
    if length==1:
        yield [-rank]
        return
    F=fg.FGFreeGroup(numgens=rank)
    currentword=[-rank for i in range(length)]
    # currentword is a counter with entries nonzero integers between -rank and rank and having the given length. We will increment on the right. However, we will try to be clever by incrementing in larger steps to avoid ranges where all elements will fail to be SLPCI minimal.
    yield currentword
    currentindex=length-1
    while currentindex: # we never need to increment index 0, because then the word would never be lex minimal in its class
        currentword=increment(rank,currentindex,currentword)
        assert(len(currentword)==length)
        if currentword[0]!=-rank:# If this happens we have exhausted all possibilities, since SLPCI minimal words always have first entry equal to -rank.
            return
        if currentword[0]==-currentword[-1]: # the currentword is not cyclially reduced; skip it.
            currentindex=length-1
            continue
        foundproblem=False # a 'problem' is a subword of (a conjugate of) currentword (or its inverse) that is lex before the prefix of currentword of the same length. If we find such a prolem currentword is not SLPCI minimal, nor is any subsequent word that doesn't change the prefix of currentword containing the problem subword. This tells us that the next index to increment is the rightmost index containing part of the problem subword. 
        Reversedword=[x for x in reversed(currentword)]
        for RI in range(1,length): # RI is the rightmost index of the problem subword. First we will check the case that the subword does not wrap.
            for subwordlength in range(2,RI+2):
                if not shortlexleq(F.word(currentword[:subwordlength]),shortlexpermutationrep(F.word(currentword[RI+1-subwordlength:RI+1]))):
                    foundproblem=True
                    currentindex=RI
                    break
            if foundproblem:
                break
            if not noinversion: # also check backwords subwords
                subwordlength=RI+1
                if not shortlexleq(F.word(currentword[:subwordlength]),shortlexpermutationrep(F.word(Reversedword[length-1-RI:length-1-RI+subwordlength]))):
                    currentindex=RI
                    foundproblem=True
                    break
        else: # didn't find any nonwrapping problem subwords. Check for wrapping problem subwords.
            for LI in range(1,length):
                if not shortlexleq(F.word(currentword),shortlexpermutationrep(F.word(currentword[LI:]+currentword[:LI]))):
                    currentindex=length-1
                    foundproblem=True
                    break
            if not noinversion and not foundproblem:
                for RI in range(length-1): # range b/c if the rightmost index is length-1 then the word wouldn't wrap
                    if not shortlexleq(F.word(currentword),shortlexpermutationrep(F.word(Reversedword[length-1-RI:]+Reversedword[:length-1-RI]))):
                        currentindex=length-1
                        foundproblem=True
                        break
        if not foundproblem:
            yield currentword
            currentindex=length-1
    # now loop and increment at the identified currentindex
            
        
def increment(rank,index,word):
    if word[index]==rank: # this index will rollover, so also increment previous index
        return increment(rank,index-1,word[:index]+[-rank for i in range(len(word)-index)])
    if word[index]==-1 or (index>0 and word[index]+1==-word[index-1]): # if incrementing by 1 yields a 0 or inverse of preceding entry then increment by 2
        return increment(rank,index,word[:index]+[word[index]+1]+word[index+1:])
    if word[index]==rank-1 and index<len(word)-1: # if incrementing by 1 yields entry=rank then we would have right cancellation, so also increment next index
        return increment(rank,index+1,word[:index]+[word[index]+1]+[-rank for i in range(len(word)-index-1)])
    return word[:index]+[word[index]+1]+[-rank for i in range(len(word)-index-1)] # no problems, just increment the current index
