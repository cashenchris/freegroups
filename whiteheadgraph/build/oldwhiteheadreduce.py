import wgraph as wg
import group
import AutF as aut
import networkx as nx
from fish import ProgressFish
from itertools import product

def findMincutPart(G,origin,terminus):
    """
    Find the vertices on the origin side of a mincut of G separating origin from terminus.
    """
    flow_rate, flow_dict=nx.ford_fulkerson(G,origin,terminus)
    newverts=set([origin])
    verts=set([])
    while newverts:
        thisvert=newverts.pop()
        verts.add(thisvert)
        for e in G.out_edges_iter(thisvert, data=True):
            if e[2]['capacity']>flow_dict[e[0]][e[1]] and e[1] not in verts:
                newverts.add(e[1])
    return verts

def findCutVertReduction(F, simplifiedwordlist, stopatdisconnected=False, verbose=False):
    """
    Find a Whitehead automorphism that reduces complexity, either by making components inverse closed or by eliminating a cut vertex.
    Assume the wordlist is already simplified.
    Return graphisconnected T/F, reduction (vertex, vertex set to push)/None
    """
    graphisconnected=None
    reduction=None
    undirectedsimplewg=nx.Graph()
    edgemultiplicities=dict()
    vertexvalences=dict()
    for w in simplifiedwordlist:
        for i in range(len(w)):
            try:
                vertexvalences[abs(w.letters[i])]+=1
            except KeyError:
                vertexvalences[abs(w.letters[i])]=1
            if -w.letters[i-1]<w.letters[i]:
                turn=(-w.letters[i-1],w.letters[i])
            else:
                turn=(w.letters[i],-w.letters[i-1])
            undirectedsimplewg.add_edge(*turn)
            try:
                edgemultiplicities[turn]+=1
            except KeyError:
                edgemultiplicities[turn]=1
    # first source of a reduction would be a vertex and its inverse in different components
    connectedcomponents=nx.connected_components(undirectedsimplewg)
    if len(connectedcomponents)==1:
        graphisconnected=True
    else:
        graphisconnected=False
        if stopatdisconnected:
            return graphisconnected,  reduction
        for concom in connectedcomponents:
            if len(concom)%2 and len(concom)>1: # if it has an odd number of vertices it can't be inverse closed
                for i in concom:
                    if -i in concom:
                        pass
                    else:
                        reduction=(i,concom)
                        return graphisconnected, reduction
        for concom in connectedcomponents: # none have odd length
            if len(concom)>1:
                for i in concom:
                    if -i in concom:
                        pass
                    else:
                        reduction=(i,concom)
                        typeofreduction=2
                        return graphisconnected, reduction
                
    #  All connected components are inverse closed.
    # Second source of a reduction would be a cut vertex.
    cutvertices=nx.articulation_points(undirectedsimplewg)
    try:
        cutvert=cutvertices.next()
    except StopIteration: # There were no cut vertices. Connected with no cut vertices implies all future reductions will still be connected.
        cutvert=None
    if cutvert is not None:
        undirectedsimplewg.remove_node(cutvert)
        Zcomplement=set(nx.node_connected_component(undirectedsimplewg, -cutvert))
        Z=list(set(undirectedsimplewg.nodes())-Zcomplement)+[cutvert]
        reduction=(cutvert, Z)
    return graphisconnected, reduction

def findMinCutReduction(F, simplifiedwordlist, startingvertex=None, verbose=False):
    """
    Find a Whitehead automorphism that reduces complexity.
    Assume the wordlist is already simplified.
    Assume Whithead graph is already cut vertex free and components are inverse closed.
    Return graphisconnected T/F, graphiscutvertfree T/F/N, type of reduction found 2 (non-inverse closed components)/ 1 (cutvert) / 0 (cut set smaller than valence), reduction (vertex, vertex set to push)
    """
    reduction=None
    undirectedsimplewg=nx.Graph()
    edgemultiplicities=dict()
    vertexvalences=dict()
    for w in simplifiedwordlist:
        for i in range(len(w)):
            try:
                vertexvalences[abs(w.letters[i])]+=1
            except KeyError:
                vertexvalences[abs(w.letters[i])]=1
            if -w.letters[i-1]<w.letters[i]:
                turn=(-w.letters[i-1],w.letters[i])
            else:
                turn=(w.letters[i],-w.letters[i-1])
            undirectedsimplewg.add_edge(*turn)
            try:
                edgemultiplicities[turn]+=1
            except KeyError:
                edgemultiplicities[turn]=1
    
    # Change graph to a directed graph and use maxflow/mincut to find such a cut set.
    for edge in undirectedsimplewg.edges_iter(): # write the edge multiplicities into the graph as 'capacity'
        if edge[0]<edge[1]:
            undirectedsimplewg.add_edge(*edge, capacity=edgemultiplicities[edge])
        else:
            undirectedsimplewg.add_edge(*edge, capacity=edgemultiplicities[(edge[1],edge[0])])
    simplewg=nx.DiGraph(undirectedsimplewg) # This just doubles each edge, with opposite orientations. Need directed for maxflow algorithm.
    if verbose:
        fish2=ProgressFish(total=1+F.rank)
    if startingvertex is None:
        startingvertex=1
    for i in range(startingvertex,1+F.rank)+range(1,startingvertex):
        if verbose:
            fish2.animate(amount=1+i-startingvertex)
        if vertexvalences[i]<=2:
            pass
        else:
            if verbose:
                fish2.animate(amount=i)
            z=findMincutPart(simplewg,i,-i)
            if len(z)>1:
                Z=list(z)
                reduction=(i,Z)
                return  reduction
    # Didn't find any reductions. This wordlist is already minimal.
    return  reduction



