import group
import freegroup
import whiteheadgraph.split.split as split
import whiteheadgraph.build.wgraph as wg
import multiword
from whiteheadgraph.test.knownexamples import *
import testmaxsplitting
import ipdb
import graphembeddings

F=freegroup.FGFreeGroup(numgens=3)
wl=[F.word('acbc'),F.word('aBABabc')]
W=wg.WGraph(wl,simplified=True)
edges1=['e0','e1','e2','e3']
edges2=['e4','e5','e6','e7','e8','e9','e10']

twocrossingembeddings=[]
gs=graphembeddings.pairedRotationStructures(W)
for prs in gs:
    surface=graphembeddings.getSurface(prs); 
    g=graphembeddings.genus(surface)
    if g==1:
        for x in graphembeddings.G2A0forgenusone(surface,['e0','e1','e2','e3'],['e4','e5','e6','e7','e8','e9','e10']):
            twocrossingembeddings.append((prs,surface,g,x))
    elif g==2:
        for x in graphembeddings.G2A0forgenustwo(surface,['e0','e1','e2','e3'],['e4','e5','e6','e7','e8','e9','e10']):
            twocrossingembeddings.append((prs,surface,g,x))
#if __name__ == "__main__":
#ipdb.run("graphembeddings.twocrossingsforgenusone(surface)")


    #else:
    #pass
     

    
