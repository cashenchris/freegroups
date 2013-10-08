from group import *
from freegroup import *

print "from group import *"

G1=FGGroup(['x','y'],inverses=['X','Y'],identity='e')
print "> G1=FGGroup(['x','y'],inverses=['X','Y'],identity='e')"
w1=G1.word([])
print "> w1=G1.word([])"

w2=G1.word([1,2,-2,-2,-1])
print "> w2=G1.word([1,2,-2,-2,-1])"
w3=G1.word([1,1,1,1,1,1])
print "> w3=G1.word([1,1,1,1,1,1])"
print "> w1()\n",w1()
print "> w2()\n",w2()
print "> (w1*w2)()\n",(w1*w2)()
print "> (w3*w2)()\n",(w3*w2)()
print "> (w2*w3)()\n",(w2*w3)()
print "> (w2**(-3))()\n",(w2**(-3))()

F=FGFreeGroup(numgens=3)
print "> F=FGFreeGroup(numgens=3)"
print "> print F\n", F

G=FGSubgroupOfFree(F,[F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],gens=['x','y','z'],inverses=['X','Y','Z'])
print "> G=FGSubgroupOfFree(F,[F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],['x','y','z'],inverses=['X','Y','Z'])"

print "> w4=G.word([1,2,3])"
w4=G.word([1,2,3])
print "> w4()\n", w4()
print "> w4(G)\n", w4(G)
print "> w4(F)\n", w4(F)

print "> G.isSubgroup(F)\n",G.isSubgroup(F)
print "> F.isSubgroup(G)\n",F.isSubgroup(G)

GinF=G.getInclusion(F)
print "> GinF=G.getInclusion(F)"

print "> GinF(w4)()\n", GinF(w4)()

H=FGSubgroupOfFree(G,[G.word('xxx'),G.word('xyxyxyxy')],gens=['m','n'])
print "> H=FGSubgroupOfFree(G,[G.word('xxx'),G.word('xyxyxyxy')],['m','n'])"
print "> print H\n" , H
w5=H.word('mmmnnn')
print "> w5=H.word('mmmnnn')"
print "> w5()\n",w5()
print ">w5(G)\n",w5(G)
print ">w5(F)\n",w5(F)
print ">(w5*w4)() \# Product is a word in the smallest common supergroup containing the two words, in this case G.\n",(w5*w4)()




        
