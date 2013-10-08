import freegroup
import graphembeddings as ge
from scallop import scl
from numpy.linalg import matrix_rank
import whiteheadgraph.build.wgraph as wg
import whiteheadgraph.split.split as split
import whiteheadgraph.build.whiteheadreduce as wr
from numpy import prod
from math import factorial
import smtplib
import enumeratewords
import itertools
import heegaard

def homologicalDimension(*words):
    if len(words)==0:
        return 0
    F=words[0].group
    matrix=[F.abelianization(w) for w in words]
    return matrix_rank(matrix)
    

rank=3
xlength=5
ylength=5
ulength=8
newxy=20
scallopmaxtime=3000
maxnumberprses=100000
F=freegroup.FGFreeGroup(numgens=rank)

def getsimpleloopcandidate(F=F,xlength=xlength,ylength=ylength,ulength=ulength,newxy=newxy,scallopmaxtime=scallopmaxtime):
    while True:
        x0=F.word([1])#F.randomWord(xlength)
        while freegroup.ishomologicallytrivial(x0):
            x0=F.randomword(xlength)
        y0=F.randomWord(ylength)
        while homologicalDimension(x0,y0)<2 or F.splitsFreelyRel([x,y]):
            y0=F.randomword(ylength)
        G=freegroup.FGSubgroupOfFree(F,[x0,y0])
        incl=G.getInclusion(F)
        utriesleft=newxy
        while utriesleft:
            u00=G.randomcommutator(ulength)
            utriesleft-=1
            if len(u00)==0:
                continue
            u0=incl(u00)
            v0=u**(-1)*x0*y0*x0**(-1)*y0**(-1)
            if len(v0)==0:
                continue
            u=F.cyclicReduce(u0)
            v=F.cyclicReduce(v0)
            minimized=wr.WhiteheadMinimal(F,[u,v],[x0,y0],simplified=True,blind=True)
            x=minimized['extrawordlist'][0]
            y=minimized['extrawordlist'][1]
            u=minimized['wordlist'][0]
            v=minimized['wordlist'][1]
            if F.splitsFreelyRel([x,y,u,v]):
                continue
            #try:
            #    thescl=scl(u,v,maxtime=scallopmaxtime)
            #    print "scl"+str(scl)
            #except RuntimeError:
            #    continue
            #if thescl==0:
            #    continue
            return x,y,u,v, x0,y0,u0,v0
   

def generatecandidates(F=F,xlength=xlength,ylength=ylength,ulength=ulength,newxy=newxy,scallopmaxtime=scallopmaxtime,maxnumberprses=maxnumberprses):
    while True:
        x,y,u,v=getsimpleloopcandidate(F,xlength,ylength,ulength,newxy,scallopmaxtime)
        W=wg.WGraph([u,v],simplified=True)
        prses=prod([factorial(W.valence(j)-1) for j in range(1,1+W.rank)])
        #if prses<maxnumberprses and prses>0:
        yield (x,y,u,v,prses)
    


def admitsG2A0Immersion(u,v):
    W=wg.WGraph([u,v],simplified=True)
    uedges=['e'+str(i) for i in range(len(u))]
    vedges=['e'+str(i+len(u)) for i in range(len(v))]
    crossings=ge.G2A0ImmersionCrossings(W,uedges,vedges)
    try:
        crossings.next()
        return True
    except StopIteration:
        return False
    

def getw(F,Wprs,crossingpairpair):
    wletters=[]
    zerothedge=crossingpairpair[0][0]
    crossingedge=crossingpairpair[0][1]
    if crossingedge in crossingpairpair[1]:# zerothedge might be in both crossings. assume crossingedge is not
        zerothedge=crossingpairpair[0][1]
        crossingedge=crossingpairpair[0][0]
        if crossingedge in crossingpairpair[1]:
            raise RuntimeError, "repeated crossing?"
    firstvert=Wprs.terminus(crossingedge)
    wletters.append(firstvert)
    nextedge=Wprs.nextEdge(crossingedge,firstvert)
    nextvert=firstvert
    while nextedge not in crossingpairpair[1]:
        nextvert=Wprs.oppositeEnd(nextedge,-nextvert)
        wletters.append(nextvert)
        nextedge=Wprs.nextEdge(nextedge,nextvert)
    if zerothedge in crossingpairpair[1]:
        pass
    else:
        if nextedge==crossingpairpair[1][0]:
            nextedge=crossingpairpair[1][1]
        else:
            nextedge=crossingpairpair[1][0]
        nextvert=Wprs.terminus(nextedge)
        wletters.append(nextvert)
        nextedge=Wprs.nextEdge(nextedge,nextvert)
        while nextedge not in crossingpairpair[0]:
            nextvert=Wprs.oppositeEnd(nextedge,-nextvert)
            wletters.append(nextvert)
            nextedge=Wprs.nextEdge(nextedge,nextvert)
    return F.word(wletters)

