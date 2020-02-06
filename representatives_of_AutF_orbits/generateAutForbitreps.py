import lazyautreps as lr
import freegroups.AutF as aut
import freegroups.freegroup as fg


def generateautreps(rank,length,compress=False,noinversion=True,candidates=None):
    """
    Generator of representatives of Aut(F) equivalence classes of words in free group F of given rank whose Whitehead complexity is given length.

    If compress=True then return values are encoded as integers
    If noinversion=False then also mod out by inversion, so we're really generating equivalence classes of cyclic subgroups rather than elements.
    """
    F=fg.FGFreeGroup(numgens=rank)
    if candidates is None:
        candidates=lr.generatelazyrep(rank,length,compress,noinversion)
    remaining=set(candidates)
    currentcomponent=set()
    newverts=set()
    while remaining:
        nextvert=remaining.pop()
        yield nextvert
        newverts.add(nextvert)
        while newverts:
            v=newverts.pop()
            if compress:
                vastuple=fg.intdecode(rank,v)
            else:
                vastuple=v
            WA=aut.WhiteheadAutomorphisms(F)
            for alpha in WA:
                wastuple=tuple(lr.SLPCIrep(alpha(F.word(vastuple)),noinversion=noinversion).letters)
                assert(len(wastuple)>=length)
                if len(wastuple)>length:
                    continue
                if compress:
                    w=fg.intencode(rank,wastuple)
                else:
                    w=wastuple
                if w==v or w in currentcomponent or w in newverts:
                    continue
                else:
                    remaining.remove(w)
                    newverts.add(w)
            currentcomponent.add(v)

def levelset(therank,theword):
    F=fg.FGFreeGroup(numgens=therank)
    thelen=len(theword)
    newverts=set()
    currentcomponent=set()
    vastuple=tuple(F.word(theword).letters)
    newverts.add(vastuple)
    while newverts:
        vastuple=newverts.pop()
        currentcomponent.add(vastuple)
        autos=[x for x in aut.NielsenGenerators(F)]+[x for x in aut.WhiteheadAutomorphisms(F,allow_inner=True)]
        for alpha in autos:
            w=alpha(F.word(vastuple))
            wastuple=tuple(w.letters)
            if len(wastuple)>thelen or wastuple in currentcomponent or wastuple in newverts:
                continue
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
    autos=[x for x in aut.NielsenGenerators(F)]+[x for x in aut.WhiteheadAutomorphisms(F,allow_inner=True)]
    for alpha in autos:
        for v in G:
            w=tuple((alpha(F.word(v))).letters)
            if len(w)>length:
                continue
            else:
                assert(w in G)
                G.add_edge(v,w)
    Comps=[c for c in nx.connected_components(G)]
    return len(Reps)==len(Comps)
