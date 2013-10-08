from group import *
from freegroup import *
import AutF as aut
import whiteheadgraph.split.split as split
import whiteheadgraph.build.wgraph as wg

print "from group import *"
print "from freegroup import *"
print "import AutF as aut"
print "import whiteheadgraph.split.split"
print "import whiteheadgraph.build.wgraph as wg"


F=FGFreeGroup(numgens=3)
print "> F=FGFreeGroup(numgens=3)"
print "> wl=[F.word('a'),F.word('bcBC')]"
wl=[F.word('a'),F.word('abcBCA'), F.word('bcAACB')]
print "> alpha, alphainverse=aut.randomAutomorphismPair(F,5) \# It's a product of 5 random Whitehead automorphisms."
alpha, alphainverse=aut.randomAutomorphismPair(F,5)
print "> print alpha\n", alpha
print "> newwordlist=[alpha(w) for w in wl]"
newwordlist=[alpha(w) for w in wl]
print "> print newwordlist\n", newwordlist
print "> print [w() for w in newwordlist]\n", [w() for w in newwordlist]
print "> F.getFreeSplittingRel(newwordlist,printresult=True,withwordmap=True)"
F.getFreeSplittingRel(newwordlist,printresult=True,withwordmap=True)

G=FGFreeGroup(['x','y'],inverses=['X','Y'])
print "> G=FGFreeGroup(['x','y'],inverses=['X','Y'])"
bs13=G.word([1,2,-1,-1,-1,-2])
print "> bs13=G.word([1,2,-1,-1,-1,-2])"

print "> G.splitsFreelyRel([bs13])"
print G.splitsFreelyRel([bs13])
print "> G.isCircle([bs13])"
print G.isCircle([bs13])
print "> G.isRigidRel([bs13])"
print G.isRigidRel([bs13])
print ">split.findCutPairs(G,wg.WGraph([bs13]),[bs13])"
print split.findCutPairs(G,wg.WGraph([bs13]),[bs13])
print "> split.findCutPairs(G,wg.WGraph([bs13, G.word([1])]),[bs13, G.word([1])])"
print split.findCutPairs(G,wg.WGraph([bs13, G.word([1])]),[bs13, G.word([1])])



