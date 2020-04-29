import freegroups.AutF as aut
import freegroups.freegroup as fg
import freegroups.whiteheadgraph as wg
from collections import deque



def canonical_representative_in_AutF_orbit(inputword,compress=False,noinversion=True):
    """
    Give the shortlex minimal element (with respect to fixed basis) in the same AutF orbit as the inputword. 

    Lex ordering is integer ordering, or the corresponding ordering on string generators: -2<-1<1<2 and 'B'<'A'<'a'<'b'

    If noinversion=False then return the shortlex minimal element in the union of the AutF orbit of the inputword and its inverse.

    >>> canonical_representative_in_AutF_orbit('abc')
    'C'
    >>> canonical_representative_in_AutF_orbit([3,1,2,1,2,1,2,-3])
    [-3, -3, -3]
    >>> canonical_representative_in_AutF_orbit('zxyXZY')
    'ZYzy'
    """
    # Does Whitehead peak reduction and then enumerates the reduced levelset and finds minimal element.
    if not inputword:
        return inputword
    F,theword=fg.parseinputword(inputword)
    wmin=wg.whitehead_minimal_representative(theword)
    thereducedlevelset=reduced_levelset(wmin,noinversion)
    canonicalrep=shortlexmin(thereducedlevelset)
    if compress:
        return fg.intencode(F.rank,canonicalrep,shortlex=True)
    if hasattr(inputword,'group'):
        return F.word(canonicalrep)
    elif type(inputword)==str:
        return (F.word(canonicalrep))()
    elif type(inputword)==list and type(inputword[0])==int:
        return list(canonicalrep)
    else:
        return canonicalrep

def is_canonical_representative_in_AutF_orbit(inputword,noinversion=True,skipchecks=False):
    """
    Decides if the inputword is the canonical representative of its AutF orbit.

    if noinversion=False then decide if inputword is shortlex minimal element in the union of the AutF orbits of inputword and its inverse.
    """
    F,theword=fg.parseinputword(inputword)
    inputwordastuple=tuple(theword.letters)        
    if not skipchecks:
        if not wg.is_minimal(F,[theword]):
            return False
        if not inputwordastuple==tuple(SLPCIrep(theword,noinversion=noinversion).letters):
            return False
    newverts=set([inputwordastuple])
    reducedlevelset=set()
    while newverts:
        v=newverts.pop()
        reducedlevelset.add(v)
        WA=aut.WhiteheadAutomorphisms(F,both_kinds=False,allow_inner=False) # generator of all Whitehead automorphisms of the second kind that are not inner. We don't need first kind or inner because they don't change the SLPCIrep.
        for alpha in WA:
            w=F.cyclic_reduce(alpha(F.word(v)))
            if len(w)>len(v): # w not in the levelset
                continue
            u=tuple(SLPCIrep(w,noinversion=noinversion).letters)
            if u<inputwordastuple: # u has same length as input but is a lex predecessor
                return False
            if u==v or u in reducedlevelset or u in newverts: # we've already seen this u
                continue 
            else: # this u is in the level set, is not lex smaller, and is new
                newverts.add(u)
    return True

def levelset(Whiteheadminimalinputword,noinversion=True):
    """
    Given Whiteheadminimalinputword that is a Whitehead minimal word in a free group, returns the set of words of the same length that are in the same Aut(F) orbit.
    """
    # output is set of tuples
    F,theword=fg.parseinputword(Whiteheadminimalinputword)
    newverts=set()
    currentcomponent=set()
    vastuple=tuple(theword.letters)
    newverts.add(vastuple)
    if not noinversion:
        newverts.add(tuple((theword**(-1)).letters))
    while newverts:
        vastuple=newverts.pop()
        currentcomponent.add(vastuple)
        autos=aut.WhiteheadAutomorphisms(F,allow_inner=True,both_kinds=True)
        for alpha in autos:
            w=F.cyclic_reduce(alpha(F.word(vastuple)))
            wastuple=tuple(w.letters)
            if len(wastuple)>len(vastuple) or vastuple==wastuple or wastuple in currentcomponent or wastuple in newverts:
                pass
            else:
                newverts.add(wastuple)
    return currentcomponent

def reduced_levelset(Whiteheadminimalinputword,noinversion=True):
    """
    Given Whiteheadminimalinputword that is a Whitehead minimal word in a free group, returns the set of words of the same length that are in the same Aut(F) orbit and SLPCI minimal.

    Note that the output only contains the input if the input is SLPCI minimal.
    """
    # output is set of tuples
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
        
def shortlexmin(iterable):
    """
    Return shortlex minimal element.
    """
    listofelements=list(iterable)
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




            



if __name__ == "__main__":
    import doctest
    doctest.testmod()
