from group import *
import AutF as aut
import whiteheadgraph.split.split as split

G1=FGGroup(['x','y'],['X','Y'],one='e')
print "> G1=FGGroup(['x','y'],['X','Y'],one='e')"
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

G=FGFreeSubgroup([F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],F,['x','y','z'],['X','Y','Z'])
print "> G=FGFreeSubgroup([F.word([1,2,3]),F.word([1,2,-1,-2]),F.word([3])],F,['x','y','z'],['X','Y','Z'])"
w4=G.word([1,2,3])
print "> w4=G.word([1,2,3])"
print "> w4()",w4()
print "> w4(G)",w4(G)
print "> w4(F)",w4(F)

print "> G.isSubgroup(F)",G.isSubgroup(F)
print "> F.isSubgroup(G)",F.isSubgroup(G)

GinF=G.getInclusion(F)
print "> GinF=G.getInclusion(F)"

print "> GinF(w4)()\n", GinF(w4)()

H=FGFreeSubgroup([G.word('xxx'),G.word('xyxyxyxy')],G,['m','n'])
print "> H=FGFreeSubgroup([G.word('xxx'),G.word('xyxyxyxy')],G,['m','n'])"
print "> print H\n" , H
w5=H.word('mmmnnn')
print "> w5=H.word('mmmnnn')"
print "> w5()\n",w5()
print ">w5(G)\n",w5(G)
print ">w5(F)\n",w5(F)
print ">(w5*w4)() \# Product is a word in the smallest common supergroup containing the two words. In this case G.\n",(w5*w4)()

print "> wl=[F.word('a'),F.word('bcBC')]"
wl=[F.word('a'),F.word('abcBCA'), F.word('bcAACB')]
print "> alpha, alphainverse=aut.randomAutomorphismPair(F,5) \# It's a product of 5 random Whitehead automorphisms."
alpha, alphainverse=aut.randomAutomorphismPair(F,5)
print "> print alpha\n", alpha
print "> newwordlist=[alpha(w) for w in wl]"
newwordlist=[alpha(w) for w in wl]
print "> print newwordlist\n", newwordlist
print "> print [w() for w in newwordlist]\n", [w() for w in newwordlist]
print "> F.getFreeSplitting(newwordlist,printresult=True,withwordmap=True)"
F.getFreeSplitting(newwordlist,printresult=True,withwordmap=True)


        
