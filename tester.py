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
wl=[F.word('CBaCbacbb')]
if __name__ == "__main__":
    ipdb.run("split.getMaxFreeAndCyclicSplittingRel(F,wl)")


    #else:
    #pass
     

    
