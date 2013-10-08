import networkx as nx

class xgraph(nx.MultiDiGraph):
    def __init__(self,wordlist):
        nx.MultiDiGraph.__init__(self)
        self.add_node(0)
        counter=1
        for w in wordlist:
            currentvert=0
            newletters=[x for x in w.letters]
            while len(newletters)>1:
                nextletter=newletters.pop(0)
                self.add_node(counter)
                self.add_edge(currentvert,counter,superlabel=nextletter)
                self.add_edge(counter,currentvert,superlabel=-nextletter)
                currentvert=counter
                counter+=1
            if newletters:# word was nonempty
                nextletter=newletters.pop(0)
                self.add_edge(currentvert,0,superlabel=nextletter)
                self.add_edge(0,currentvert,-superlabel=nextletter)
            else: #word was empty
                pass

    def add_edge(self, origin, terminus, superlabel, **kwargs):
        key=1+max(0,*[edge[2] for edge in self.edges(key=True)])
        self.nx.add_edge(origin,terminus, key, superlabel=superlabel,**kwargs)
        self.nx.add_edge(terminus,origin, -key, superlabel=-superlabel,**kwargs)

    def del_edge(self,origin, terminus, superlabel): # delete an arbitrary edge with given data
        for k in self[origin][terminus]:
            if self[origin][terminus][k]['superlabel']==superlabel:
                break
        else:
            raise KeyError
        self.nx.remove_edge(origin,terminus,k)
        self.nx.remove_edge(terminus,origin,-k)

    def clone_node(self,v,new_node=None):
        if new_node==None:
            new_node=1+max(self.nodes())
        self.add_node(new_node)
        for edge in self.nx.out_edges(v,data=True):
            if edge[1]==v: # this edge is a loop at v
                if edge[2]['superlabel']>0:
                    self.add_edge(new_node,new_node,**edge[2])
            else:
                self.add_edge(new_node,edge[1],**edge[2])
        

    def switch_nodes(self,one,two):
        """
        switch two nodes, carrying edges along.
        """
        new = self.clone_node(one)
        self.del_node(one)
        self.clone_node(two,one)
        self.del_node(two)
        self.clone_node(new,two)
        self.del_node(new)
        

    def neighbors(self,vertex):
        """
        return as list
        """
        return [edge[1] for edge in self.nx.out_edges(vertex)]

    def distinct_neighbors(self,vertex):
        """
        return as set
        """
        return self[vertex].keys()

    def posedges(self):
        return [edge for edge in self.edges(data=True) if edge[2]['superlabel']>0]

    def fold(self):
        while foldonce(self)!=None:
            pass
        
def unfolded(g):
    "Return key for vertex which is not folded "
    for vertex in g.nodes():
        edges=g.nx.out_edges(vertex,data=True)
        for i in range(len(edges)-1):
            for j in range(i+1,len(edges)):
                if edges[i][2]['superlabel']==edges[j][2]['superlabel']:
        # We're going to delete one of the targets if they differ.  Make sure not to delete the source.
                    target1 = edges[i][1]; target2 = edges[j][1]
                    if target1!=target2 and target2==vertex:
                        return (vertex,edges[j],edges[i])
                    else:
                        return (vertex,edges[i],edges[j])
    return None

def foldonce(g):
    "Do a single fold (identify two edges) if possible.  Returns 1 if something happened. Returns 'None' otherwise."
    place_to_fold = unfolded(g)
    if place_to_fold==None:
        return None
    else:
        source,edge1,edge2 = place_to_fold
        target1 = edge1[1]
        target2 = edge2[1]
        foldletter = edge1[3]['superlabel']
        # First delete extra edge coming from source
        g.del_edge(source,target2,foldletter)
        # If target1=target2, we are done.
        if target1==target2:
            return g
        # We are going to delete target2, but we don't want to delete the zero node.
        if target2==0:
            g.switch_nodes(target1,target2)
            dummy = target2
            target2 = target1
            target1 = dummy
        # Now redirect edges from target2
        for edge in g.out_edges(target2,data=True):
            if edge[1]==target2:
                g.add_edge(target1,target1,**edge[2])
            else:
                g.add_edge(target1,edge[1],**edge[2])
        g.del_node(target2)
        return 1


                
def max_tree(g,rootvertex=0):
    """Return a subgraph of g which is a maximal tree."""
    needed = set(g.nodes())
    tree = xgraph()
    newverts=[rootvertex]
    tree.add_node(rootvertex)
    needed.remove(rootvertex)
    while needed:
        edges=g.nx.out_edges(newverts,key=True,data=True)
        newverts=[]
        for edge in edges:
            if edge[1] in needed:
                tree.add_edge(edge[0],edge[1],**edge[2])
                needed.remove(edge[1])
                newverts.append(edge[1])
    return tree

def mark_max_tree(g,rootvertex=0):
    needed = set(g.nodes())
    newverts=[rootvertex]
    needed.remove(rootvertex)
    rank=0
    while needed:
        edges=g.nx.out_edges(newverts,key=True,data=True)
        newverts=[]
        for edge in edges:
            if 'basislabel' in edge[3]:
                pass # we've already visited this edge
            elif edge[1] in needed: # this edge is part of the maxtree. label it and its inverse 0
                g.[edge[0]][edge[1]][edge[2]]['basislabel']=0
                g.[edge[0]][edge[1]][-edge[2]]['basislabel']=0
                needed.remove(edge[1])
                newverts.append(edge[1])
            else: # this edge is not in the maxtree and does not have a label. label it.
                rank+=1
                if edge[2]>0:
                    g.[edge[0]][edge[1]][edge[2]]['basislabel']=rank
                    g.[edge[0]][edge[1]][-edge[2]]['basislabel']=-rank
                else:
                    g.[edge[0]][edge[1]][edge[2]]['basislabel']=-rank
                    g.[edge[0]][edge[1]][-edge[2]]['basislabel']=rank
                
                    

 
