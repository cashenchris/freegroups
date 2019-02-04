import networkx as nx

# G is nx.MultiDigraph where each edge carries an attribute 'label' which is a positive integer.


def one_fold(G,e,f):
    """
    Fold edges e and f together. They must have same label.
    """
    assert(G.edges[e]['label']==G.edges[f]['label'])
    if e[1]==f[1] and e[0]==f[0]:
        G.remove_edge(*e)
    elif e[0]==f[0]:
        for i in G.in_edges(e[1],keys=True,data=True):
            if i[:3]==e:
                continue
            G.add_edge(i[0],f[1],**i[3])
        for i in G.out_edges(e[1],keys=True,data=True):
            G.add_edge(f[1],i[1],**i[3])
        G.remove_node(e[1])
    elif e[1]==f[1]:
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

def fold(G,basepoint=None):
    """
    Fold graph G as much as possible. If a basepoint is specified the folding steps will not delete that vertex.
    """
    place=find_place_to_fold(G)
    if place is not None:
        if basepoint:
            if place[0][0]==place[1][0]:
                if place[0][1]==basepoint:
                    place=(place[1],place[0])
            else:
                if place[0][0]==basepoint:
                    place=(place[1],place[0])
        one_fold(G,place[0],place[1])
        fold(G,basepoint=basepoint)

def wedge(G,v,w):
    for e in G.out_edges(v,keys=True,data=True):
        G.add_edge(w,e[1],**e[3])
    for e in G.in_edges(v,keys=True,data=True):
        G.add_edge(e[0],w,**e[3])
    G.remove_node(v)
