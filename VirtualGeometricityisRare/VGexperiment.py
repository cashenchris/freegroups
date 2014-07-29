#!/usr/bin/env python

## usage:  ./VGexperiment.py rank (minlength maxlength samplesize testgeometric)
# maxlength=0 means continue until vg rate falls below 1% for 3 consecutive lengths
# samplesize=0 means samplesize starts at 500, increases to 1000 when vg rate falls below 50%, increases to 2000 when vg rate falls below 25%,  increases to 4000 when vg rate falls below 5%, increases to 8000 when vg rate falls below 2%

import sys
import multiword, freegroup
import old_python
from time import localtime,strftime
import whiteheadgraph.split.split as split




is_geometric = old_python.heegaard.is_realizable
######
rank = int(sys.argv[1])
try:
    minlength = int(sys.argv[2])
except:
    minlength = 2
try:
    maxlength = int(sys.argv[3])
except:
    maxlength = 40
try:
    sample_size = int(sys.argv[4])
except:
    sample_size = 1000
try:
    cut_pair_limit = int(sys.argv[5])
except:
    cut_pair_limit = None
try:
    test_geometric = int(sys.argv[6])
except:
    test_geometric = True


length=minlength

if not sample_size:
    adaptive_sample_size=True
    sample_size_counter=0
    sample_size_threshholds=dict([(0,.50),(1,.25), (2,.05),(3,.02),(4,0.0)])
    sample_sizes=dict([(0,500), (1,1000),(2,2000),(3,4000), (4,8000)])
    sample_size=sample_sizes[sample_size_counter]
else:
    adaptive_sample_size=False

consecutive_low_vg=0
max_consecutive_low_vg=3
low_vg_threshhold=.01

outputname = 'rank'+str(rank)+'_threeway.txt'
badwordname = 'rank'+str(rank)+'_threeway_bad.txt'

######
outfile = open(outputname,'a')
F = freegroup.FGFreeGroup(numgens=rank)
print 'length','geometric','vg','not_vg'
outfile.write(strftime("%Y-%m-%d,%H:%M",localtime())+'\n')
while True:
    if maxlength:
        if length>maxlength:
            break
    else:
        if consecutive_low_vg>=max_consecutive_low_vg:
            break
    if test_geometric:
        geometric = 0
    else:
        geometric = ''
    vg = 0
    not_vg = 0
    longrunwords=[]
    for i in range(sample_size):
        w = F.random_word(length)
        if not split.missing_3_letter_subwords(w):
            not_vg+=1
            print length,geometric,vg,not_vg,'\r',
            sys.stdout.flush()
            continue
        if test_geometric:
            try:
                heegaard_yes = is_geometric([w.alpha()])
            except RuntimeError:
                heegaard_yes = False
            if heegaard_yes:
                geometric+=1
                print length,geometric,vg,not_vg,'\r',
                sys.stdout.flush()
                continue
        try:
            if multiword.is_virtually_geometric(F,[w],maxnumberof2componentcutstoconsider=cut_pair_limit):
                vg+=1
            else:
                not_vg+=1
        except split.TooBigError:
            # these words need more time
            longrunwords.append(w)
        except StandardError as foo:
            # try to keep a record of the bad words
            print foo, w  
            wordsfile = open(badwordname,'a') 
            wordsfile.write(str(type(foo))+foo.message+'  '+w.alpha()+'\n')
            wordsfile.close()
        print length,geometric,vg,not_vg,'\r',
        sys.stdout.flush()
    outfile.write(str(length)+ '   '+ str(geometric)+ '   '+ str(vg)+ '   ' + str(not_vg)+ '\n')
    outfile.close()
    outfile = open(outputname,'a')
    print
    length+=1
    vg_rate=1.0*(geometric+vg)/sample_size
    if vg_rate>=low_vg_threshhold:
        consecutive_low_vg=0
    else:
        consecutive_low_vg+=1
    if adaptive_sample_size:
        if vg_rate<sample_size_threshholds[sample_size_counter]:
            sample_size_counter+=1
            sample_size=sample_sizes[sample_size_counter]

        
        
outfile.close()

