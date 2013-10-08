import freegroup
import whiteheadgraph.build.wgraph as wg
import whiteheadgraph.build.whiteheadreduce as wr

def conjugatesContainedInProperFreeFactor(F,wordlist):
    W=wg.WGraph(wordlist,autominimize=True)
    for vert in W:
        if not W.valence(vert):
            break
    else:
        return False
    return True
