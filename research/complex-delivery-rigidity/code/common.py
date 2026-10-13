"""F2^9 frame helpers shared by the scripts (same conventions as the pinned words: a frame is a reduced basis tuple)."""
def basis(vs):
    b={}
    for x in vs:
        for p in sorted(b,reverse=True):
            if x>>p&1:x^=b[p]
        if x:
            p=x.bit_length()-1
            for q in b:
                if b[q]>>p&1:b[q]^=x
            b[p]=x
    return tuple(b[p]for p in sorted(b,reverse=True))
def inside(a,b):return basis(list(a)+list(b))==tuple(b)
def hyper(p):return basis([x for x in range(1,512)if(x&p).bit_count()%2==0])
