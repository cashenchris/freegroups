import itertools

def generate_words(rank,maxlen,startlength=1,reversed=True):
    """
    Generator of unique, non-trivial words in a free group of given rank,  up to length maxlen. Words returned as list of non-zero integers, with 1 corresponding to first generator, -1 its inverse, etc.
    """
    letters=[-x for x in range(rank,0,-1)]+[x for x in range(1,1+rank)]
    counters=dict()
    for i in range(startlength):
        counters[i]=0
    maxindex=startlength-1
    theletters=[letters[counters[i]] for i in range(maxindex+1)]
    while maxindex<maxlen:
        if reversed:
            yield theletters[::-1]
        else:
            yield theletters
        maxindex=maxindex+nextword(rank,counters,letters,maxindex)
        theletters=[letters[counters[i]] for i in range(maxindex+1)]

def generate_ordered(rank,maxlen,startlength=1):
    """
    Generate words with the restirciton that first letter is 1, second letter to appear is 2, first letter after +-1,+-2 to appear is 3
    """
    gen=generate_words(rank,maxlen,startlength=startlength)
    for w in gen:
        if w[0]!=1:
            continue
        if all([x==1 for x in w]):
            yield w
        else:
            for firstnon1 in range(len(w)):
                if w[firstnon1]!=1:
                    break
            if w[firstnon1]!=2:
                continue
            else:
                if all([abs(x)<=2 for x in w]):
                    yield w
                else:
                    for firstnon12 in range(len(w)):
                        if abs(w[firstnon12])>2:
                            break
                    if w[firstnon12]>0:
                        yield w
                    else:
                        continue
                    

        
def advance_counter(thecounter,index,resetval):
    """
    Advance a big-endian counter. thecounter is a list of non-negative integers. index is index to be incremented by 1. resetval is number at which the place value should rollover and the next index should be incremented.
    Return value is largest index whose value changed.
    """
    thecounter[index]=(thecounter[index]+1)%resetval
    if thecounter[index]==0:
        if index+1 not in thecounter:
            thecounter[index+1]=0
            return index+1
        else:
            return advance_counter(thecounter,index+1,resetval)
    else:
        return index
    
def nextword(rank,counters,letters,maxindex,index=0):
    checkindex=advance_counter(counters,index,2*rank) # advance the counters at index and set checkindex to largest index that changed.
    if checkindex==maxindex+1: # length increased, no free reductions
        return 1
    elif checkindex<maxindex and letters[counters[checkindex]]+letters[counters[checkindex+1]]==0: # there is a forward free reduction, recurse
        return nextword(rank,counters,letters,maxindex,index=checkindex)
    elif checkindex>0 and letters[counters[checkindex]]+letters[counters[checkindex-1]]==0: # there is a backward free reduction, recurse
        return nextword(rank,counters,letters,maxindex,index=checkindex-1)
    else: # no free reduction or length increase
        return 0
        
def evaluate_word(word,elements,gpproduct=None,gpinverse=None):
    """
    Evaluate a word w in {1,-1,..,i,-i} by replacing 1 with group element elements[i], -1 with elements[1]^{-1}, etc.
    """
    if gpproduct:
        z=gpproduct(elements[0],gpinverse(elements[0]))
    else:
        z=elements[0]**0
    for i in range(len(word)):
        if word[i]>0:
            if gpproduct:
                z=gpproduct(z,elements[word[i]-1])
            else:
                z=z*elements[word[i]-1]
        else:
            if gpproduct:
                z=gpproduct(z,gpinverse(elements[-word[i]-1]))
            else:
                z=z*(elements[-word[i]-1]**(-1))
    return z
