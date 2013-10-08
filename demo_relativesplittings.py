import group
import freegroup
import whiteheadgraph.split.split

print "> import group"
print "> import freegroup"
print "> import whiteheadgraph.split.split"

F=freegroup.FGFreeGroup(numgens=3)
print "> F=freegroup.FGFreeGroup(numgens=3)"

wl1=[F.word('aabbAb'),F.word('bcB'),F.word('ccc')]
print "> wl1=[F.word('aabbAb'),F.word('bcB'),F.word('ccc')]"
print "> print F.splitsFreelyRel(wl1)"
print F.splitsFreelyRel(wl1)

gamma1=F.getFreeSplittingRel(wl1)
print "> gamma1=F.getFreeSplittingRel(wl1)"
print "> print gamma1"
print gamma1

wl2=[F.word('aabAAAB'),F.word('aacAAAC')]
print "> wl2=[F.word('aabAAAB'),F.word('aacAAAC')]"



