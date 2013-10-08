from __future__ import division
from numpy import sign
import random
import copy
from fractions import gcd
from numpy import sqrt

key = 'ZYXWVUTSRQPONMLKJIHGFEDCBA abcdefghijklmnopqrstuvwxyz'
key_offset = 26


def freereduce(l):
    if len(l)<2:
        return l
    else:
        reduction=[l[0]]
        for i in range(len(l)-1):
            if reduction==[]:
                reduction=[l[i+1]]
            else:
                if reduction[-1]==-l[i+1]:
                    reduction.pop()
                else:
                    reduction.append(l[i+1])
    return reduction

def stringtolist(letters):
    """
    Convert some alphabetic word to a list of numbers.
    """
    if not letters.isalpha():
        return []
    return [key.find(letters[0])-key_offset]+stringtolist(letters[1:])

    

class word(object):
    """
    Word in the free group, together with function for evaluating word in
    some representation
    """
    # Primary representation is as a list of integers
    def __init__(self,letters):
        """
        Constructor takes a list of integers or string.
        
        Example: w = word([1,2,-1,-2]) followed by w([a,b]) returns
        the commutator abAB.

        Words can also be specified as strings
        of lower and upper case letters, e.g. word('abAB') returns the
        same thing as word([1,2,-1,-2]).
        """
        if type(letters)==word: # if the input is already a word this just copies it
            self.letters=[x for x in letters.letters]
        elif type(letters)==type([]):
            self.letters=freereduce(letters)
        elif type(letters)==type('') and letters.isalpha():
            self.letters=stringtolist(letters)
        else:
            print('WARNING:List of integers or alphabetic string expected, returning [].\n')
            self.letters=[]

    def __len__(self):
        return len(self.letters)

    def __repr__(self):
        return str(self.letters)

    def __mul__(self,other):
        return word(self.letters+other.letters)

    def __cmp__(self,other):
        " shortlex order "
        if self.letters == other.letters:
            return 0
        elif len(self.letters)!=len(other.letters):
            return len(self.letters)-len(other.letters)
        else:
            # This is probably too clever.  Also it might be better to order differently.
            return -2*int(self.letters<other.letters)+1

    def __pow__(self,n):
        # take n'th power
        result = word([])
        if n == 0:
            return result
        elif n>0:
            for i in range(n):
                result = result * self
            return result
        else:
            inverse = word(map(lambda x: -x, self.letters[::-1]))
            for i in range(-n):
                result = result * inverse
            return result

    def __call__(self,arg,one='Identity?'):
# The optional argument is so that an identity element of the target
# can be provided.
        if len(self.letters)==0:
            if type(one)==type(''):
                print 'Warning, returning string.'
            return one
        else:
            answer = arg[abs(self.letters[0])-1]**(sign(self.letters[0]))
            for letter in self.letters[1:]:
                answer = answer * arg[abs(letter)-1]**(sign(letter))
            return answer
    def pop(self):
        """
        Return first letter (as a number!), and shorten word.
        """
        first = self.letters[0]
        self.letters = self.letters[1:]
        return first

    def alpha(self):
        """
        Return word as string.
        """
        strout = ''
        for letter in self.letters:
            strout = strout+key[letter+key_offset]
        return strout

def randomword(numgens,length):
    letterlist = range(1,numgens+1)+range(-1,-(numgens+1),-1)
    letters = []
    for n in range(length):
        letters.append(random.choice(letterlist))
    return word(letters)

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




########   Here's some more stuff

def guessRank(*wordlist):
    """
    The highest generator appearing in wordlist.
    """
    rank=0
    for word in wordlist:
        rank=max(rank,max(abs(i) for i in word.letters))
    return rank

def freeReduce(w):
    return word(freereduce(w.letters))

def cyclicReduce(w):
    w1=copy.copy(w.letters)
    w1=freereduce(w1)
    while len(w1) > 2 and w1[0]+w1[-1]==0:
        w1=w1[1:-1]
    return word(w1)

def areConjugate(v,w):
    v1=copy.copy(cyclicReduce(v).letters)
    w1=copy.copy(cyclicReduce(w).letters)
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
        
def isPower(v,w):
    """
    Decide if v is a power of w.
    """
    v1=copy.copy(v)
    w1=copy.copy(w)
    w1bar=w1.__pow__(-1)
    pos=word([])
    neg=word([])
    ispower=False
    while len(v1)>=len(pos):
        if v1==pos or v1==neg:
            ispower=True
            break
        pos=pos*w1
        neg=neg*w1bar
        
    return ispower



def isConjugateInto(v, *wordlist, **kwargs):
    """
    Decide if v is conjugate into <w> for some w in wordlist. Use keyword 'withindex' to get also the index of the first word w in wordlist such that v is conjugate into <w>.
    """
    withindex=kwargs.pop('withindex',False)
    def isConjugateIntoOne(v,w):
        """
        Decide if v is conjugate into <w>.
        """
        v1=cyclicReduce(v)
        w1=cyclicReduce(w)
        if len(v1)==0:
            return True
        elif len(w1)==0:
            return False
        elif len(v1)%len(w1):
            return False
        else:
            return areConjugate(v1,w1.__pow__(len(v1)//len(w1))) or areConjugate(v1,w1.__pow__(-len(v1)//len(w1)))
    for i in range(len(wordlist)):
        if isConjugateIntoOne(v,wordlist[i]):
            if withindex:
                return True, i
            else:
                return True
    if withindex:
        return False, None
    else:
        return False


def isSubword(v,w,orientable=True):
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

def abelianization(w):
    """
    Compute abelianzation of a word w.
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

def maxRoot(w,uptoconjugacy=False):
    """
    Find an indivisible root of w.
    """
    w1=cyclicReduce(w)
    conjugator=word(w.letters[0:(len(w)-len(w1))//2])
    n=len(w1.letters)
    if n==0:
        return w
    else:
        abpowergcd=reduce(gcd,abelianization(w1))
        possiblerootlengths=[i for i in range(1,1+int(sqrt(n))) if (n%i==0 and abpowergcd%(n//i)==0) ]+[n//i for i in range(int(sqrt(n)),0,-1) if (n%i==0 and abpowergcd%i==0)]
        theroot=[]
        for i in possiblerootlengths:
            if w1.letters[0:i]*(n//i)==w1.letters:
                theroot=word(w1.letters[0:i])
                break
        if uptoconjugacy:
            return theroot
        else:
            return conjugator*theroot*conjugator**(-1)
    
