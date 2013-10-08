import group
import freegroup
import whiteheadgraph.split.split as split
import whiteheadgraph.build.wgraph as wg
import multiword
from whiteheadgraph.test.knownexamples import *
import testmaxsplitting
import ipdb


    
F=freegroup.FGFreeGroup(numgens=3)
ll=[[-3,2,-1,2,1,1,-3,-1]]
wl=[F.word(l) for l in ll]
splittingword=F.word([-1])
W=wg.WGraph(wl)
ipdb.set_trace()
gamma, wordmap=split.getRelativeCyclicSplittingOver(F,W,wl,splittingword, verbose=True)

#if __name__ == "__main__":
#    pdb.run("split.getRelativeCyclicSplittingOver(F,wl,splittingword)")


#else:
#     pass
     

    
