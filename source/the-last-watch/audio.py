import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; T=50.0; n=int(SR*T); rng=np.random.default_rng(3)
mix=np.zeros((n,2))
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
def tt(d): return np.arange(int(d*SR))/SR
def put(sig,at,g=1.0,pan=0.0):
    i=int(at*SR); 
    if sig.ndim==1: sig=np.stack([sig*(1-max(0,pan)),sig*(1+min(0,pan))],1)
    m=min(len(sig),n-i); mix[i:i+m]+=sig[:m]*g
def env_lin(points, d):  # piecewise-linear envelope over d seconds
    x=tt(d); xs=[p[0] for p in points]; ys=[p[1] for p in points]; return np.interp(x,xs,ys)
# --- drone (A1 + E2, slowly beating), whole piece with automation
x=tt(T)
drone=(np.sin(2*np.pi*55*x)+0.18*np.sin(2*np.pi*55.15*x)+0.4*np.sin(2*np.pi*82.4*x)+0.25*np.sin(2*np.pi*110.3*x))
drone=lp(np.tanh(drone*0.8),400)
dr_env=env_lin([(0,0),(1.0,0.0),(3,0.35),(14,0.4),(22,0.5),(30,0.7),(37.4,0.7),(37.5,0.0),(39.5,0.0),(42,0.25),(44,0.3),(47,0.2),(50,0)],T)
put(drone*dr_env,0,0.5)
# --- wind (filtered noise, gusting)
wn=rng.normal(0,1,n); gust=0.6+0.4*np.sin(2*np.pi*0.09*x)*np.sin(2*np.pi*0.031*x+1)
wind=np.stack([bp(wn,250,1400)*gust, bp(np.roll(wn,977),250,1400)*gust],1)
w_env=env_lin([(0,0),(5.5,0.0),(6.5,0.5),(14,0.45),(14.3,0.15),(22,0.25),(30,0.35),(30.1,0.1),(37.6,0.1),(38,0.55),(40,0.4),(44,0.15),(47,0.3),(50,0)],T)
put(wind*w_env[:,None],0,0.22)
# --- match strike + flame ignite
strike=hp(rng.normal(0,1,int(0.35*SR)),1800)*np.exp(-tt(0.35)*14); crack=(rng.random(int(0.35*SR))<0.004)*rng.normal(0,1,int(0.35*SR))
put(strike*0.6+crack*0.8,1.38,0.7)
whoosh=lp(rng.normal(0,1,int(1.2*SR)),900)*env_lin([(0,0),(0.15,1),(1.2,0)],1.2); put(whoosh,1.45,0.45)
put(whoosh,39.3,0.5)
# --- distant bell (inharmonic partials)
def bell(f0,d=6.0):
    y=tt(d); s=sum(a*np.sin(2*np.pi*f0*r*y)*np.exp(-y*dk) for r,a,dk in [(0.5,0.6,0.5),(1,1,0.8),(1.19,0.5,1.1),(1.56,0.4,1.4),(2.0,0.35,1.6),(2.74,0.25,2.4),(3.76,0.15,3)])
    return s*np.minimum(1,y/0.004)
put(lp(bell(294),2500),9.0,0.10,0.3); put(lp(bell(294),2500),12.4,0.07,0.3)
# --- heartbeat pulse
def thump(f=50,d=0.35): y=tt(d); return np.sin(2*np.pi*f*y*(1+0.6*np.exp(-y*30)))*np.exp(-y*12)
beat=14.6; gap=1.0
while beat<30:
    g=0.35+0.4*(beat-14.6)/15
    put(thump(),beat,g); put(thump(44),beat+0.22,g*0.7)
    gap=1.0 if beat<22 else max(0.6,1.0-(beat-22)*0.06); beat+=gap
# --- match-cut whoosh (lantern -> moon)
mc=bp(rng.normal(0,1,int(1.0*SR)),300,3000)*env_lin([(0,0),(0.7,1),(0.78,0)],1.0); put(mc,18.9,0.35)
# --- string pad (detuned saws, lowpassed)
def saw(f,y): return 2*((f*y)%1)-1
def pad(freqs,d,cut=900,att=1.5,rel=2.0):
    y=tt(d); s=sum(saw(f*(1+dt),y) for f in freqs for dt in (-0.004,0,0.005))/(3*len(freqs))
    s=lp(s,cut,2); e=np.minimum(1,y/att)*np.minimum(1,(d-y)/rel); return s*e
put(pad([73.42,110,146.83,174.61],8.4,700),22.0,0.45)   # D minor, low
# --- riser 26 -> 30
y=tt(4.0); rs=bp(rng.normal(0,1,len(y)),400,6000)*(y/4)**2.2; tone=np.sin(2*np.pi*np.cumsum(110+330*(y/4)**2)/SR)*(y/4)**2
put(rs*0.6+tone*0.35,26.0,0.6)
# --- hits (30–37) with low ostinato
def hit(big=1.0,d=1.6):
    y=tt(d); sub=np.sin(2*np.pi*48*y*(1+1.5*np.exp(-y*20)))*np.exp(-y*3.2)
    crack=hp(rng.normal(0,1,len(y)),1200)*np.exp(-y*26)
    metal=sum(np.sin(2*np.pi*f*y)*np.exp(-y*dk) for f,dk in [(212,6),(347,7),(523,9),(811,11)])*0.18
    return (sub*1.0+crack*0.45*big+metal*big)
for c in [30.0,31.0,31.5,32.5,33.0,34.0,34.5,35.5,36.0,36.5,37.0]: put(hit(1.0 if c in (30.0,31.0,32.5,34.0,37.0) else 0.6),c,0.42)
put(lp(bell(220,4),3000),31.5,0.18,-0.2); put(lp(bell(220,4),3000),36.0,0.22,0.2)
ost=0.0
for k in range(int(7.4/0.25)):
    at=30+k*0.25; f=73.42 if (k//4)%2==0 else 69.3
    y=tt(0.22); s=lp(saw(f,y),500)*np.exp(-y*9); put(s,at,0.22)
# --- swell 40 -> 44 (D major, hopeful), then low hit at the title
put(pad([73.42,146.83,185.0,220,293.66,369.99],8.0,1600,att=2.8,rel=3.0),39.8,1.5)
put(hit(0.3,3.5),47.0,0.7)
# --- ember crackle while the title builds
cr=(rng.random(int(4.5*SR))<0.0016)*rng.normal(0,1,int(4.5*SR)); cr=hp(cr,2500)*env_lin([(0,0),(0.5,1),(3.5,0.8),(4.5,0)],4.5); put(cr,44.1,0.5)
# --- reverb
ir_t=tt(2.6); ir=rng.normal(0,1,(len(ir_t),2))*np.exp(-ir_t*2.6)[:,None]; ir[:,0]=lp(ir[:,0],5000); ir[:,1]=lp(ir[:,1],5000)
wet=np.stack([fftconvolve(mix[:,c],ir[:,c])[:n] for c in (0,1)],1); wet/=np.max(np.abs(wet))+1e-9
out=mix/ (np.max(np.abs(mix))+1e-9) + 0.22*wet
out=np.tanh(out*1.2); out/=np.max(np.abs(out))*1.1
fade=np.ones(n); k=int(0.8*SR); fade[-k:]=np.linspace(1,0,k); out*=fade[:,None]
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
