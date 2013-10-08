import group
import freegroup
import whiteheadgraph.split.split as split

F=freegroup.FGFreeGroup(numgens=5)

def testmaxsplitting(F,wl, verbose=False, impatient=False):
    splitting, wordmap=F.getMaxFreeAndCyclicSplittingRel(wl, withmap=True, verbose=verbose, impatient=impatient)
    success=F.isRJSJ(wordmap,splitting)
    if verbose:
        if success:
            print "Testing verifies this is the canonical maximal splitting."
        else:
            print "Testing indicates this is not the canonical maximal splitting."
        print ""
    return success

def testsplittings(howmany, verbose=False, debug=False, impatient=500):
    allpassed=True
    for i in range(howmany):
        wl=F.randomMultiword(30)
        if verbose:
            print wl
        try:
            testpass=testmaxsplitting(F,wl, verbose=verbose, impatient=impatient)
        except split.TooBigError as TBE:
            if verbose:
                print TBE
        else:
            if not testpass: 
                if verbose:
                    print "fail"
                else:
                    print "fail: "+str(wl)
                allpassed=False
                if debug:
                    assert(allpassed)
    if allpassed:
        print "All passed."