def cutvertFreeWhiteheadMinimizer(F,wordlist,simplified=False, stopatdisconnected=False, returnwordlist=False, verbose=False):
    """
    Find a sequence of Whitehead automorphisms that reduces wordlist until no cut vertices.
    Optionally stop if graph becomes disconnected.
    return graphisconnected:True/False and whiteheadsequence, where whiteheadsequence is a list of Whitehead automorphisms
    
    """
    if not simplified:
        simplifiedwordlist=wg.blindSimplifyWordlist(F,wordlist)
    else:
        simplifiedwordlist=wordlist
    nextwordlist=simplifiedwordlist
    whiteheadsequence=[]
    if verbose:
        complexity=sum([len(w) for w in nextwordlist])
        fish1=ProgressFish(total=complexity)
    graphisconnected,  nextred=findCutVertReduction(F, nextwordlist, stopatdisconnected=stopatdisconnected, verbose=verbose)
    if stopatdisconnected and not graphisconnected:
        if returnwordlist:
            return graphisconnected, whiteheadsequence, nextwordlist
        else:
            return graphisconnected, whiteheadsequence
    else:
        while nextred is not None: # loop until no further reduction is found
            reducingautomorphism=aut.WhiteheadAuto(F,*nextred)
            whiteheadsequence=[reducingautomorphism]+whiteheadsequence
            nextwordlist=[F.cyclicReduce(reducingautomorphism(w)) for w in nextwordlist]
            if verbose:
                fish1.animate(amount=sum([len(w) for w in nextwordlist]))
            graphisconnected, nextred=findCutVertReduction(F,nextwordlist, stopatdisconnected=stopatdisconnected, verbose=verbose)
            if stopatdisconnected and not graphisconnected:
                if returnwordlist:
                    return graphisconnected, whiteheadsequence, nextwordlist
                else:
                    return graphisconnected, whiteheadsequence
        if returnwordlist:
            return graphisconnected, whiteheadsequence, nextwordlist
        else:
            return graphisconnected, whiteheadsequence
        

def WhiteheadMinimizer(F, wordlist, simplified=False,verbose=False):
    """
    Find a sequence of Whitehead automorphisms that reduces wordlist to minimal complexity.
    return whiteheadsequence, where whiteheadsequence is a list of Whitehead automorphisms.
    """
    if not simplified:
        simplifiedwordlist=wg.blindSimplifyWordlist(F,wordlist)
    else:
        simplifiedwordlist=wordlist
    graphisconnected, whiteheadsequence=cutvertFreeWhiteheadMinimizer(F,simplifiedwordlist, simplified=True,verbose=verbose) #this reduces the graph so that each component is cut vertex free and inverse closed
    if whiteheadsequence:
        cutvertminimizingautomorphism=group.product(*whiteheadsequence)
        nextwordlist=[F.cyclicReduce(cutvertminimizingautomorphism(w)) for w in simplifiedwordlist]
    else:
        nextwordlist=simplifiedwordlist
    if verbose:
        print "Looking for mincut reduction"
        complexity=sum([len(w) for w in nextwordlist])
        fish1=ProgressFish(total=complexity)
    nextred=findMinCutReduction(F, nextwordlist, verbose=verbose)
    while nextred is not None:
        reducingautomorphism=aut.WhiteheadAuto(F,*nextred)
        whiteheadsequence=[reducingautomorphism]+whiteheadsequence
        nextwordlist=[F.cyclicReduce(reducingautomorphism(w)) for w in nextwordlist]
        if verbose:
            newcomplexity=sum([len(w) for w in nextwordlist])
            assert(newcomplexity<complexity)
            complexity=newcomplexity
            fish1.animate(amount=newcomplexity)
        nextred=findMinCutReduction(F,nextwordlist, startingvertex=nextred[0],verbose=verbose)
    return whiteheadsequence

