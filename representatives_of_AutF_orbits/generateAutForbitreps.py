import freegroups.AutF as aut
import freegroups.freegroup as fg
import freegroups.enumeratefreegroupwords as enum
from collections import deque
import freegroups.whiteheadgraph as wg


def generateautreps(rank,length,compress=False,noinversion=True,candidates=None):
    """
    Generator of representatives of Aut(F) equivalence classes of words in free group F of given rank whose Whitehead complexity is given length.

    If compress=True then return values are encoded as integers with fg.intencode(rank,___,shortlex=True)
    If noinversion=False then also mod out by inversion, so we're really generating equivalence classes of cyclic subgroups rather than elements.
    """
    # slow algortihm:
    # 1. Enumerate all Whitehead minimal elements of given length, make them vertices of a graph
    # 2. Add edges between vertices that differ by a Whitehead automorphism of 1st kind, conjugation/cyclic permutation, and non-inner Whitehead automorphism of 2nd kind (and inversion, if noinversion=False).
    # 3. Whitehead says  connected components of this graph = Aut(F) orbits
    # However, this graph is highly redundant.
    # improved algorithm:
    # 1. Enumerate elements of given length that are shortlex minimal among elements that differ by permutation of, conjugation by, and inversion of generators, and by inversion of element if noinversion=False. This is what generate_precandidates does. The point is we can enumerate such words without haveing to first enumerate all words and then screen for SLPCI minimality.
    # 2. Filter for Whitehead minimality. This is what generate_candidates does.
    # 3. Think of remaining elements as vertices in graph. Connect vertices by edge if they differ by non-inner Whitehead automorphism of second kind followed by SLPCI reduction. 
    # 4. Claim equivalence relation of belonging to same connected component is the same for this graph as it is in slow algorithm. This follows from the fact that the set of Whitehead automorphisms of the first kind forms a finite group that acts on the set of Whitehead automorphisms of the second kind by the action on the defining x,Z.
    #
    # If we just want reps, can yield any element of a connected component, but since we have to compute the entire component anyway we should select the shortlex minimal element in the connected component. 
    #
    # Within a connected component there can be elements that are local minima in the shortlex ordering but are not the global minimum.
    # Example (-2, -2, -1, -2, -2, -1, -1, 2, -1)--(-2, -2, -1, -2, -1, 2, -1, 2, -1)--(-2, -2, -2, -1, -2, -2, -1, -1, -1)
    # Don't know any way to determine if two elements are in the same component other than constructing the entire component.
    F=fg.FGFreeGroup(numgens=rank)
    if candidates is None:
        candidates=generate_candidates(rank,length,compress,noinversion)
    remaining=set(candidates)
    newverts=set()
    while remaining:
        nextvert=remaining.pop()
        # construct reduced levelset of nextvert. Same logic as function reducedlevelset, except here as we find each new neighbor we also remove it from remaining.
        reducedlevelset=set()
        newverts.add(nextvert)
        while newverts:
            v=newverts.pop()
            reducedlevelset.add(v)
            if compress:
                vastuple=fg.intdecode(rank,v,shortlex=True)
            else:
                vastuple=v
            WA=aut.WhiteheadAutomorphisms(F,allow_inner=False, both_kinds=False) # generator of all Whitehead automorphisms of the second kind that are not inner
            for alpha in WA:
                w=F.cyclic_reduce(alpha(F.word(vastuple)))
                if len(w)>len(vastuple):
                    continue
                uastuple=tuple(SLPCIrep(w,noinversion=noinversion).letters)
                if compress: # w is a neighbor of v in reduced levelset
                    u=fg.intencode(rank,uastuple,shortlex=True)
                else:
                    u=uastuple
                if u==v or u in reducedlevelset or u in newverts: # we've already seen this u
                    continue 
                else: # this u is new
                    remaining.remove(u)
                    newverts.add(u)
        # we have constructed a complete component, yield one representative from this component and then loop
        if compress:
            yield min(reducedlevelset)
        else:
            yield shortlexmin(list(reducedlevelset))
            

