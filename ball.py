import whiteheadgraph.split.split

def Spheres(F,k):
    """
    Dict with keys 0..k whose i-th entry is the list of unique words of length i in F.
    """
    assert(k>=0)
    Spheres=dict()
    Spheres[0]=[F.word([])]
    if k:
        Spheres[1]=[F.word([i]) for i in range(1,F.rank+1)]+[F.word([-i]) for i in range(1,F.rank+1)]
        for i in range(2,1+k):
            Spheres[i]=[]
            for w in Spheres[i-1]:
                for j in range(1,F.rank+1):
                    if w.letters[-1]!=-j:
                        Spheres[i].append(F.word(w.letters+[j]))
                    if w.letters[-1]!=j:
                        Spheres[i].append(F.word(w.letters+[-j]))
    return Spheres

def RootConjugacyClasses(F,k,spheres=None):
    """
    Dict with keys 0..k whose i-th entry is the list of unique indivisible words of length i in F that are shortlex minimal in their conjugacy class.
    """
    if spheres:
        S=spheres
    else:
        S=Spheres(F,k)
    RCC=dict()
    RCC[0]=S[0]
    RCC[1]=[F.word([i]) for i in range(1,F.rank+1)]
    for i in range(2,1+k):
        RCC[i]=[]
        for w in S[i]:
            rcc=F.conjugateRoot(w)
            if rcc==w:
                RCC[i].append(w)
    return RCC



def Primitives(F,k,rcc=None):
    """
    Dict with keys 0..k whose i-th entry is the list of primitive words of length i in F that are shortlex minimal in their conjugacy class.
    """
    Primitives=dict()
    if rcc:
        RCC=rcc
    else:
        RCC=RootConjugacyClasses(F,k)
    Primitives[1]=RCC[1]
    for i in range(2,1+k):
        Primitives[i]=[]
        for w in RCC[i]:
            if F.isPrimitive(w):
                Primitives[i].append(w)
    return Primitives
    

def xprim(F,j,k):
    """
    Generator for primitive of length at least j and at most k-1 that are shortlex minimal among conjugates and inverses.
    """
    n=F.rank
    def increment(l,i):
        if l[i]==-1:
            l[i]=1
        elif l[i]!=n:
            l[i]=l[i]+1
        else:# reset and carry 1
            l[i]=-n
            if len(l)==i+1:
                l.append(-n)
            else:
                increment(l,i+1)
    letters=[-n]*(j)
    w=F.word(letters)
    rcc=F.conjugateRoot(w)
    while ((not letters==rcc.letters) or (not F.isPrimitive(rcc))) and len(letters)<k:
            increment(letters,0)
            w=F.word(letters)
            rcc=F.conjugateRoot(w)
    while len(letters)<k:
        yield w
        increment(letters,0)
        w=F.word(letters)
        rcc=F.conjugateRoot(w)
        while ((not letters==rcc.letters) or (not F.isPrimitive(rcc))) and len(letters)<=k:
            increment(letters,0)
            w=F.word(letters)
            rcc=F.conjugateRoot(w)
        
        
