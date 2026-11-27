# Placeholder sound design for Act 1 (synthesised). Replaced/augmented once real VO + library SFX are in.
import numpy as np, wave, json, os
D=os.path.dirname(os.path.abspath(__file__)); SR=48000; DUR=17.5
tim=json.load(open(D+'/timings.json')); FZ=tim['freeze']; SH=FZ-12.3; DUR=17.5+SH
out=np.zeros(int(SR*DUR)+1)
def at(t,sig,g=1.0):
    i=int(t*SR); n=min(len(sig),len(out)-i); out[i:i+n]+=sig[:n]*g
def tt(d): return np.arange(int(d*SR))/SR
def lp(x,a=0.15):
    y=np.zeros_like(x); acc=0.0
    for i,v in enumerate(x): acc+=a*(v-acc); y[i]=acc
    return y
rng=np.random.default_rng(7)
# room tone until freeze
n=rng.standard_normal(int(SR*FZ)); out[:len(n)]+=lp(n,0.02)*0.004
# vibration buzzes (dot appears / stretches)
for t0,d in [(0.55,0.26),(1.0,0.32)]:
    x=tt(d); env=np.minimum(1,x/0.02)*np.minimum(1,(d-x)/0.04)
    s=np.tanh(3*np.sin(2*np.pi*170*x))*(0.6+0.4*np.sin(2*np.pi*31*x)); at(t0,lp(s*env,0.12),0.5)
# ring: two-note soft bell, synced to rings
for t0 in [2.38,2.98]:
    for k,(f,dt) in enumerate([(1046.5,0),(783.99,0.13)]):
        x=tt(0.9); env=np.exp(-x*5.5)*np.minimum(1,x/0.004)
        at(t0+dt,(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*f*2.01*x)+0.12*np.sin(2*np.pi*f*3.0*x))*env,0.12)
# hover tick + click
x=tt(0.012); at(3.37,rng.standard_normal(len(x))*np.exp(-x*900),0.05)
x=tt(0.04); at(3.555,(rng.standard_normal(len(x))*0.6+np.sin(2*np.pi*2300*x))*np.exp(-x*220),0.28)
# connect tone
for k,f in enumerate([659.3,987.8]):
    x=tt(0.16); at(3.74+k*0.1,np.sin(2*np.pi*f*x)*np.exp(-x*18)*np.minimum(1,x/0.005),0.13)
# freeze: soft low thump, then silence
x=tt(0.25); f=np.linspace(130,45,len(x)); at(FZ,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*14),0.35)
# tension tone under the line, rising into the shirt draw
T0=FZ+0.78; d=15.05+SH-T0+0.2; x=tt(d); f=196*2**(np.clip(x/d,0,1)*4/12)
ph=2*np.pi*np.cumsum(f)/SR; env=np.minimum(1,x/0.35)*np.minimum(1,(d-x)/0.25)
at(T0,(np.sin(ph)+0.35*np.sin(2*ph)+0.15*np.sin(3*ph))*env,0.07)
# whoosh as flames ripple up
d=0.55; x=tt(d); nz=rng.standard_normal(len(x)); a=np.linspace(0.02,0.35,len(x)); y=np.zeros_like(nz); acc=0
for i in range(len(nz)): acc+=a[i]*(nz[i]-acc); y[i]=acc
at(T0+1.62,y*np.sin(np.pi*x/d)**2,0.22)
# reverse swell into the drop
d=0.75; x=tt(d); nz=lp(rng.standard_normal(len(x)),0.25); at(16.2+SH-d,nz*(x/d)**3,0.35)
# DROP at 16.2: sub + log-drum style hit + click
x=tt(1.6); f=40+60*np.exp(-x*18); at(16.2+SH,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2.2),0.85)
x=tt(0.5); f=70+90*np.exp(-x*30); at(16.2+SH,np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-x*7),0.45)
x=tt(0.02); at(16.2+SH,rng.standard_normal(len(x))*np.exp(-x*300),0.3)
# logo lands on chest: soft tick
x=tt(0.05); at(17.28+SH,np.sin(2*np.pi*1800*x)*np.exp(-x*90),0.08)
out/=max(1e-9,np.abs(out).max()); out*=0.89
st=np.stack([out,out],1); pcm=(st*32767).astype('<i2')
w=wave.open(D+'/sfx_placeholder.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('sfx ok')