def levelset(Whiteheadminimalinputword,noinversion=True):
    """
    Given a rank of free group and element Whiteheadminimalinputword that is Whitehead minimal, return the set of words of the same length that are in the same Aut(F) orbit.
    """
    # output is set of tuples
    F,theword=fg.parseinputword(Whiteheadminimalinputword)
    newverts=set()
    currentcomponent=set()
    vastuple=tuple(theword.letters)
    newverts.add(vastuple)
    while newverts:
        vastuple=newverts.pop()
        currentcomponent.add(vastuple)
        if not noinversion:
            w=(F.word(vastuple))**(-1)
            wastuple=tuple(w.letters)
            if wastuple in currentcomponent or wastuple in newverts:
                pass
            else:
                newverts.add(wastuple)
        autos=aut.WhiteheadAutomorphisms(F,allow_inner=True,both_kinds=True)
        for alpha in autos:
            w=alpha(F.word(vastuple))
            wastuple=tuple(w.letters)
            if len(wastuple)>len(vastuple) or vastuple==wastuple or wastuple in currentcomponent or wastuple in newverts:
                pass
            else:
                newverts.add(wastuple)
    return currentcomponent

def reduced_levelset(Whiteheadminimalinputword,noinversion=True):
    """
    Given a rank of free group and element Whiteheadminimalinputword that is Whitehead minimal, return the set of words of the same length that are in the same Aut(F) orbit and are SLPCI minimal.

    Note that the output only contains the input if the input is SLPCI minimal.
    """
    F,theword=fg.parseinputword(Whiteheadminimalinputword)
    newverts=set([tuple(SLPCIrep(theword,noinversion=noinversion).letters)])
    reducedlevelset=set()
    while newverts:
        v=newverts.pop()
        reducedlevelset.add(v)
        WA=aut.WhiteheadAutomorphisms(F,both_kinds=False,allow_inner=False) # generator of all Whitehead automorphisms of the second kind that are not inner
        for alpha in WA:
            w=F.cyclic_reduce(alpha(F.word(v)))
            if len(w)>len(v): # w not in the levelset
                continue
            u=tuple(SLPCIrep(w,noinversion=noinversion).letters)
            if u==v or u in reducedlevelset or u in newverts: # we've already seen this u
                continue 
            else: # this u is new
                newverts.add(u)
    return reducedlevelset
            



def generate_candidates(rank,length,compress=False,noinversion=False):
    """
    Generator of elements of given length of free group of given rank that are Whitehead minimal and are minimal in lexicographic ordering among elements of the orbit of a conjugate of the word or its inverse by perutations of the generators and inversion.
    If compress=False then return object is a tuple of nonzero integers where n represents the nth generator of a free group and -n represents its inverse.
    If compress=True then return object is an integer encoding the tuple using fg.intencode(rank,___,shortlex=True)
    If noinversion=True then remove "or its inverse" from the first sentence. 
    """
    # take the generator generate_precandidates and screen for whitehead minimality.
    if length==0:
        if not compress:
            yield tuple()
        else:
            yield fg.intencode(rank,[],shortlex=True)
        return
    if length==1:
        if not compress:
            yield tuple([-rank])
        else:
            yield fg.intencode(rank,tuple([-rank]),shortlex=True)
        return
    F=fg.FGFreeGroup(numgens=rank)
    thewords=generate_precandidates(rank,length,noinversion) # generator for precandidates
    for v in thewords: # for each candidate, check if it is Whitehead minimal. If not, discard.
        w=F.word(v)
        if not wg.is_minimal(F,[w]):
            continue
        if compress:
            yield fg.intencode(rank,w.letters,shortlex=True)
        else:
            yield tuple(w.letters)

def generate_precandidates(rank,length,noinversion):
    """
    Generate words in free group of given rank with given length while avoinding words that will obviously not be shortlex minimal in their orbit.
    """
    # This is an odometer. However, we notice that if there is a subword of the current word such that, after permuting and inverting generators, the image of the subword comes shortlex before the current word, then all further words in which the subword survives will not be SLPCI minimal. Therefore, we increment the odometer to disrupt the problem subword instead of at the last position. This allows us to skip over potential large ranges of values.
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

