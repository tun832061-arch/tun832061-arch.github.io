import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; T=50.0; n=int(SR*T); rng=np.random.default_rng(11); mix=np.zeros((n,2))
def tt(d): return np.arange(int(d*SR))/SR
def lp(x,f): return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def bp(x,a,b): return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
def put(s,at,g=1.0,pan=0.0):
    i=int(at*SR); m=min(len(s),n-i)
    if m<=0: return
    mix[i:i+m,0]+=s[:m]*g*(1-max(0,pan)); mix[i:i+m,1]+=s[:m]*g*(1+min(0,pan))
def mtof(m): return 440*2**((m-69)/12)
def pluck(f,d=0.45,bright=1.0):
    y=tt(d); s=np.sin(2*np.pi*f*y)+0.5*np.sin(4*np.pi*f*y)*np.exp(-y*14)+0.25*np.sin(6*np.pi*f*y)*np.exp(-y*20)
    return s*np.exp(-y*(7/bright))*np.minimum(1,y/0.003)
def kick(): y=tt(0.35); return np.sin(2*np.pi*np.cumsum(50+120*np.exp(-y*30))/SR)*np.exp(-y*10)
def clap():
    d=0.25; x=rng.normal(0,1,int(d*SR)); e=np.zeros(len(x))
    for o in (0,0.011,0.022): e+=np.exp(-np.maximum(0,tt(d)-o)*60)*(tt(d)>=o)
    return bp(x,900,4000)*e*0.5
def shaker(): x=rng.normal(0,1,int(0.08*SR)); return hp(x,6000)*np.exp(-tt(0.08)*45)*0.18
def blip(f,d=0.12): y=tt(d); return np.sin(2*np.pi*f*y*(1+0.3*np.exp(-y*40)))*np.exp(-y*30)
def pop_(f=900): y=tt(0.1); return np.sin(2*np.pi*np.cumsum(f*(1+2*np.exp(-y*60)))/SR)*np.exp(-y*40)
def tick(): y=tt(0.03); return hp(rng.normal(0,1,len(y)),3000)*np.exp(-y*200)*0.6
def whoosh(d=0.4): x=rng.normal(0,1,int(d*SR)); e=np.sin(np.pi*tt(d)/d)**2; return bp(x,500,5000)*e*0.4
def chime(f): return pluck(f,1.2,3.0)*0.6+pluck(f*2,1.2,3.0)*0.25
B=0.5
# --- chords: C G Am F (two bars each = 4 beats of 0.5 s)
prog=[[60,64,67],[55,59,62,67],[57,60,64],[53,57,60,65]]; bass=[36,31,33,29]
for bar in range(int(T/(4*B))):
    at=bar*4*B; ch=prog[bar%4]; full = 6.0<=at<46.0
    for step in range(8):  # eighth-note pluck arpeggio
        st=at+step*B/2
        if st>=T: break
        if not full and step%2: continue
        note=ch[[0,1,2,1,0,2,1,2][step]%len(ch)]+12
        put(pluck(mtof(note),0.35),st,0.16 if full else 0.12,(-0.3 if step%2 else 0.3))
    if full:
        for b in range(4):
            bt=at+b*B
            put(kick(),bt,0.55 if b in (0,2) else 0.0)
            if b in (1,3): put(clap(),bt,0.55)
            for s in range(4): put(shaker(),bt+s*B/4,0.6 if s%2 else 0.35)
        put(lp(np.tanh(2*np.sin(2*np.pi*mtof(bass[bar%4])*tt(1.9)))*np.minimum(1,tt(1.9)/0.02)*np.exp(-tt(1.9)*0.6),300),at,0.12)
# --- UI sound design
put(bp(rng.normal(0,1,int(1.2*SR)),1500,7000)*np.exp(-tt(1.2)*2)*0.25,0.2,1.0)       # receipt unroll
for k in range(int(4.0/0.07)): put(tick(),1.6+k*0.07,0.25,0.3*np.sin(k))          # numbers scrambling
for i in range(4): put(pop_(700+i*120),1.8+i*0.15,0.5)
for i in range(4): put(pop_(1300),3.0+i*0.2,0.3)
put(whoosh(0.6),5.55,0.8); put(kick(),6.3,0.7); put(chime(mtof(84)),6.8,0.45); put(chime(mtof(91)),6.85,0.25)
# camera + shutter
sh=hp(rng.normal(0,1,int(0.12*SR)),2000)*np.exp(-tt(0.12)*50); put(sh,13.5,0.7); put(blip(2200,0.05),13.5,0.3)
for i in range(6): put(whoosh(0.25),14.0+i*0.12,0.25); put(blip(mtof(72+i*2)),14.25+i*0.12,0.25)
put(whoosh(0.3),16.2,0.3)
tap={'A':76,'B':79,'C':81,'D':84}
for t0,i,pid in [(17.2,0,"A"),(17.7,1,"B"),(18.2,2,"C"),(18.7,3,"D"),(19.4,4,"A"),(19.65,4,"B"),(19.9,4,"C"),(20.15,4,"D"),(20.9,5,"A"),(21.3,5,"C")]:
    put(pop_(600),t0+0.02,0.2); put(blip(mtof(tap[pid])),t0+0.3,0.35)
# totals counting, toggle, donut, button
for i in range(4):
    for k in range(14): put(tick(),24.7+i*0.2+k*0.075,0.2)
    put(blip(mtof(88)),25.8+i*0.2,0.2)
put(blip(1800,0.05),26.6,0.4); put(whoosh(1.2),27.6,0.5); put(pop_(500),29.4,0.5); put(pop_(900),31.5,0.4)
# notifications + paid chimes
for i in range(4): put(chime(mtof(88)),34.6+i*0.45,0.25); put(chime(mtof(95)),34.62+i*0.45,0.12)
for i,m in enumerate([72,76,79,84]): put(chime(mtof(m)),37.4+i*0.6,0.4)
# end: logo hit + badges
put(whoosh(0.6),42.0,0.6); put(kick(),42.7,0.8)
for m in [60,64,67,72,76]: put(pluck(mtof(m),2.5,4),42.7,0.18)
put(pop_(800),44.4,0.4); put(pop_(950),44.52,0.4)
# --- light room reverb + master
ir=rng.normal(0,1,(int(1.2*SR),2))*np.exp(-tt(1.2)*5)[:,None]
wet=np.stack([fftconvolve(mix[:,c],lp(ir[:,c],6000))[:n] for c in (0,1)],1)
out=mix/np.max(np.abs(mix)) + 0.12*wet/np.max(np.abs(wet))
out=np.tanh(out*1.3); out/=np.max(np.abs(out))*1.1
f=np.ones(n); k=int(1.0*SR); f[-k:]=np.linspace(1,0,k); out*=f[:,None]
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
