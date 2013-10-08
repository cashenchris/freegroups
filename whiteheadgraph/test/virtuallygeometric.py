import whiteheadgraph.build.wgraph as wg
import copy
import group
import whiteheadgraph.build.orderedmultigraph as omg
import whiteheadgraph.split.split as split
import AutF as aut
import whiteheadgraph.build.whiteheadreduce as wreduce
from whiteheadgraph.test.knownexamples import *
import freegroup
import multiword





def vgtest(maxlength,verbose,debug,randomautomorphismlength,examplename,freegroup,wordlist,virtuallygeometric):
    nonefailed=True
    # take a known example and mix it up with an automorphism alpha
    if virtuallygeometric is None:
        return nonefailed
    F=freegroup
    rank=F.rank
    alpha,alphainv=aut.randomAutomorphismPair(F,randomautomorphismlength)

    if verbose:
        print "Trying example ", examplename, " changed by automorphism:\n", alpha
    newwordlist=[alpha(w) for w in wordlist]
    if multiword.isVirtuallyGeometric(F,newwordlist)==virtuallygeometric:
        if verbose:
            print "Correctly found vg for",examplename,"."
    else:
        nonefailed=False
        if verbose:
            print "Error computing vg for", examplename,"."
        if debug:
            if virtuallygeometric:
                print str(newwordlist)+" was expected to be virtually geometric."
            else:
                print str(newwordlist)+" was not expected to be virtually geometric."
            print '********************************'
    return nonefailed
        
def testall(maxlength=30, randomautomorphismlength=0,verbose=False, debug=False):
    
    if all([vgtest(maxlength,verbose,debug,randomautomorphismlength,k,knownexamples[k]['freegroup'],knownexamples[k]['wordlist'],knownexamples[k]['virtuallygeometric']) for k in knownexamples]):
        print "Found expected virtual geometricity in all examples."
    else:
        print "Some virtual geometrictiy tests failed."