def shortlexmin2(w,v):
    if shortlexleq(w,v):
        return w
    else:
        return v
        
def shortlexmin(listofelements):
    """
    Return shortlex minimal element from a list.
    """
    if len(listofelements)==0:
        raise ValueError("shortlexmin arg is empty sequence")
    elif len(listofelements)==1:
        return listofelements[0]
    else:
        return shortlexmin2(shortlexmin(listofelements[:len(listofelements)//2]),shortlexmin(listofelements[len(listofelements)//2:]))
    





def lexleq(w,v):
    """
    Compare words w and v in lex ordering.
    """
    try:
        return w.letters<=v.letters
    except AttributeError:
        return list(w)<=list(v)

def lexmin(w,v):
    """
    Return whichever of words w or v is lex less than the other.
    """
    if lexleq(w,v):
        return w
    else:
        return v
    
def shortlexpermutationrep(w):
    """
    Return the shortlex minimal word that can be obtained from w by permuting or inverting generators.
    """
    # first letter of w is assigned to -rank. This determines image of all other copies of that letter and its inverse.
    # next unassigned letter that occurs is sent to -rank+1, etc...
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

def SLPCIrep(inputword,is_self=False,noinversion=False):
    """
    Return the shortlex minimal word that can be obtained from a conjugate of inputword or its inverse by permuting or inverting generators. 

    If noinversion=True then only apply permutation of, inversion of, and conjugation by generators to inputword, not to inverse.

    If is_self=True shortcircuit early if we find that inputword itself is not its own SLPCIrep.
    """
    F,w=fg.parseinputword(inputword)
    theletters=deque([x for x in (F.cyclic_reduce(w)).letters])
    inverseletters=deque([x for x in ((F.cyclic_reduce(w))**(-1)).letters])
    themin=w
    for i in range(len(themin)):
        themin=shortlexmin2(themin,shortlexpermutationrep(F.word(theletters)))
        if not noinversion:
            themin=shortlexmin2(themin,shortlexpermutationrep(F.word(inverseletters)))
        if is_self and themin!=w:
            return False
        theletters.rotate() # this is cyclic permutation = conjugation by a generator
        inverseletters.rotate()
    if is_self:
        if themin==w:
            return True
        else:
            return False
    else:
        return themin




def converttostring(thelist):
    thestring=''
    for x in thelist:
        if x>0:
            thestring+=chr(96+thelist)
        else:
            thestring+=chr(64-x)
    return thestring


def verify_correct_count(rank,length,noinversion=False):
    """
    Computes a set of representatives using generateautreps and another by enumerating all elements of given length in free groups and counting number of Aut(F) orbits represented by minimal length elements. Returns True if they have same length.

    This is very slow. Only used to validate generateautreps. The whole point is that generateautreps is much faster than the other way.
    """
    import networkx as nx
    import freegroups.whiteheadgraph as wg
    import freegroups.enumeratefreegroupwords as enum
    F=fg.FGFreeGroup(numgens=rank)
    g=generateautreps(rank,length,noinversion=noinversion)
    Reps=[w for w in g]
    g=enum.generate_words(rank,length,length)
    All=[w for w in g]
    assert(len(All)==2*rank*(2*rank-1)**(length-1))
    Min=[w for w in All if wg.is_minimal(F,[F.word(w)])]
    G=nx.Graph()
    for w in Min:
        G.add_node(tuple(w))
    if not noinversion:
            for w in Min:
                winv=tuple(((F.word(w))**(-1)).letters)
                G.add_edge(tuple(w),winv)
    for alpha in aut.WhiteheadAutomorphisms(F,allow_inner=True,both_kinds=True):
        for v in G:
            w=tuple((alpha(F.word(v))).letters)
            if len(w)>length:
                continue
            else:
                assert(w in G)
                G.add_edge(v,w)
    Comps=[c for c in nx.connected_components(G)]
    return len(Reps)==len(Comps)


            
