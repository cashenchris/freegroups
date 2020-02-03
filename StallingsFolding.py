import networkx as nx

# G is nx.MultiDigraph where each edge carries an attribute 'label' which is a positive integer.
# This file meant to be low overhead version of Stallings graphs and foldings.
# Different Stallings graph with more group theory functions in freegroup.py

def fold(G,basepoint=None):
    """
    Fold graph G in place until no further folds are possible. If a basepoint is specified the folding steps will not delete that vertex.
    """
    place=find_place_to_fold(G)
    if place is not None:
        one_fold(G,place[0],place[1],basepoint)
        fold(G,basepoint)

def graphrank(thegraph):
    """
    Returns the rank of a connected graph.
    """
    return len(thegraph.edges())-len(thegraph)+1

def contains_subgraph(G,Gbase,H,Hbase):
    """
    Return true if  G contains  H as a subgraph such that the inclusion matches basepoints, orientations, and labels. This means group defined by H is subgroup of group defined by G inside ambient free group.
    """
    vertmap=dict()
    edgemap=dict()
    vertmap[Hbase]=Gbase
    newvertices=[Hbase]
    while newvertices:
        currentvertex=newvertices.pop()
        for e in H.out_edges(currentvertex,data=True,keys=True):
            if tuple(e[:3]) in edgemap:
                continue
            if e[1] not in vertmap:
                newvertices.append(e[1])
            for f in G.out_edges(vertmap[currentvertex],data=True,keys=True):
                if f[3]['label']==e[3]['label']:
                    if e[1] in vertmap:
                        if vertmap[e[1]]!=f[1]:
                            return False
                    edgemap[tuple(e[:3])]=tuple(f[:3])
                    vertmap[e[1]]=f[1]
                    break
            else:
                for f in G.in_edges(vertmap[currentvertex],data=True,keys=True):
                    if f[3]['label']==-e[3]['label']:
                        if e[1] in vertmap:
                            if vertmap[e[1]]!=f[0]:
                                return False
                        edgemap[tuple(e[:3])]=tuple(f[:3])
                        vertmap[e[1]]=f[0]
                        break
                else:
                    return False
    return True

def one_fold(G,firstedge,secondedge,basepoint=None):
    """
    Fold firstedge and secondedge together. They must have same label and a common vertex.
    If basepoint specifies a vertex then will not delete that vertex.
    """
    e=firstedge
    f=secondedge
    assert(G.edges[e]['label']==G.edges[f]['label'])
    if e[1]==f[1] and e[0]==f[0]:
        G.remove_edge(*e)
    elif e[0]==f[0]:
        if basepoint is not None and e[1]==basepoint:
            e=secondedge
            f=firstedge
        for i in G.in_edges(e[1],keys=True,data=True):
            if i[:3]==e:
                continue
            G.add_edge(i[0],f[1],**i[3])
        for i in G.out_edges(e[1],keys=True,data=True):
            G.add_edge(f[1],i[1],**i[3])
        G.remove_node(e[1])
    elif e[1]==f[1]:
        if basepoint is not None and e[0]==basepoint:
            e=secondedge
            f=firstedge
        for i in G.out_edges(e[0],keys=True,data=True):
            if i[:3]==e:
                continue
            G.add_edge(f[0],i[1],**i[3])
        for i in G.in_edges(e[0],keys=True,data=True):
            G.add_edge(i[0],f[0],**i[3])
        G.remove_node(e[0])
    else:
        raise RuntimeError

def find_place_to_fold(G):
    """
    Return a pair of edges in G that can be folded, or None if no such pair exists.
    """
    for n in G:
        for e in G.out_edges(n,keys=True,data=True):
            for f in G.out_edges(n,keys=True,data=True):
                if e!=f and e[3]['label']==f[3]['label']:
                    return e[:3],f[:3]
    for n in G:
        for e in G.in_edges(n,keys=True,data=True):
            for f in G.in_edges(n,keys=True,data=True):
                if e!=f and e[3]['label']==f[3]['label']:
                    return e[:3],f[:3]
    return None



def wedge(G,v,w):
    for e in G.out_edges(v,keys=True,data=True):
        G.add_edge(w,e[1],**e[3])
    for e in G.in_edges(v,keys=True,data=True):
        G.add_edge(e[0],w,**e[3])
    G.remove_node(v)
