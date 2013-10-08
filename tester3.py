import freegroup
import freefactors as ff
import whiteheadgraph.build.whiteheadreduce as wr

def findanexample(numbertries):
    F=freegroup.FGFreeGroup(numgens=3)
    a=F.word('a')
    for i in range(numbertries):
        x=F.randomWord(10)
        while not (wr.WhiteheadComplexity(F,[a,x])>2 and wr.WhiteheadComplexity(F,[x])==1 and ff.conjugatesContainedInProperFreeFactor(F,[a,x])):
            x=F.randomWord(10)
        y=F.randomWord(10)
        while not (wr.WhiteheadComplexity(F,[a,y])>2 and wr.WhiteheadComplexity(F,[y])==1 and ff.conjugatesContainedInProperFreeFactor(F,[a,y]) and (not ff.conjugatesContainedInProperFreeFactor(F,[a,x,y]))):
            y=F.randomWord(10)
        if ff.conjugatesContainedInProperFreeFactor(F,[x,y]):
            print x,y
            break
        else:
            print "no"

def findanexample2(F,a,candidates):
    thelen=len(candidates)
    thex=0
    they=0
    while thex<thelen:
        x=candidates[thex]
        if wr.WhiteheadComplexity(F,[a,x])<3:
            thex+=1
            continue
        if not ff.conjugatesContainedInProperFreeFactor(F,[a,x]):
            thex+=1
            continue
        while they<thelen:
            y=candidates[they]
            if wr.WhiteheadComplexity(F,[x,y])==1:
                they+=1
                continue
            if wr.WhiteheadComplexity(F,[a,y])<3:
                they+=1
                continue
            if not ff.conjugatesContainedInProperFreeFactor(F,[a,y]):
                they+=1
                continue
            if ff.conjugatesContainedInProperFreeFactor(F,[a,x,y]):
                they+=1
                continue
            if ff.conjugatesContainedInProperFreeFactor(F,[x,y]):
                print x,y
                print "is good"
                return True
            else:
                print x,y
                they+=1
        thex+=1
        they=0
    
