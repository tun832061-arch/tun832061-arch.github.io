# Original amapiano-style instrumental (fully synthesised here, so no licence issues).
import numpy as np
SR=48000; BPM=112; B=60/BPM
rng=np.random.default_rng(11)
def tt(d): return np.arange(int(d*SR))/SR
def nf(m): return 440*2**((m-69)/12)
CH=[[57,60,64,67],[53,57,60,64],[50,53,57,60,64],[52,55,59,62]]   # Am7 Fmaj7 Dm9 Em7
ROOT=[45,41,38,40]
def render(total, t0, t1):
    out=np.zeros(int(total*SR)); 
    def at(t,sig,g):
        i=int(t*SR); n=min(len(sig),len(out)-i)
        if n>0 and i>=0 and t<t1: out[i:i+n]+=sig[:n]*g
    nbar=int((t1-t0)/(4*B))+1
    kicks=[]
    for bar in range(nbar):
        tb=t0+bar*4*B; c=bar%4
        # pad (additive saw-ish, slow attack)
        d=4*B; x=tt(d); env=np.minimum(1,x/0.35)*np.minimum(1,(d-x)/0.25)
        pad=np.zeros_like(x)
        for m in CH[c]:
            for det in (-0.08,0.08):
                f=nf(m+det)
                for h in range(1,6): pad+=np.sin(2*np.pi*f*h*x+rng.random()*6)/h**1.6
        at(tb,pad*env,0.012)
        # keys stabs (rhodes-like) on syncopated 16ths
        for pos in (0.5,1.75,2.5,3.25):
            x=tt(0.45); s=np.zeros_like(x)
            for m in CH[c][-3:]:
                f=nf(m+12); s+=np.sin(2*np.pi*f*x)+0.35*np.sin(2*np.pi*2*f*x)*np.exp(-x*20)
            at(tb+pos*B,s*np.exp(-x*7)*np.minimum(1,x/0.003),0.035)
        # log drum bassline
        for pos,iv in ((0,0),(0.75,0),(1.5,7),(2.5,12),(3.0,0),(3.25,7)):
            x=tt(0.42); f=nf(ROOT[c]+iv)*(1+0.5*np.exp(-x*28))
            at(tb+pos*B,np.tanh(1.8*np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-x*6.5),0.26)
        for beat in range(4):
            t=tb+beat*B
            # kick
            x=tt(0.3); f=48+110*np.exp(-x*45); at(t,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*10),0.42); kicks.append(t)
            # shaker 16ths with swing
            for s in range(4):
                x=tt(0.06); nz=np.diff(np.r_[0,rng.standard_normal(len(x))])
                at(t+s*B/4+(0.018 if s%2 else 0),nz*np.exp(-x*(70 if s%2 else 110)),0.045 if s%2 else 0.03)
            # rim on 2 & 4
            if beat in (1,3):
                x=tt(0.08); at(t,(np.diff(np.r_[0,rng.standard_normal(len(x))])*0.6+np.sin(2*np.pi*1700*x))*np.exp(-x*55),0.07)
        # open hat on the "and" of 4
        x=tt(0.25); at(tb+3.5*B,np.diff(np.r_[0,rng.standard_normal(len(x))])*np.exp(-x*12),0.03)
    # gentle sidechain pump from the kick
    g=np.ones_like(out)
    for k in kicks:
        i=int(k*SR); n=int(0.18*SR)
        if i<len(g): seg=g[i:i+n]; seg*=1-0.45*np.exp(-np.arange(len(seg))/SR*18)
    out*=g; out[int(t1*SR):]=0
    # fade the last 40ms at the cut
    i=int(t1*SR); n=int(0.04*SR); out[max(0,i-n):i]*=np.linspace(1,0,min(n,i))
    return out
