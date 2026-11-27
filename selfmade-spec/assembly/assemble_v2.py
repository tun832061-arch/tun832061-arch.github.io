# Full film v2: Act1 (0-17.5) + continuous Act2 (17.5-41.0) + placeholder soundtrack synced to Act2 events.
import numpy as np, subprocess, os, wave, math
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(D)
import json
CJ=json.load(open(R+'/vo/cta.json')); G=CJ['G']; DUR=CJ['total']; SR=48000; SH=G-17.5
T=dict(spin=(1.75,8.2),flip0=4.7,expand=8.2,iris=10.3,type0=10.9,swap=13.55,merge=15.55,cta0=16.3,end0=19.3)
B=60/112
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','/dev/stdin','-c','copy',D+'/_video.mp4'],
  input=f"file '{R}/act1/act1_silent.mp4'\nfile '{R}/act2/act2_silent.mp4'\n".encode(),check=True)
out=np.zeros(int(SR*DUR)); rng=np.random.default_rng(5)
def at(t,sig,g=1.0,buf=None):
    b=out if buf is None else buf; i=int(t*SR); n=min(len(sig),len(b)-i)
    if n>0 and i>=0: b[i:i+n]+=sig[:n]*g
def tt(d): return np.arange(int(d*SR))/SR
def smooth(x,k): return np.convolve(x,np.ones(k)/k,'same')
def whoosh(t,d=0.35,g=0.15,k=10):
    x=tt(d); at(t-d/2,smooth(rng.standard_normal(len(x)),k)*np.sin(np.pi*x/d)**2,g)
def swell(t_end,d=0.7,g=0.25):
    x=tt(d); at(t_end-d,smooth(rng.standard_normal(len(x)),6)*(x/d)**3,g)
def sub(t,g=0.6,dec=2.5,f0=40,f1=60):
    x=tt(1.4); f=f0+f1*np.exp(-x*18); at(t,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*dec),g)
def tick(t,f=1800,g=0.07):
    x=tt(0.05); at(t,np.sin(2*np.pi*f*x)*np.exp(-x*90),g)
def tone2(t,fs,g=0.1,gap=0.13,dec=6):
    for k,f in enumerate(fs):
        x=tt(0.7); at(t+k*gap,(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*f*2.01*x))*np.exp(-x*dec)*np.minimum(1,x/0.004),g)
w=wave.open(R+'/act1/sfx_placeholder.wav'); a1=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2)[:,0]/32768.0
out[:len(a1)]+=a1*0.9
L=lambda x:G+x
# crossing + tile fold
whoosh(L(0.45),0.6,0.14,14); whoosh(L(1.35),0.5,0.12)
# card passes (every 72deg of a 720deg sine-eased spin)
s0,s1=T['spin']
for k in range(1,9):
    lo,hi=0.0,1.0
    for _ in range(40):
        m=(lo+hi)/2; th=648*(-(math.cos(math.pi*m)-1)/2)
        lo,hi=(m,hi) if th<k*72 else (lo,m)
    whoosh(L(s0+(s1-s0)*lo),0.3,0.09)
for i in range(5): tick(L(T['flip0']+0.22*i+0.3),1200,0.05)
whoosh(L(T['expand']+0.25),0.55,0.18)
swell(L(T['type0']),0.5,0.2)
b0=T['type0']
sub(L(b0+0.05+2*B),0.55)          # FIT. lands
whoosh(L(T['swap']+0.2),0.4,0.14)  # FIT -> STYLE
for i in range(7): tick(L(b0+0.3+0.14*i),1500+120*i,0.05)
swell(L(T['merge']+0.3),0.6,0.22); tick(L(T['merge']+0.3),900,0.1)
tone2(L(T['cta0']+0.15),[1046.5,783.99],0.09)
sub(L(T['cta0']+[c['o'] for c in CJ['cta'] if c['w']=='now!'][0]),0.6,3); 
tone2(L(T['end0']+0.35),[659.3,493.9],0.12,0.22,4)
swell(L(T['end0']+1.9),0.7,0.25); sub(L(T['end0']+1.9),0.7,2)
# original instrumental from the drop to "call ended"
import sys as _s; _s.path.insert(0,D); from music import render as _mus
tend=L(T['end0']+0.35); t0=16.2+SH
music=_mus(DUR,t0,tend)
music[int(tend*SR):]=0
duck=np.ones_like(music); duck[int(L(T['cta0'])*SR):int(L(T['end0'])*SR)]=0.45
out+=music*duck*1.5
import sys
VARIANT=sys.argv[1] if len(sys.argv)>1 else 'main'
w=wave.open(R+('/vo/vo_track_portfolio.wav' if VARIANT=='portfolio' else '/vo/vo_track.wav')); vo=np.frombuffer(w.readframes(w.getnframes()),'<i2')/32768.0
n=min(len(vo),len(out)); out*=0.62; out[:n]+=vo[:n]*1.0
out/=np.abs(out).max(); out*=0.89
pcm=(np.stack([out,out],1)*32767).astype('<i2')
w=wave.open(D+'/_audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',D+'/_video.mp4','-i',D+'/_audio.wav','-c:v','copy','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','192k','-shortest',D+('/animatic_v7_portfolio.mp4' if VARIANT=='portfolio' else '/animatic_v7.mp4')],check=True)
print('ok')
