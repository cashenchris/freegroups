import freegroups.AutF as aut
import freegroups.freegroup as fg
import freegroups.whiteheadgraph as wg
import freegroups.representatives_of_AutF_orbits.generateAutForbitreps as genreps


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
    canonicalrep=genreps.shortlexmin(thereducedlevelset)
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
    Given Whiteheadminimalinputword that is a Whitehead minimal word in a free group, returns the set of words of the same length that are in the same Aut(F) orbit and SLPCI minimal.

    Note that the output only contains the input if the input is SLPCI minimal.
    """
    F,theword=fg.parseinputword(Whiteheadminimalinputword)
    newverts=set([tuple(genreps.SLPCIrep(theword,noinversion=noinversion).letters)])
    reducedlevelset=set()
    while newverts:
        v=newverts.pop()
        reducedlevelset.add(v)
        WA=aut.WhiteheadAutomorphisms(F,both_kinds=False,allow_inner=False) # generator of all Whitehead automorphisms of the second kind that are not inner
        for alpha in WA:
            w=F.cyclic_reduce(alpha(F.word(v)))
            if len(w)>len(v): # w not in the levelset
                continue
            u=tuple(genreps.SLPCIrep(w,noinversion=noinversion).letters)
            if u==v or u in reducedlevelset or u in newverts: # we've already seen this u
                continue 
            else: # this u is new
                newverts.add(u)
    return reducedlevelset








if __name__ == "__main__":
    import doctest
    doctest.testmod()
