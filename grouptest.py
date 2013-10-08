from group import *

G1=FGGroup(['x','y'],['X','Y'],one='e')
print "G1=FGGroup(['x','y'],['X','Y'],one='e')"
w1=G1.word([])
print "w1=G1.word([])"

w2=G1.word([1,2,-2,-2,-1])
print "w2=G1.word([1,2,-2,-2,-1])"
w3=G1.word([1,1,1,1,1,1])
print "w3=G1.word([1,1,1,1,1,1])"
print "w1()",w1()
print "w2()",w2()
print "(w1*w2)()",(w1*w2)()
print "(w3*w2)()",(w3*w2)()
print "(w2*w3)()",(w2*w3)()

F=FGFreeGroup(numgens=3)
print "F=FGFreeGroup(numgens=3)"

G=FGFreeSubgroup([F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],F,['x','y','z'],['X','Y','Z'])
print "G=FGFreeSubgroup([F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],F,['x','y','z'],['X','Y','Z'])"
w4=G.word([1,2,3])
print "w4=G.word([1,2,3])"
print "w4()",w4()
print "w4(G)",w4(G)
print "w4(F)",w4(F)

print "G.isSubgroup(F)",G.isSubgroup(F)
print "F.isSubgroup(G)",F.isSubgroup(G)

GinF=G.getInclusion(F)
print "GinF=G.getInclusion(F)"

print "GinF(w4)()", GinF(w4)()

H=FGFreeSubgroup([G.word('xxx'),G.word('xyxyxyxy')],G,['m','n'])
print "H=FGFreeSubgroup([G.word('xxx'),G.word('xyxyxyxy')],G,['m','n'])"
w5=H.word('mmmnnn')
print "w5=H.word('mmmnnn')"
print "w5()",w5()
print "w5(G)",w5(G)
print "w5(F)",w5(F)
print "(w5*w4)()",(w5*w4)()

