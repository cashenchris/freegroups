import lazyautreps as lr
import freegroups.AutF as aut
import freegroups.freegroup as fg


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
    # improved algorithm:
    # 1. Enumerate Whitehead minimal elemtents of given length that are shortlex minimal among elements that differ by Whitehead automorphisms of 1st kind and conjugation (and inversion if noinversion=False). This is what lr.generatelazyrep does.
    # 2. Connected vertices by edges if they differ by non-inner Whitehead automorphism of second kind.
    # 3. Claim equivalence relation of belonging to same connected component is the same for both graphs. This follows from the fact that the set of Whitehead automorphisms of the first kind forms a finite group that acts on the set of Whitehead automorphisms of the second kind by the action on the defining x,Z.
    #
    # If we just want reps, can yield any element of a connected component, but since we have to compute the entire component anyway we should select the shortlex minimal element in the connected component. 
    #
    # Within a connected component there can be elements that are local minima in the shortlex ordering but are not the global minimum. Don't know any way to determine if two elements are in the same component other than constructing the entire component.
    F=fg.FGFreeGroup(numgens=rank)
    if candidates is None:
        candidates=lr.generatelazyrep(rank,length,compress,noinversion)
    remaining=set(candidates)
    newverts=set()
    while remaining:
        currentcomponent=set()
        nextvert=remaining.pop()
        newverts.add(nextvert)
        while newverts:
            v=newverts.pop()
            currentcomponent.add(v)
            if compress:
                vastuple=fg.intdecode(rank,v,shortlex=True)
            else:
                vastuple=v
            WA=aut.WhiteheadAutomorphisms(F,allow_inner=False) # generator of all Whitehead automorphisms of the second kind that are not inner
            for alpha in WA:
                # w=alpha(v)
                wastuple=tuple(lr.SLPCIrep(alpha(F.word(vastuple)),noinversion=noinversion).letters)
                if len(wastuple)>length:
                    continue
                if compress:
                    w=fg.intencode(rank,wastuple,shortlex=True)
                else:
                    w=wastuple
                if w==v or w in currentcomponent or w in newverts: # we've already seen this w
                    continue 
                else: # this w is new
                    remaining.remove(w)
                    newverts.add(w)
        # we have constructed a complete component, yield one representative from this component and then loop
        if compress:
            yield min(currentcomponent)
        else:
            yield lr.shortlexmin(list(currentcomponent))
            

def levelset(therank,theword,noinversion=True):
    """
    Given a rank of free group and element theword that is Whitehead minimal, return the set of words of the same length that are in the same Aut(F) orbit.
    """
    F=fg.FGFreeGroup(numgens=therank)
    thelen=len(theword)
    newverts=set()
    currentcomponent=set()
    vastuple=tuple(F.word(theword).letters)
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
            if len(wastuple)>thelen or wastuple in currentcomponent or wastuple in newverts:
                pass
            else:
                newverts.add(wastuple)
    return currentcomponent
        
            


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

    This is very slow. The whole point is that generateautreps is much faster than the other way.
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
