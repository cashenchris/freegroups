from __future__ import division
from numpy import sign
import random
import copy
from fractions import gcd
from numpy import sqrt
from group import *
from freegroup import *


# some functions involving free groups




def ishomologicallytrivial(w):
    reorder = copy.copy(w.letters)
    reorder.sort()
    reorder = freereduce(reorder)
    if len(reorder)>0:
        return False
    else:
        return True

def randomcommutator(numgens,length,stopafter=10000):
    rndwd = randomword(numgens,length)
    for n in range(stopafter):
        if ishomologicallytrivial(rndwd):
            print('Found commutator on '+str(n)+'th try.')
            return rndwd
        else:
            rndwd = randomword(numgens,length)
    print('Failed to find commutator.')
    return []

def guessmean(numgens,length):
# Here's some experimental verification that the expected progress of
# a random walk of length n in a free group of rank k is about
# (1-1/k)n.  (Not quite right for small values of n.)
    result = []
    for n in range(100):
        result.append(randomword(numgens,length).letters)
    result = map(len,result)
    return sum(result)/100


def areConjugate(F,v,w):
    v1=copy.copy(F.cyclicReduce(v).letters)
    w1=copy.copy(F.cyclicReduce(w).letters)
    equal=False
    if len(v1)!=len(w1):
        return equal
    else:
        for i in range(len(v1)):
            if v1==w1:
                equal=True
                break
            temp = v1.pop()
            v1.insert(0, temp)
    return equal
FGFreeGroup.areConjugate=areConjugate
        
def isPower(F,v,w):
    """
    Decide if v is a power of w.
    """
    v1=copy.copy(v)
    w1=copy.copy(w)
    w1bar=w1**(-1)
    pos=F.word([])
    neg=F.word([])
    ispower=False
    while len(v1)>=len(pos):
        if v1==pos or v1==neg:
            ispower=True
            break
        pos=pos*w1
        neg=neg*w1bar
        
    return ispower
FGFreeGroup.isPower=isPower



def isConjugateInto(F,v, *wordlist, **kwargs):
    """
    Decide if v is conjugate into <w> for some w in wordlist. Use keyword 'withindex' to get also the index of the first word w in wordlist such that v is conjugate into <w>.
    """
    withindex=kwargs.pop('withindex',False)
    def isConjugateIntoOne(F,v,w):
        """
        Decide if v is conjugate into <w>.
        """
        v1=F.cyclicReduce(v)
        w1=F.cyclicReduce(w)
        if len(v1)==0:
            return True
        elif len(w1)==0:
            return False
        elif len(v1)%len(w1):
            return False
        else:
            return F.areConjugate(v1,w1.__pow__(len(v1)//len(w1))) or F.areConjugate(v1,w1.__pow__(-len(v1)//len(w1)))
    for i in range(len(wordlist)):
        if isConjugateIntoOne(F,v,wordlist[i]):
            if withindex:
                return True, i
            else:
                return True
    if withindex:
        return False, None
    else:
        return False
FGFreeGroup.isConjugateInto=isConjugateInto


def isSubword(F,v,w,orientable=True):
    """
    Decide if v is a subword of w.
    """
    lv = len(v.letters)
    lw = len(w.letters)
    if orientable:
        return any((v.letters == w.letters[i:i+lv]) for i in xrange(len(w.letters)-lv+1))
    else:
        vbackward=[i for i in reversed(v.letters)]
        return any((v.letters == w.letters[i:i+lv] or vbackward == w.letters[i:i+lv]) for i in xrange(len(w.letters)-lv+1))
FGFreeGroup.isSubword=isSubword

def abelianization(F,w):
    """
    Compute abelianzation of a word w in a free group F.
    """
    if len(w.letters)==0:
        return []
    else:
        powers=[0]*guessRank(w)
        lets=copy.copy(w.letters)
        while lets:
            l=lets.pop()
            powers[abs(l)-1]=powers[(abs(l)-1)]+sign(l)
        return powers
FGFreeGroup.abelianization=abelianization


    