def WhiteheadMinimal(F,wordlist,extrawordlist=None,simplified=False,verbose=False,blind=False,stopatdisconnected=False, minimizingsequence=False,cutvertsonly=False):
    """
    Make wordlist Whitehead minimal.

    simplied=True is wordlist is already simplified, don't try to resimplify

    blind=True to get back just the minimal wordlist and not the minimizing automorphsim and its inverse

    stopatdisconnected=True to stop as soon as the resulting Whitehead graph becomes disconnected

    cutvertsonly=True to only reduce until the resulting graph has no cut vertices

    minimizingsequence=True to track the entire sequence of reducing automorphisms.

    extrawordlist is a list of words to which reducing automorphisms are also applied.
    
    """
    results=dict([('connected',None),('wordlist',None),('minimizingautomomorphism',None),('inverseminimizer',None), ('whiteheadsequence',None),('extrawordlist',None)])
    if minimizingsequence:
        results['whiteheadsequence']=[]
    if not simplified:
        results['wordlist']=wg.blindSimplifyWordlist(F,wordlist)
    else:
        results['wordlist']=wordlist
    if extrawordlist is not None:
        results['extrawordlist']=extrawordlist
    if not blind:
        results['minimizingautomorphism']=group.Automorphism(F)
        results['inverseminimizer']=group.Automorphism(F)
    if verbose:
        complexity=sum([len(w) for w in results['wordlist']])
        fish1=ProgressFish(total=complexity)
        print "Looking for cut vertex reductions. Current complexity:"

    # Look for cut vertex reductions.
    graphisconnected,  nextred=findCutVertReduction(F, results['wordlist'], stopatdisconnected=stopatdisconnected, verbose=verbose)
    if stopatdisconnected and not graphisconnected:
        results['connected']=graphisconnected
        return results

    while nextred is not None: # loop until no further reduction is found
        reducingautomorphism=aut.WhiteheadAuto(F,*nextred)
        if minimizingsequence:
            results['whiteheadsequence']=[reducingautomorphism]+results['whiteheadsequence']
        if not blind:
            results['minimizingautomorphism']=reducingautomorphism*results['minimizingautomorphism']
            results['inverseminimizer']=results['inverseminimizer']*reducingautomorphism**(-1)
        results['wordlist']=[F.cyclicReduce(reducingautomorphism(w)) for w in results['wordlist']]
        if results['extrawordlist']:
            results['extrawordlist']=[F.cyclicReduce(reducingautomorphism(w)) for w in results['extrawordlist']]
        if verbose:
            fish1.animate(amount=sum([len(w) for w in results['wordlist']]))
        graphisconnected, nextred=findCutVertReduction(F,results['wordlist'], stopatdisconnected=stopatdisconnected, verbose=verbose)
        if stopatdisconnected and not graphisconnected:
            results['connected']=graphisconnected
            return results

    # At this point the wordlist is reduced to the point that the resutling Whitehead graph has no cut vertices
    # Connectivity of the graph will not change after this point
    results['connected']=graphisconnected
    if cutvertsonly:
        return results
    if verbose:
        print "Looking for mincut reductions. Current complexity:"
    nextred=findMinCutReduction(F, results['wordlist'], verbose=verbose)
    while nextred is not None:
        reducingautomorphism=aut.WhiteheadAuto(F,*nextred)
        if minimizingsequence:
            results['whiteheadsequence']=[reducingautomorphism]+results['whiteheadsequence']
        if not blind:
            results['minimizingautomorphism']=reducingautomorphism*results['minimizingautomorphism']
            results['inverseminimizer']=results['inverseminimizer']*reducingautomorphism**(-1)
        results['wordlist']=[F.cyclicReduce(reducingautomorphism(w)) for w in results['wordlist']]
        if results['extrawordlist']:
            results['extrawordlist']=[F.cyclicReduce(reducingautomorphism(w)) for w in results['extrawordlist']]
        if verbose:
            fish1.animate(amount=sum([len(w) for w in results['wordlist']]))
        nextred=findMinCutReduction(F,results['wordlist'], startingvertex=nextred[0],verbose=verbose)
    return results

