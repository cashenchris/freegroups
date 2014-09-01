#!/usr/bin/env python


## usage:  ./vgprofileExperiment.py rank number_of_words_in_multiword (minlength maxlength samplesize output_file_name)

# Test random multiwords for geometricity and virtual geometricity. If virtuall geometric also record whether or not rJSJ is trivial and number of rigid and QH vertices of the rJSJ.
# Only test words that do not split freely.


import freegroup
import virtuallygeometric as vg
import sys
from time import localtime,strftime
import whiteheadgraph.split.split as split

######

rank = int(sys.argv[1])
number_of_words_in_multiword=int(sys.argv[2])
try:
    minlength = int(sys.argv[3])
except:
    minlength = 1
try:
    maxlength = int(sys.argv[4])
except:
    maxlength = 40
try:
    sample_size = int(sys.argv[5])
except:
    sample_size = 100
try:
    outputname = str(sys.argv[6])
except:
    outputname = 'vgprofileData.txt'

######
outfile = open(outputname,'a')
outfile.write(strftime("%Y-%m-%d,%H:%M",localtime())+'\n')
#outfile.write('rank'+'    '+'mwlength'+'    '+'length'+'    '+'trivrjsj'+'    '+'geo'+'    '+'vgeo'+'    '+'numqh'+'    '+'numrig'+'    '+'number'+ '\n')
######

F=freegroup.FGFreeGroup(numgens=rank)
for i in range(sample_size/10):
    if True:
        for length in range(minlength,maxlength+1):
            numg=0
            numvg=0
            numnotvg=0
            results=dict()
            print 'rank','mwlength','length','geometric','vg','notvg'
            for t in range(10):
                splitsfreely=0
                wl=F.random_multiword(number_of_words_in_multiword,length)
                while split.splits_freely_rel(F,wl) and splitsfreely<50:
                    splitsfreely+=1
                    wl=F.random_multiword(number_of_words_in_multiword,length)
                if splitsfreely>=50:
                    print g,vg,notvg,'\r',
                    sys.stdout.flush()
                    break
                try:
                    geometric=vg.is_orientably_geometric(wl)
                except:
                    geometric=None
                if geometric:
                    numg+=1
                virtuallygeometric, trivrjsj, numqh, numrigid=vg.is_virtually_geometric(F,wl,rjsjprofile=True)
                if virtuallygeometric:
                    numvg+=1
                    try:
                        results[(rank,number_of_words_in_multiword,length,trivrjsj,geometric,virtuallygeometric,numqh,numrigid)]+=1
                    except KeyError:
                        results[(rank,number_of_words_in_multiword,length,trivrjsj,geometric,virtuallygeometric,numqh,numrigid)]=1
                else:
                    numnotvg+=1
                    try:
                        results[(rank,number_of_words_in_multiword,length,trivrjsj,geometric,virtuallygeometric,0,0)]+=1
                    except KeyError:
                        results[(rank,number_of_words_in_multiword,length,trivrjsj,geometric,virtuallygeometric,0,0)]=1
                print rank,number_of_words_in_multiword,length,numg,numvg,numnotvg,'\r',
                sys.stdout.flush()
            print
            print 'rank','mwlength','length','trivrjsj','geometric','vgeometric','numqh','numrigid','number'
            for k in results:
                print k,results[k]
                if k[4] is None:
                    outfile.write(str(k[0])+'    '+str(k[1])+'    '+str(k[2])+'    '+str(int(k[3]))+'    '+str(-1)+'    '+str(int(k[5]))+'    '+str(k[6])+'    '+str(k[7])+'    '+str(results[k])+ '\n')
                else:
                    outfile.write(str(k[0])+'    '+str(k[1])+'    '+str(k[2])+'    '+str(int(k[3]))+'    '+str(int(k[4]))+'    '+str(int(k[5]))+'    '+str(k[6])+'    '+str(k[7])+'    '+str(results[k])+ '\n')
            outfile.close()
            outfile = open(outputname,'a')
outfile.close()
