import numpy as np, wave, sys
SR=48000; BPM=120; B=60/BPM; T=32.0; n=int(SR*T); t=np.arange(n)/SR
out=np.zeros((n,2))
rng=np.random.default_rng(7)
def add(sig,at,gain=1.0,pan=0.0):
    i=int(at*SR); s=sig[:max(0,min(len(sig),n-i))]*gain
    out[i:i+len(s),0]+=s*(1-max(0,pan)); out[i:i+len(s),1]+=s*(1+min(0,pan))
def env(d,a=0.002,r=None):
    m=int(d*SR); e=np.ones(m); k=int(a*SR); e[:k]=np.linspace(0,1,k)
    e*=np.exp(-np.arange(m)/(SR*(r or d/4))); return e
def kick():
    d=.45; tt=np.arange(int(d*SR))/SR; f=45+110*np.exp(-tt*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(d,r=.12)*1.0
def snare():
    d=.3; return (rng.normal(0,1,int(d*SR))*.6+np.sin(2*np.pi*190*np.arange(int(d*SR))/SR)*.4)*env(d,r=.06)
def hat(o=False):
    d=.25 if o else .06; x=rng.normal(0,1,int(d*SR)); x=np.diff(x,prepend=0)
    return x*env(d,r=d/3)*.25
def bass(f,d):
    tt=np.arange(int(d*SR))/SR; s=np.tanh(2.2*np.sin(2*np.pi*f*tt))*.5
    e=np.minimum(1,tt/.005)*np.exp(-tt*2.5); return s*e
def pad(fs,d):
    tt=np.arange(int(d*SR))/SR; s=sum(np.sin(2*np.pi*f*tt+np.sin(2*np.pi*.3*tt)*.4) for f in fs)/len(fs)
    e=np.minimum(1,tt/1.2)*np.minimum(1,(d-tt)/1.5); return s*e*.35
def hit():
    d=1.6; tt=np.arange(int(d*SR))/SR
    return (np.sin(2*np.pi*55*tt)*.9+rng.normal(0,1,len(tt))*.25*np.exp(-tt*9))*np.exp(-tt*2.2)
def riser(d):
    tt=np.arange(int(d*SR))/SR; x=rng.normal(0,1,len(tt)); x=np.diff(x,prepend=0)
    return x*(tt/d)**2*.35
roots=[55,55,65.41,49]  # A, A, C, G per bar
BREATH=(99,99); END=29.0
beat=0
while beat*B<T:
    at=beat*B; bar=beat//4; r=roots[bar%4]
    inbreath=BREATH[0]<=at<BREATH[1]
    if at<END and not inbreath:
        add(kick(),at,1.0)
        if beat%4 in (1,3) and at>=2 and at<26: add(snare(),at,.55)
        add(hat(),at+B/2,.8,.3); add(hat(),at,.5,-.3)
        if at>=2: add(bass(r,B*.9),at,.55); add(bass(r*2,B*.4),at+B*.5,.25)
    beat+=1
for c in [5.0,7.5,10.5,13.5,17.0,19.5,22.0,23.5,26.0]: add(hit(),c,.5)
add(riser(2.0),24.0,1.0)
for k in range(8): add(hat(True),k*0.25,.6,(k%2)*.6-.3)
add(hit(),END,1.0); add(pad([110,130.81,164.81,220],4.5),END,.9)
# master
out=np.tanh(out*1.1); out/=np.max(np.abs(out))*1.12
fade=np.ones(n); k=int(1.2*SR); fade[-k:]=np.linspace(1,0,k); out*=fade[:,None]
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
