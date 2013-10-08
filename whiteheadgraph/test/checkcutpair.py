import whiteheadgraph.build.wgraph as wg
import copy
import group
import whiteheadgraph.build.orderedmultigraph as omg
import whiteheadgraph.split.split as split
import AutF as aut
import whiteheadgraph.build.whiteheadreduce as wreduce
from whiteheadgraph.test.knownexamples import *
import freegroup





def cutpairtest(maxlength,verbose,debug,randomautomorphismlength,examplename,freegroup,wordlist,splitsfreely,iscircle,isrigid,cutpoints,uncrossed):
    nonefailed=True
    # take a known example and mix it up with an automorphism alpha
    F=freegroup
    rank=F.rank
    alpha,alphainv=aut.randomAutomorphismPair(F,randomautomorphismlength)

    if verbose:
        print "Trying example ", examplename, " changed by automorphism:\n", alpha
    
    wm=wreduce.WhiteheadMinimal(F,[alpha(w) for w in wordlist], verbose=verbose)
    minimizingautomorphism=wm['minimizingautomorphism']
    newwordlist=wm['wordlist']
    W=wg.WGraph(newwordlist, simplified=True, verbose=verbose)
    wholeautomorphism=minimizingautomorphism*alpha
    
    newcutpoints=[wholeautomorphism(cutpoint) for cutpoint in cutpoints] 
    newuncrossed=[wholeautomorphism(uncross) for uncross in uncrossed]
    
    if not F.areEquivalentWordlists(W.getWordlist(),newwordlist):
        if verbose:
            print "Error in getWordlist for ", examplename
        nonefailed=False
    if  splitsfreely!=F.splitsFreelyRel(W.wordlist):
        if verbose:
            print "Error in splitsFreely for ", examplename
        nonefailed=False
    if  iscircle!=W.isCircle():
        if verbose:
            print "Error in isCircle for ", examplename
        nonefailed=False
    if isrigid!=F.isRigidRel(W,maxlength):
        if verbose:
            print "Error in isRigid for ", examplename
        nonefailed=False
    if not F.areEquivalentWordlists(newcutpoints,split.findCutPoints(F,W)):
        if verbose:
            print "Error in split.findCutPoints for ", examplename
        nonefailed=False
    cuts=split.findCutPairs(F,W,newwordlist,maxlength)[0]
    if not F.areEquivalentWordlists(list(cuts['cutpoints']),newcutpoints):
        if verbose:
            print "Error finding cut points in split.findCutPairs for ", examplename
        nonefailed=False
    if not F.simplifyWordlist(list(cuts['uncrossed']),newuncrossed)==[]:
        if verbose:
            print "Error too many uncrossed cut pairs in split.findCutPairs for ", examplename
        nonefailed=False
    if not F.simplifyWordlist(newuncrossed,list(set.union(set(cuts['uncrossed']),set(cuts['othercuts']))))==[]:
        if verbose:
            print "Error didn't find all uncrossed cut pairs in split.findCutPairs for ", examplename
        nonefailed=False        

    # test some random words to see if splitting info is correct
    for i in range(1,maxlength):
        w=F.randomword(i)
        w=F.cyclicReduce(w)
        if len(w)>0:
            if iscircle:
                if not split.givesCut(F,W,w)!=F.isConjugateInto(w,*newwordlist):
                    if verbose:
                        print "Error: W is a circle, so ",w," should be a cut pair in ", examplename
                    nonefailed=False
                    break
            else:
                if not split.givesCut(F,W,w)==F.isConjugateInto(w,*set.union(set(newuncrossed),set(newcutpoints))):
                    if verbose:
                        print "Warning",w," gives a cut but wasn't found in ", examplename
                        print "It may be that ",w," is a crossed cut pair and everything is ok."
                    #nonefailed=False
                    break
    if verbose and nonefailed:
        print "All tests passed for ",examplename,"."
    return nonefailed
        
def testall(maxlength=30, randomautomorphismlength=0,verbose=False,debug=False):
    
    if all([cutpairtest(maxlength,verbose,debug,randomautomorphismlength,k,knownexamples[k]['freegroup'],knownexamples[k]['wordlist'],knownexamples[k]['splitsfreely'],knownexamples[k]['iscircle'],knownexamples[k]['isrigid'],knownexamples[k]['cutpoints'],knownexamples[k]['uncrossed']) for k in knownexamples]):
        print "Found all expected cut points/pairs"
    else:
        print "Failed to find expected cut points/pairs"
    