def getz(F,Wprs,crossingpairpair,uedges,vedges):
    # find a vertex with adjacent u and v edges
    foundstart=False
    for j in range(1,1+Wprs.rank):
        valence=Wprs.valence(j)
        for i in range(valence):
            if Wprs.node[j]['edgeorder'][i] in uedges and Wprs.node[j]['edgeorder'][(i+1)%valence] in vedges:
                firstuedge=Wprs.node[j]['edgeorder'][i]
                firstvedge=Wprs.node[j]['edgeorder'][(i+1)%valence]
                foundstart=True
                break
            elif Wprs.node[j]['edgeorder'][i] in vedges and Wprs.node[j]['edgeorder'][(i+1)%valence] in uedges:
                firstvedge=Wprs.node[j]['edgeorder'][i]
                firstuedge=Wprs.node[j]['edgeorder'][(i+1)%valence]
                foundstart=True
                break
        if foundstart:
            break

    # now follow u edges until reach a crossing, then switch to v edges until reach firstvedge
    zletters=[]
    nextvert=Wprs.terminus(firstuedge)
    zletters.append(nextvert)
    nextedge=Wprs.nextEdge(firstuedge,nextvert)
    while (nextedge not in crossingpairpair[0]) and (nextedge not in crossingpairpair[1]): # follow along u
        nextvert=Wprs.oppositeEnd(nextedge,-nextvert)
        zletters.append(nextvert)
        nextedge=Wprs.nextEdge(nextedge,nextvert)
    # now we've reached one of the crossings
    if nextedge in crossingpairpair[0]:
        if nextedge==crossingpairpair[0][0]:
            nextedge=crossingpairpair[0][1]
        elif nextedge==crossingpairpair[0][1]:
            nextedge=crossingpairpair[0][0]
        else:
            raise RuntimeError
    elif nextedge in crossingpairpair[1]:
        if nextedge==crossingpairpair[1][0]:
            nextedge=crossingpairpair[1][1]
        elif nextedge==crossingpairpair[1][1]:
            nextedge=crossingpairpair[1][0]
        else:
            raise RuntimeError
    else:
        raise RuntimeError
    # nextedge is now a vedge. Follow v until we return to firstvedge
    if nextedge!=firstvedge:
        nextvert=Wprs.terminus(nextedge)
        zletters.append(nextvert)
        nextedge=Wprs.nextEdge(nextedge,nextvert)
        while nextedge!=firstvedge:
            nextvert=Wprs.oppositeEnd(nextedge,-nextvert)
            zletters.append(nextvert)
            nextedge=Wprs.nextEdge(nextedge,nextvert)
    z=F.word(zletters)
    return z
    
    
def xyzinjective(u,v,w,x,y,z):
    if homologicalDimension(x,y,z)<3:
        return False
    kerneldimension=homologicalDimension(u,v,w)
    if kerneldimension==0:
        return True
    elif kerneldimension==1: # u and v are homologous by construction
        if freegroup.ishomologicallytrivial(u):
            k=u
        elif freegroup.ishomologicallytrivial(w):
            k=w
        else:
            raise RuntimeError
        if homologicalDimension(k,x,y,z)==4:
            return True
        else:
            return False
    elif kerneldimension==2:
        if homologicalDimension(u,w,x,y,z)==5:
            return True
        else:
            return False
    else:
        raise RuntimeError

failurelog=[]
counterexample=None
    
def findacounterexampletothesimpleloopconjecture(counterexample,failurelog):
    candidatesexamined=0
    candidategenerator=generatecandidates()
    while not counterexample:
        candidatesexamined+=1
        print candidatesexamined
        x,y,u,v,prses=candidategenerator.next()
        print x, y, u, v, prses
        W=wg.WGraph([u,v],simplified=True)
        uedges=['e'+str(i) for i in range(len(u))]
        vedges=['e'+str(i+len(u)) for i in range(len(v))]
        crossings=ge.G2A0ImmersionCrossings(W,uedges,vedges,returnprs=True)
        noknownG2A0immersions=True
        for (crossingpair,Wprs) in crossings:
            noknownG2A0immersions=False
            w=getw(F,Wprs,crossingpair)
            z=getz(F,Wprs,crossingpair,uedges,vedges)
            if xyzinjective(u,v,w,x,y,z):
                counterexample=(u,v,w,x,y,z,Wprs)
                sendalertemail(counterexample)
                break
            else:
                print "Not injective on relative homology."
                failurelog.append((u,v,w,x,y,z,Wprs))
        if noknownG2A0immersions:
            print "No G2A2 immersions."
            
            
            

def sendalertemail(counterexample):
    sender = 'cashenchris@gmail.com'
    receivers = ['cashenchris@gmail.com']

    message = """From:computer
    To: Chris
    Subject: Found possible counterexample

    I found the following possible counterexample. Please check it.
    """+str(counterexample)

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)         
       print "Successfully sent email"
    except smtplib.SMTPException:
       print "Error: unable to send email"        

