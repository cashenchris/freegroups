import matplotlib.pyplot as plt
import freegroup
import whiteheadgraph.split.split as split
from scipy.stats import linregress
from math import exp, log


def testFullWords(rank=3,minlength=100,maxlength=700,trials=100,verbose=False, cyclicallyreduced=False):
    """
    test whether random words, as cyclic words, contain every 3 letter subword or its inverse
    return xs, ys, ts where xs are lenths of random words checked, ys are percentage that were full
    , and ts are the number of trials.
    """
    F=freegroup.FGFreeGroup(numgens=rank)
    xs=[]
    ys=[]
    ts=[]
    hasall=dict()
    L=minlength

    if not trials:
        adaptive_sample_size=True
        sample_size_counter=0
        sample_size_threshholds=dict([(0,.50),(1,.75), (2,.95),(3,.98),(4,100)])
        sample_sizes=dict([(0,500), (1,1000),(2,2000),(3,4000), (4,8000)])
        trials=sample_sizes[sample_size_counter]
    else:
        adaptive_sample_size=False

    consecutive_high_rate=0
    max_consecutive_high_rate=3
    high_rate_threshhold=.99

    while True:
        if maxlength:
            if L>maxlength:
                break
        else:
            if consecutive_high_rate>=max_consecutive_high_rate:
                break
        xs.append(L)
        ts.append(trials)
        if verbose:
            print "Testing words of length "+str(L)
        hasall[L]=0
        for i in range(trials):
            if cyclicallyreduced:
                w=F.randomCyclicallyReducedWord(L)
            else:
                w=F.randomWord(L)
            if split.containsAll3LetterSubwords(w): # w, as a cyclic word, contains all 3 letter subwords
                hasall[L]+=1
        fullrate=(1.0*hasall[L])/trials
        ys.append(fullrate)
        if verbose:
            print "Found "+str(hasall[L])+" full words in "+str(trials)+" trials. (%.2f)" % fullrate
        L+=1
        if fullrate<=high_rate_threshhold:
            consecutive_high_rate=0
        else:
            consecutive_high_rate+=1
        if adaptive_sample_size:
            if fullrate>sample_size_threshholds[sample_size_counter]:
                sample_size_counter+=1
                trials=sample_sizes[sample_size_counter]
    return xs, ys, ts

def logisticapproximation(xs,ys,xs2=None):
    """
    Returns best approxiation of ys as y=1/(1+exp(mx+b))
    """      
    loggedxs=[]
    loggedys=[]
    for i in range(len(xs)):
        if ys[i]<1:
            if ys[i]>0:
                loggedxs.append(xs[i])
                loggedys.append(log(1/ys[i]-1))
    lreg=linregress(loggedxs,loggedys)
    slope=lreg[0]
    intercept=lreg[1]
    if xs2:
        zs=[1/(1+exp(slope*x+intercept)) for x in xs2]
    else:
        zs=[1/(1+exp(slope*x+intercept)) for x in xs]
    return zs

def expapproximation(xs,ys,xs2=None):
    """
    Returns best approxiation of ys as y=1-exp(mx+b)
    """      
    expedxs=[]
    expedys=[]
    for i in range(len(xs)):
        if ys[i]<1:
            if ys[i]>0:
                expedxs.append(xs[i])
                expedys.append(log(1-ys[i]))
    lreg=linregress(expedxs,expedys)
    slope=lreg[0]
    intercept=lreg[1]
    if xs2:
        zs=[max(0,1-exp(slope*x+intercept)) for x in xs2]
    else:
        zs=[max(0,1-exp(slope*x+intercept)) for x in xs]
    return zs


def smooth(xs,ys,radius=2):
    smoothedxs=[]
    smoothedys=[]
    for i in range(radius, len(xs)-radius):
        smoothedxs.append(xs[i])
        smoothedys.append(sum(ys[i-radius:i+radius+1])/(1.0+2*radius))
    return smoothedxs, smoothedys
    
