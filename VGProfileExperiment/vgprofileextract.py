#!/usr/bin/env python

## usage:  ./vgprofileextract.py rank[2,3,4,5] number_of_words_in_multiword[1,2,3] vgprofiledatafilename

# plots interactive 3d bar graph
# green bars are geometric
# violet bars are virtually geometric but not geometric
# rJSJ profile means:
#     0 if trivial rJSJ
#     1 if non-trivial rJSJ with only one non-cyclic vertex
#     2 if non-trivial rJSJ with only two non-cyclic vertices
#     3 if non-trivial rJSJ with more than two non-cyclic vertices


import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg, log, exp, sqrt
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
####

rank=int(sys.argv[1])
mwlength=int(sys.argv[2])
vgprofilefilename=sys.argv[3]
####



def extractdata(filename,rank,mwlength,geometric,vg):
    f=open(filename)
    lines = list(f)
    f.close()
    datadict=dict()
    trials=dict()
    for line in lines:
        sline=line.split()
        if len(sline)==9:
            intline=[int(entry) for entry in sline]
            if intline[0]==rank and intline[1]==mwlength:
                try:
                    trials[intline[2]]+=intline[8]
                except KeyError:
                    trials[intline[2]]=intline[8]
                if intline[5]==vg and (intline[4]==geometric or (geometric==0 and intline[4]==-1)):
                    if intline[3]==1:
                        numverts=0
                    else:
                        numverts=intline[6]+intline[7]
                    if not intline[2] in datadict:
                        datadict[intline[2]]=dict()
                    try:
                        datadict[intline[2]][numverts]+=intline[8]
                    except KeyError:
                        datadict[intline[2]][numverts]=intline[8]
    t=max([trials[l] for l in trials])
    return datadict, t

howmanyvg=[]
datavg, trials=extractdata(vgprofilefilename,rank,mwlength,0,1)
howmanyg=[]
datag, trialsg=extractdata(vgprofilefilename,rank,mwlength,1,1)
assert(trials==trialsg)
xs=sorted(list(set(datag.keys()+datavg.keys())))
# x is length, y is rjsj profile
for y in range(0,3):
    for x in xs:
        try:
            howmanyvg.append(datavg[x][y])
        except KeyError:
            howmanyvg.append(0)
for x in xs:
    morethan2=0
    if x in datavg:
         for y in [y for y in datavg[x] if y>2]:
             morethan2+=datavg[x][y]
    howmanyvg.append(morethan2)


for y in range(0,3):
    for x in xs:
        try:
            howmanyg.append(datag[x][y])
        except KeyError:
            howmanyg.append(0)
for x in xs:
    morethan2=0
    if x in datag:
         for y in [y for y in datag[x] if y>2]:
             morethan2+=datag[x][y]
    howmanyg.append(morethan2)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

nxs=len(xs)
xpos = np.array([x-.125 for x in xs]*4+[x+.125 for x in xs]*4)
ypos = np.array([-.16]*nxs+[1-.16]*nxs+[2-.16]*nxs+[3-.16]*nxs+[-.16]*nxs+[1-.16]*nxs+[2-.16]*nxs+[3-.16]*nxs)
zpos = np.array([0]*(nxs*8))
dx = .25
dy = .33
dz = np.array(howmanyg+howmanyvg)

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=np.array(['g']*(4*nxs)+['violet']*(4*nxs)), zsort='average')
plt.xlabel('Word length')
plt.ylabel('rJSJ profile')
plt.title('Random '+str(mwlength)+'-multiwords in rank '+str(rank)+' ('+str(trials)+' trials/length)')

plt.show()

