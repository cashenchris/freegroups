import whiteheadgraph.build.wgraph as wg
import copy
import group
import whiteheadgraph.build.orderedmultigraph as omg
import whiteheadgraph.split.split as split
import AutF as aut
import whiteheadgraph.build.whiteheadreduce as wreduce
from whiteheadgraph.test.knownexamples import *
import freegroup





def rjsjtest(maxlength,verbose,debug,randomautomorphismlength,examplename,freegroup,wordlist,splitsfreely):
    nonefailed=True
    if splitsfreely:
        return nonfailed
    # take a known example and mix it up with an automorphism alpha
    F=freegroup
    rank=F.rank
    alpha,alphainv=aut.randomAutomorphismPair(F,randomautomorphismlength)

    if verbose:
        print "Trying example ", examplename, " changed by automorphism:\n", alpha
    newwordlist=[alpha(w) for w in wordlist]
    gamma, wordmap=F.getRJSJ(newwordlist, withmap=True)
    minimizedwordlist=[]
    for (v,w,p) in wordmap:
        minimizedwordlist.append(gamma.localgroup(v).getInclusion(F)(w))
    if not F.isRJSJ(wordmap,gamma,verbose=verbose):
        if verbose:
            print "Error computing RJSJ for", examplename,"."
        nonefailed=False
        if debug:
            print gamma, wordmap
            print '********************************'

    if verbose and nonefailed:
        print "Correctly found RJSJ for",examplename,"."
    return nonefailed
        
def testall(maxlength=30, randomautomorphismlength=0,verbose=False, debug=False):
    
    if all([rjsjtest(maxlength,verbose,debug,randomautomorphismlength,k,knownexamples[k]['freegroup'],knownexamples[k]['wordlist'],knownexamples[k]['splitsfreely']) for k in knownexamples]):
        print "Found expected rJSJ's."
    else:
        print "Some rJSJ test failed."
