import networkx as nx
import StallingsFolding as stallings
import freegroup as fg
import whiteheadgraph.build.whiteheadreduce as wreduce



def Wsubgroups(theword):
    """
    Given a list or tuple of non-zero integers interpreted as a word in a free group, returns a list of Stallings graphs representing the maximal subgroups of minimal rank contaiing theword as an imprimitive element.
    Returns an empty list if theword is primitive.
    """
    graphs=constructgraphs(theword)
    return maximalelements(graphs)
    
def imprimitivityrank(theword,precomputedWsubgroups=None):
    """
    Given a list or tuple of non-zero integers interpreted as a word in a free group, returns the minimal rank of a subgroup contaiing theword as an imprimitive element. Returns float('inf') if theword is primitve.
    If precomputedWsubgroups=None then Wsubgroups are computed and their rank is returned. Otherwise, the rank of the precomputedWsubgroups is returned.
    """
    if precomputededWsubgroups is None:
        graphs=constructgraphs(theword)
    else:
        graphs=precomputedWsubgroups
    if graphs:
        return graphrank(graphs[0])
    else:
        return float('inf')


def immersedcycle(thegraph,theword,thebasepoint):#unused
    """
    thegraph is nx.MultiDiGraph where each edge has a non-zero integer 'label'. the word is a list of non-zero integers. Function checks if the word labels an immersed loop in thegraph based at thebasepoint.
    """
    nextvertex=thebasepoint
    for theletter in theword:
        for e in G.out_edges(nextvertex,keys=True,data=True):
            if e[3]['label']==theletter:
                nextvertex=e[1]
                break
        else:
            for e in G.in_edges(nextvertex,keys=True,data=True):
                if e[3]['label']==-theletter:
                    nextvertex=e[0]
                    break
            else:
                return False
    return nextvertex==thebasepoint
                
def vertexhaslabel(thegraph,thevertex,thelabel,returnopvert=False):
    for e in thegraph.out_edges(thevertex,data=True,keys=True):
        if e[3]['label']==thelabel:
            if returnopvert:
                return e[1]
            else:
                return True
    else:
        for e in thegraph.in_edges(thevertex,data=True,keys=True):
            if e[3]['label']==-thelabel:
                if returnopvert:
                    return e[0]
                else:
                    return True
        else:
            if returnopvert:
                return None
            else:
                return False
def graphrank(thegraph):
    return len(thegraph.edges())-len(thegraph)+1

def constructgraphs(rel):
    rank=max([abs(x) for x in rel])
    bestrank=rank
    maxedges=dict([(i,[abs(x) for x in rel].count(i)/2) for i in range(1,1+rank)])
    G=nx.MultiDiGraph()
    G.add_node(0)
    workinggraphs=[]
    finishedgraphs=[]
    workinggraphs.append((G,0,rel))
    while workinggraphs:
        oldg=workinggraphs.pop()
        if graphrank(oldg[0])>bestrank:
            continue
        currentvertex=oldg[1]
        nextlabel=oldg[2][0]
        nextsuffix=oldg[2][1:]
        # If there is already incident edge with correct label, follow it.
        nextvert=vertexhaslabel(oldg[0],currentvertex,nextlabel,returnopvert=True)
        if nextvert is not None:
            if not nextsuffix:
                if nextvert==0:
                    thisrank=graphrank(oldg[0])
                    if thisrank<=bestrank and not containedinproperfactor(oldg[0],0,rel):
                        finishedgraphs.append(oldg[0].copy())
                        bestrank=min(thisrank,bestrank)
            else:
                workinggraphs.append((oldg[0].copy(),nextvert,nextsuffix))
        else: #there is not already an incident edge with the correct label
            if len([e for e in oldg[0].edges(keys=True,data=True) if abs(e[3]['label'])==abs(nextlabel)])<maxedges[abs(nextlabel)]: #we haven't yet exceeded max number of edges with this label, so can try to add a new one
                if not nextsuffix: #if we are out of letters then the only way to make our immersed cycle is to now connect back to the basepoint
                    if vertexhaslabel(oldg[0],0,-nextlabel):
                        pass # base vertex already has an edge with the desired label, so adding another would make unfolded graph
                    else:# basepoint does not already have an incident edge with this lable, so ok to make one
                        newg=nx.MultiDiGraph(oldg[0])
                        newg.add_edge(currentvertex,0,label=nextlabel)
                        newrank=graphrank(newg)
                        if newrank<=bestrank and not containedinproperfactor(newg,0,rel):
                            finishedgraphs.append(newg)
                            bestrank=min(newrank,bestrank)
                else: # we are not out of leffers, so can add a new edge going to any available vertex, or to a new vertex
                    nextvertex=len(oldg[0])
                    newg=nx.MultiDiGraph(oldg[0])
                    newg.add_edge(currentvertex,nextvertex,label=nextlabel)
                    if graphrank(newg)<=bestrank:
                        workinggraphs.append((newg,nextvertex,nextsuffix))
                    for nextvertex in oldg[0]:
                        if vertexhaslabel(oldg[0],nextvertex,-nextlabel):
                            pass # this vertex already has an edge with the desired label, skip it
                        else:
                            newg=nx.MultiDiGraph(oldg[0])
                            newg.add_edge(currentvertex,nextvertex,label=nextlabel)
                            if graphrank(newg)<=bestrank:
                                workinggraphs.append((newg,nextvertex,nextsuffix))
    return [G for G in finishedgraphs if graphrank(G)<=bestrank]
                            
                    
