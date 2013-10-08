from freegroup import *
import whiteheadgraph.split.split
import pickle
results={}
trials=100
maxrank=10

results={r:{l:[0,0,0] for l in range(5*r+1)} for r in range(2,maxrank+1)}

for r in range(2,1+maxrank):
    F=FGFreeGroup(numgens=r)
    wordlength=5*r
    for i in range(1,1+wordlength):
        splitfreely=0
        rigid=0
        for j in range(trials):
            rmw=F.randomMultiword(i)
            l=sum([len(w) for w in rmw])
            while l==0:
                rmw=F.randomMultiword(i)
                l=sum([len(w) for w in rmw])
            sf=F.splitsFreelyRel(rmw)
            ir=F.isRigidRel(rmw)
            if ir and sf:
                print [w() for w in rmw], "claims to be both rigid and splittable!"
                assert(not (ir and sf))
            results[r][l][0]+=1
            results[r][l][1]+=sf
            results[r][l][2]+=ir
print " rank    multiword length   number    split freely    rigid"

for r in range(2,1+maxrank):
    for l in range(1,1+5*r):
        print '{0:2d}      {1:2d}                 {2:3d}        {3:.2}             {4:.2}'.format(r,l,results[r][l][0], float(results[r][l][1])/results[r][l][0] if results[r][l][0]!=0 else float('inf'),float(results[r][l][2])/results[r][l][0] if results[r][l][0]!=0 else float('inf'))

f=open('/Users/chris/Research/Software/freegroups/experimentresults.txt','w')
pickle.dump(results,f)
f.close()