def specialgenerator(F):
    counter=0
    ll=[[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 2], [1, 1, 1, 2, 2], [1, 1, 1, 2, 2, 2], [1, 1, 2, 2], [1, 1, 2, 2, 1, -2, -2], [1, 1, 2, 2, -1, 2], [1, 1, 2, 2, -1, -2, -2], [1, 1, 2, -1, -1, 2], [1, 1, 2, -1, 2], [1, 1, 1, 2, 1, -2, -2], [1, 1, 1, 2, -1, 2], [1, 1, 1, 2, -1, 2, 2], [1, 1, 1, 2, -1, -2, -2]]
    l=[F.word(l) for l in ll]
    while counter<len(l):
        yield l[counter]
        counter+=1

def generatesimpleloopcandidate(F=F,xlength=xlength,ylength=ylength,ulength=ulength,newxy=newxy,scallopmaxtime=scallopmaxtime):
    ygenerator=enumeratewords.generatewords(F,6)
    xgenerator=specialgenerator(F)
    xygenerator=itertools.product(xgenerator,ygenerator)
    x0,y0=xygenerator.next()
    while homologicalDimension(x0,y0)<2:
        x0,y0=xygenerator.next()
    while True:
        G=freegroup.FGSubgroupOfFree(F,[x0,y0])
        incl=G.getInclusion(F)
        thisugenerator=enumeratewords.generatewordsincommutatorsubgroup(G,1,1)
        while True:
            try:
                u00=thisugenerator.next()
            except StopIteration:
                break
            u0=incl(u00)
            v0=u0**(-1)*x0*y0*x0**(-1)*y0**(-1)
            if len(v0)==0:
                continue
            u=F.cyclicReduce(u0)
            v=F.cyclicReduce(v0)
            minimized=wr.WhiteheadMinimal(F,[u0,v0],[x0,y0],simplified=True,blind=True)
            x=minimized['extrawordlist'][0]
            y=minimized['extrawordlist'][1]
            u=minimized['wordlist'][0]
            v=minimized['wordlist'][1]
            if F.splitsFreelyRel([x,y,u,v]):
                continue
            else:
                yield ((x,y,u,v),(x0,y0,u0,v0))
        x0,y0=xygenerator.next()
        while homologicalDimension(x0,y0)<2:
            x0,y0=xygenerator.next()

def isreasonable(W):
    numprses=prod([factorial(W.valence(j)-1) for j in range(1,1+W.rank)])
    if numprses < 10000000 and numprses>0:
        return True
    else:
        print "unreasonable"
        return False

def checkcrossingandhomologicalconditions(x,y,u,v,W, verbose=False):
    uedges=['e'+str(j) for j in range(len(u))]
    vedges=['e'+str(j+len(u)) for j in range(len(v))]
    crossings=ge.G2A0ImmersionCrossings(W,uedges,vedges,returnprs=True)
    for (crossingpairpair,Wprs) in crossings:
        print "G2A0 for "+str((x,y,u,v))
        w=getw(F,Wprs,crossingpairpair)
        z=getz(F,Wprs,crossingpairpair)
        if xyzinjective(u,v,w,x,y,z):
            counterexample=(u,v,w,x,y,z,Wprs)
            #sendalertemail(counterexample)
            print counterexample
            return True
    else:
        return False


def populatecandidatedictionary(candidates, provisionalcandidates1, provisionalcandidates2):
    candidatesconsidered=0
    scl0=0
    nongeomcurve=0
    ge=generatesimpleloopcandidate()
    for c in ge:
        heegaardfailed=False
        candidatesconsidered+=1
        print candidatesconsidered
        W=wg.WGraph([c[0][2],c[0][3]],simplified=True)
        try:
            if not heegaard.is_realizable([c[0][2]()]):
                nongeomcurve+=1
                continue
        except RuntimeError, InputError:
            heegaardfailed=True
        try:
            if not heegaard.is_realizable([c[0][3]()]):
                nongeomcurve+=1
                continue
        except RuntimeError, InputError:
            heegaardfailed=True
        prses=prod([factorial(W.valence(i)-1) for i in range(1,1+W.rank)])
        if heegaardfailed:
            try:
                provisionalcandidates1[prses].append(c)
            except KeyError:
                provisionalcandidates1[prses]=[c]
            continue
        else:
            try:
                thescl=scl(c[0][2],c[0][3])
            except RuntimeError:
                try:
                    provisionalcandidates2[prses].append(c)
                except KeyError:
                    provisionalcandidates2[prses]=[c]
                continue
            if thescl==0:
                scl0+=1
                continue
            try:
                candidates[prses].append(c)
            except KeyError:
                candidates[prses]=[c]
    print str(candidatesconsidered)+" candidates considered."
    print str(nongeomcurve)+" rejected for u or v not realizable."
    print str(scl0)+" rejected for scl=0."