def spanningtree(G,basepoint):
    seen=set([basepoint])
    newvertices=[basepoint]
    treeedges=[]
    while newvertices:
        thisvertex=newvertices.pop()
        for e in G.out_edges(thisvertex,keys=True):
            if e[1] in seen:
                pass
            else:
                seen.add(e[1])
                treeedges.append(e)
                newvertices.append(e[1])
        for e in G.in_edges(thisvertex,keys=True):
            if e[0] in seen:
                pass
            else:
                seen.add(e[0])
                treeedges.append(e)
                newvertices.append(e[0])
    return treeedges

def freebasis(G,basepoint):
    T=spanningtree(G,basepoint)
    return [e for e in G.edges(keys=True) if e not in T]

def wordexpressedinfreebasis(thegraph,thebasepoint,theword,thefreebasis):
    newexpression=[]
    currentvertex=thebasepoint
    for theletter in theword:
        for e in thegraph.out_edges(currentvertex,keys=True,data=True):
            if e[3]['label']==theletter:
                if e[:3] in thefreebasis:
                    newexpression.append(1+thefreebasis.index(e[:3]))
                currentvertex=e[1]
                break
        else:
            for e in thegraph.in_edges(currentvertex,keys=True,data=True):
                if e[3]['label']==-theletter:
                    if e[:3] in thefreebasis:
                        newexpression.append(-1-thefreebasis.index(e[:3]))
                    currentvertex=e[0]
                    break
            else:
                raise KeyError
    if currentvertex==thebasepoint:
        return newexpression
    else:
        raise KeyError
                    
def containedinproperfactor(thegraph,thebasepoint,theword):
    thefreebasis=freebasis(thegraph,thebasepoint)
    if len(thefreebasis)<=1:
        return False
    newword=wordexpressedinfreebasis(thegraph,thebasepoint,theword,thefreebasis)
    timeseachletterused=dict([(x,0) for x in range(1,1+len(thefreebasis))])
    for letter in newword:
        timeseachletterused[abs(letter)]+=1
    for k in timeseachletterused:
        if timeseachletterused[k]<2:
            return True
    F=fg.FGFreeGroup(numgens=len(thefreebasis))
    results=wreduce.whitehead_minimal(F,[F.word(newword)],stopatdisconnected=True)
    return not results['connected']
    
    
        
    

    
def spanningpaths(G,basepoint):# unused
    T=spanningtree(G,basepoint)
    workingpaths=[([],basepoint)]
    finishedpaths=[]
    while workingpaths:
        pathbase=workingpaths.pop()
        terminus=pathbase[1]
        terminal=True
        for e in G.out_edges(terminus,keys=True):
            if e!=pathbase[0][-1] and e in T:
                workingpaths.append((pathbase[0]+[e],e[1]))
                terminal=False
        for e in G.in_edges(terminus,keys=True):
            if e!=pathbase[0][-1] and e in T:
                workingpaths.append((pathbase[0]+[e],e[0]))
                terminal=False
        if terminal:
            finishedpaths.append(pathbase)
    return finishedpaths

def contains(G,Gbase,H,Hbase):
    """
    Return true if the subgroup defined by G contains the subgroup defined by H, where G and H are folded Stallings graphs.
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
                

def maximalelements(graphs):
    maximalelements=[]
    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if i==j:
                continue
            if contains(graphs[j],0,graphs[i],0):
                break
        else:
            maximalelements.append(graphs[i])
    return maximalelements


        
    
