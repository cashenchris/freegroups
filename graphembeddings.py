# embedding a graph into a surface
import itertools
import copy
from fractions import Fraction
import fish
    
def getSurface(thegraph):
    """
    Return list of 2-cells of a surface into which thegraph embeds.
    """
    the0cells=thegraph.nodes()
    the1cells=thegraph.edgekeys
    the2cells=[]
    alledges={(k,1) for k in thegraph.edgekeys}|{(k,-1) for k in thegraph.edgekeys}
    while alledges:
        thisedge=alledges.pop()
        thisorbit=[thisedge]
        if thisedge[1]>0:
            nextvert=thegraph.terminus(thisedge[0])
        else:
            nextvert=thegraph.origin(thisedge[0])
        nextkey=thegraph.node[nextvert]['edgeorder'][(thegraph.node[nextvert]['edgeorder'].index(thisedge[0])+1)%len(thegraph.node[nextvert]['edgeorder'])]
        if thegraph.edgekeys[nextkey][0]==nextvert:
            nextedge=(nextkey,1)
        else:
            nextedge=(nextkey,-1)
        while nextedge!=thisedge:
            thisorbit.append(nextedge)
            alledges.remove(nextedge)
            if nextedge[1]>0:
                nextvert=thegraph.terminus(nextedge[0])
            else:
                nextvert=thegraph.origin(nextedge[0])
            nextkey=thegraph.node[nextvert]['edgeorder'][(thegraph.node[nextvert]['edgeorder'].index(nextedge[0])+1)%len(thegraph.node[nextvert]['edgeorder'])]
            if thegraph.edgekeys[nextkey][0]==nextvert:
                nextedge=(nextkey,1)
            else:
                nextedge=(nextkey,-1)
        the2cells.append(thisorbit)
    return the0cells,the1cells,the2cells

def Eulercharacteristic(thecellstructure):
    return len(thecellstructure[0])-len(thecellstructure[1])+len(thecellstructure[2])

def genus(thecellstructure):
    return 1-Eulercharacteristic(thecellstructure)/2

def pairedRotationStructures(theinputgraph):
    """
    Return a generator that yields all possible paired rotation structures on thegraph.
    """
    # Note that we may assume each permutation fixes one element, since we only care about cyclic ordering 
    vertexpermutations=[itertools.permutations([i for i in range(theinputgraph.valence(v)-1)]) for v in range(1,1+theinputgraph.rank)]
    productsofvertexpermutations=itertools.product(*vertexpermutations)
    for productofpermutations in productsofvertexpermutations:
        thegraphcopy=copy.deepcopy(theinputgraph)
        for v in range(1,1+thegraphcopy.rank):
            thegraphcopy.permuteEdgeOrderAtVertex(v,productofpermutations[v-1], lastfixed=True)
            thegraphcopy.makeEdgeOrdersConsistent()
        yield thegraphcopy
            
def embeddingsIntoSurfacesOfGenusAtMost(theinputgraph,n):
    for prs in pairedRotationStructures(theinputgraph):
        surface=getSurface(prs)
        g=genus(surface)
        if g<=n:
            yield prs, surface, g
def crossratio(z1,z2,z3,z4):
    return Fraction((z1-z3)*(z2-z4),(z2-z3)*(z1-z4))

def G2A0forgenusone(thesurface, edges1, edges2):
    for ithcell in range(len(thesurface[2])):
        cell=thesurface[2][ithcell]
        edgesthatappeartwice=set([])
        edgesthatappearonce=set([])
        undirectededges=[e[0] for e in cell]
        for e in undirectededges:
            if undirectededges.count(e)==2:
                edgesthatappeartwice.add(e)
            else:
                edgesthatappearonce.add(e)
        for repeated in edgesthatappeartwice:
            lowindex=undirectededges.index(repeated)
            highindex=1+lowindex+undirectededges[1+lowindex:].index(repeated)
            if highindex-lowindex==1:
                continue
            for oncepairs in itertools.combinations(edgesthatappearonce,2):
                if repeated in edges1:
                    if oncepairs[0] in edges1 or oncepairs[1] in edges1:
                        continue
                if repeated in edges2:
                    if oncepairs[0] in edges2 or oncepairs[1] in edges2:
                        continue
                firstindex=undirectededges.index(oncepairs[0])
                secondindex=undirectededges.index(oncepairs[1])
                algebraicintersectionnumbermod4=(2+cell[firstindex][1]+cell[secondindex][1]+cell[lowindex][1]+cell[highindex][1])%4
                if algebraicintersectionnumbermod4!=0:
                    continue
                if firstindex<secondindex:
                    cr=crossratio(lowindex,firstindex,highindex,secondindex)
                else:
                    cr=crossratio(lowindex,secondindex,highindex,firstindex)
                if cr>1:
                    for jthcell in [j for j in range(len(thesurface[2])) if j!=ithcell]:
                        jthcellundirectededges=[e[0] for e in thesurface[2][jthcell]]
                        if oncepairs[0] in jthcellundirectededges and oncepairs[1] in jthcellundirectededges:
                            yield ((repeated,oncepairs[0]),(repeated, oncepairs[1]))
    

