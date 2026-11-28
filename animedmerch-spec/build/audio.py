# Original anime-phonk score + SFX for the Animedmerch spec (fully synthesised, no samples).
import numpy as np, wave
SR=48000; B=60/140; DROP=3.0
T=dict(drop=DROP,freeze=DROP+16*B,title=DROP+22*B,manga=DROP+29*B,cta=DROP+45*B,end=DROP+50*B,total=28.6)
PG=[T['manga'],T['manga']+16*B/3,T['manga']+32*B/3]
rng=np.random.default_rng(3); out=np.zeros(int(T['total']*SR)+SR)
def tt(d): return np.arange(int(d*SR))/SR
def at(t,s,g=1.0):
    i=int(t*SR); n=min(len(s),len(out)-i)
    if n>0 and i>=0: out[i:i+n]+=s[:n]*g
def nf(m): return 440*2**((m-69)/12)
def noise(n): return rng.standard_normal(n)
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def koto(m,d=1.6):
    x=tt(d); f=nf(m)*(1+0.012*np.exp(-x*25)); ph=2*np.pi*np.cumsum(f)/SR; s=np.zeros_like(x)
    for h in range(1,9): s+=np.sin(h*ph)*np.exp(-x*(2.2+h*1.6))/h**0.9
    return s*np.minimum(1,x/0.002)
def taiko(g=1):
    x=tt(1.2); f=55+70*np.exp(-x*20); return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*4)+lp(noise(len(x)),6)*np.exp(-x*30)*0.5)*g
def impact():
    x=tt(0.9); f=45+90*np.exp(-x*25); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*5)+noise(len(x))*np.exp(-x*40)*0.35
def whoosh(d=0.25):
    x=tt(d); return lp(noise(len(x)),10)*np.sin(np.pi*x/d)**2
def riser(d):
    x=tt(d); return lp(noise(len(x)),4)*(x/d)**3
HIRA=[57,59,60,64,65,69,71,72,76,77]   # A hirajoshi
# ---- cold open: drone + koto phrase + ikuzo riser
x=tt(DROP); at(0,(np.sin(2*np.pi*55*x)+0.4*np.sin(2*np.pi*82.4*x))*np.minimum(1,x/0.8)*0.12)
for t0,m in [(0.15,76),(0.55,72),(0.95,71),(1.35,69),(1.9,64),(2.15,65),(2.35,69)]: at(t0,koto(m),0.22)
at(2.6-0.0,taiko(),0.6); at(DROP-0.8,riser(0.8),0.3)
# ---- phonk beat
def cowbell(m,d=0.22):
    x=tt(d); f=nf(m); s=np.sign(np.sin(2*np.pi*f*x))*0.6+np.sign(np.sin(2*np.pi*f*1.48*x))*0.4
    return lp(s,3)*np.exp(-x*14)
COW=[(0,81),(0.75,81),(1.5,84),(2.0,83),(2.5,81),(3.0,79),(3.5,76)]
BASS=[(0,45),(1.5,45),(2.5,48),(3.0,43)]
def beat_section(t0,t1,cow=True):
    nb=int(round((t1-t0)/B))
    for b in range(nb):
        t=t0+b*B; bar=b//4; pos=b%4
        if pos in (0,) or (pos==2 and bar%2==1):
            x=tt(0.25); f=50+120*np.exp(-x*40); at(t,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*12),0.55)
        if pos==2:
            x=tt(0.25); at(t,(lp(noise(len(x)),2)*0.7+np.sin(2*np.pi*190*x)*0.4)*np.exp(-x*16),0.32)
        for s in range(2):
            x=tt(0.04); at(t+s*B/2,np.diff(np.r_[0,noise(len(x))])*np.exp(-x*120),0.06)
        if pos==3 and bar%2==1:
            for s in range(6): x=tt(0.03); at(t+s*B/6,np.diff(np.r_[0,noise(len(x))])*np.exp(-x*150),0.05)
    nbar=nb//4
    for bar in range(nbar):
        tb=t0+bar*4*B
        for i,(p,m) in enumerate(BASS):
            d=(BASS[i+1][0] if i+1<len(BASS) else 4)-p; x=tt(d*B); f=nf(m-12)*(1+0.3*np.exp(-x*30))
            if i==3: f=f*2**((-2/12)*np.clip(x/(d*B),0,1))
            at(tb+p*B,np.tanh(2.2*np.sin(2*np.pi*np.cumsum(f)/SR))*np.minimum(1,x/0.005)*np.exp(-x*0.8),0.32)
        if cow:
            for p,m in COW: at(tb+p*B,cowbell(m),0.11)
        if bar%2==0:
            for k,p in enumerate((0.5,1.25,2.75)): at(tb+p*B,koto(HIRA[(bar+k*3)%len(HIRA)]+12,0.9),0.09)
beat_section(DROP,T['freeze'])
# piece hits
for i in range(8): at(DROP+i*2*B-0.12,whoosh(),0.18); at(DROP+i*2*B,impact(),0.32 if i else 0.6)
# freeze: tape stop, glass crack, drone
x=tt(0.5); f=110*np.linspace(1,0.1,len(x)); at(T['freeze'],np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR))*np.linspace(1,0,len(x)),0.3)
x=tt(0.6); at(T['freeze']+0.03,np.diff(np.r_[0,noise(len(x))])*np.exp(-x*9)*(1+np.sin(2*np.pi*3800*x)*0.3),0.25)
d=T['title']-T['freeze']; x=tt(d); at(T['freeze'],np.sin(2*np.pi*41.2*x)*np.minimum(1,x/0.4)*0.16)
for k,m in enumerate([69,65,64,60,59,57]): at(T['freeze']+0.6+k*0.32,koto(m,2.0),0.16)
at(T['title']-0.9,riser(0.9),0.3)
# title: taiko + gong-ish
at(T['title'],taiko(),0.9); at(T['title']+0.95,taiko(),0.6)
x=tt(2.5); at(T['title'],sum(np.sin(2*np.pi*f*x)*np.exp(-x*k) for f,k in [(110,1.2),(163,1.5),(247,2),(371,2.6)])*0.12)
for k,m in enumerate([57,60,64,69,72]): at(T['title']+1.3+k*0.12,koto(m),0.15)
# manga pages
beat_section(T['manga'],T['end'])
for p in PG: at(p-0.25,whoosh(0.35),0.25)
# CTA slams
c0=T['cta']
for i in range(6): at(c0+0.1+i*B/2,impact()[:int(0.3*SR)],0.18)
sw=c0+0.1+3*B+0.1
for i in range(2): at(sw+i*B/2,impact()[:int(0.3*SR)],0.2)
at(sw+B+0.05,impact(),0.6); at(sw+B+0.05,taiko(),0.6)
# end: logo hit, then "to be continued" sting
at(T['end'],taiko(),0.5)
tb=T['end']+1.6
for k,m in enumerate([57,64,69,72,76]): at(tb+k*0.05,koto(m,2.5),0.18)
x=tt(1.8); at(tb,sum(np.sin(2*np.pi*nf(m)*x) for m in (45,52,57))*np.exp(-x*1.6)*0.1)
out/=np.abs(out).max(); out*=0.9
pcm=(np.stack([out,out],1)*32767).astype('<i2')
w=wave.open('score.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('score ok',round(T['total'],2))
