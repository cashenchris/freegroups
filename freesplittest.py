from group import *
import whiteheadgraph.split.split

F=FGFreeGroup(numgens=5)

for i in range(10):
    wl=F.randomMultiword(i)
    if F.splitsFreely(wl):
        print [w() for w in wl]
        Gamma,wm=F.getFreeSplitting(wl, withwordmap=True, printresult=True)
        print "========================================="