def G2A0forgenustwo(thesurface, edges1,edges2):
    crossings=dict()
    for ithcell in range(len(thesurface[2])):
        cell=thesurface[2][ithcell]
        edgesthatappeartwice=set([])
        undirectededges=[e[0] for e in cell]
        for e in undirectededges:
            if undirectededges.count(e)==2:
                edgesthatappeartwice.add(e)
        pairs=itertools.combinations(edgesthatappeartwice,2)
        crossingpairs=[]
        for initialpair in pairs:
            if (initialpair[0] in edges1 and initialpair[1] in edges1) or (initialpair[0] in edges2 and initialpair[1] in edges2):
                continue
            if initialpair[1] in edges1:
                pair=(initialpair[1],initialpair[0])
            else:
                pair=initialpair
            lowindices=[undirectededges.index(pair[i]) for i in [0,1]]
            highindices=[1+lowindices[i]+undirectededges[lowindices[i]+1:].index(pair[i]) for i in [0,1]]
            cr=crossratio(lowindices[0],lowindices[1],highindices[0],highindices[1])
            if cr>1:
                if pair[0] in edges1:
                    if cell[lowindices[0]][1]==1:
                        if lowindices[1]>lowindices[0]:
                            algebraicintersectionnumber=cell[lowindices[1]][1]
                        elif highindices[1]>lowindices[0] and highindices[1]<highindices[0]:
                            algebraicintersectionnumber=cell[highindices[1]][1]
                        else:
                            raise RuntimeError()
                    elif cell[highindices[0]][1]==1:
                        if highindices[1]>highindices[0] and lowindices[1]<highindices[0]:
                            algebraicintersectionnumber=cell[highindices[1]][1]
                        elif highindices[1]<highindices[0] and lowindices[1]<lowindices[0]:
                            algebraicintersectionnumber=cell[lowindices[1]][1]
                        else:
                            raise RuntimeError()
                    else:
                        raise RuntimeError()
                else:
                    raise RuntimeError()
                crossingpairs.append((pair,algebraicintersectionnumber))
        if crossingpairs:
            crossings[ithcell]=crossingpairs
    for twocellswithcrossings in itertools.combinations(crossings.keys(),2):
        for twocrossings in itertools.product(crossings[twocellswithcrossings[0]],crossings[twocellswithcrossings[1]]):
            if twocrossings[0][1]+twocrossings[1][1]==0:
                yield (twocrossings[0][0],twocrossings[1][0])
        
            
def G2A0ImmersionCrossings(inputgraph,edges1,edges2, returnprs=False):
    prss=pairedRotationStructures(inputgraph)
    while True:
        prs=prss.next()
        surface=getSurface(prs)
        ranout=False
        if genus(surface)==1:
            thisgen=G2A0forgenusone(surface,edges1,edges2)
        elif genus(surface)==2:
            thisgen=G2A0forgenustwo(surface,edges1,edges2)
        else:
            ranout=True
        while not ranout:
            try:
                pairpair=thisgen.next()
            except StopIteration:
                ranout=True
                continue
            if returnprs:
                yield pairpair, prs
            else:
                yield pairpair


def G2A0ImmersionCrossingsFixedPRS(prs,edges1,edges2,verbose=False):
    surface=getSurface(prs)
    if genus(surface)==0:
        if verbose:
            print "genus=0"
    elif genus(surface)==1:
        if verbose:
            print "genus=1"
        thisgen=G2A0forgenusone(surface,edges1,edges2)
    elif genus(surface)==2:
        if verbose:
            print "genus=2"
        thisgen=G2A0forgenustwo(surface,edges1,edges2)
    else:
        if verbose:
            print "genus>2"
        thisgen=[]
    return thisgen
        
        
    
