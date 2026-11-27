# Builds the full-length animatic: Act1 (built) + Act2 placeholders + Act3 (built) + placeholder soundtrack.
import numpy as np, subprocess, os, wave, json, math
from PIL import Image, ImageDraw, ImageFont
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(D)
FPS=24; W,H=1080,1920
font=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf',26)
r01=Image.open(R+'/flow-refs/R01/R01_take1.png').convert('RGB')
friend=Image.open(R+'/act3/img/friend_placeholder.jpg').convert('RGB')
denim=Image.open(R+'/act3/img/card_denim.jpg').convert('RGB')
# last frame of act1 for the crossing dissolve
subprocess.run(['ffmpeg','-y','-loglevel','error','-sseof','-0.05','-i',R+'/act1/act1_silent.mp4','-frames:v','1',D+'/_act1_last.png'],check=True)
last=Image.open(D+'/_act1_last.png').convert('RGB')

def crop_frame(src,box,zoom=1.0,dx=0.0):
    x0,y0,x1,y1=box; cw,ch=x1-x0,y1-y0
    # enforce 9:16 around centre
    cx,cy=(x0+x1)/2+dx,(y0+y1)/2
    if cw/ch>9/16: cw=ch*9/16
    else: ch=cw*16/9
    cw/=zoom; ch/=zoom
    return src.crop((int(cx-cw/2),int(cy-ch/2),int(cx+cw/2),int(cy+ch/2))).resize((W,H),Image.LANCZOS)
def tagged(im,txt):
    d=ImageDraw.Draw(im); d.rounded_rectangle([40,40,60+d.textlength(txt,font=font),88],12,fill=(0,0,0)); d.text((50,50),txt,font=font,fill=(200,200,200)); return im
SEGS=[ # (dur, fn(local_t,p))
 (3.0, lambda t,p: crop_frame(r01,(0,0,1536,2730),1+0.05*p)),
 (1.5, lambda t,p: tagged(crop_frame(r01,(560,1600,840,2100),1.0,dx=-120+240*p),'PLACEHOLDER · S09 flame macro (Flow)')),
 (1.5, lambda t,p: tagged(crop_frame(r01,(560,680,980,1430),1+0.06*p),'PLACEHOLDER · S10 collar (Flow)')),
 (1.5, lambda t,p: tagged(crop_frame(r01,(830,1000,1130,1540),1+0.08*p),'PLACEHOLDER · S11 chest + real logo')),
 (3.0, lambda t,p: tagged(crop_frame(denim,(0,0,540,960),1+0.06*p),'PLACEHOLDER · S12 flat-lay (Flow)')),
 (2.5, lambda t,p: tagged(crop_frame(friend,(0,0,1080,1582),1+0.05*p),'PLACEHOLDER · S13 walk (Flow)')),
]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','16',D+'/_act2_ph.mp4'],stdin=subprocess.PIPE)
first=True
for dur,fn in SEGS:
    n=int(round(dur*FPS))
    for i in range(n):
        im=fn(i/FPS,i/max(1,n-1))
        if first and i<12:  # 0.5s dissolve: outline drawing -> real shirt
            a=(i+1)/12; a=a*a*(3-2*a); im=Image.blend(last,im,a)
        ff.stdin.write(im.tobytes())
    first=False
ff.stdin.close(); ff.wait()
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','/dev/stdin','-c','copy',D+'/_video.mp4'],
  input=f"file '{R}/act1/act1_silent.mp4'\nfile '{D}/_act2_ph.mp4'\nfile '{R}/act3/act3_silent.mp4'\n".encode(),check=True)

# ---------------- soundtrack ----------------
SR=48000; DUR=42.5; out=np.zeros(int(SR*DUR)); rng=np.random.default_rng(3)
def at(t,sig,g=1.0):
    i=int(t*SR); n=min(len(sig),len(out)-i)
    if n>0: out[i:i+n]+=sig[:n]*g
def tt(d): return np.arange(int(d*SR))/SR
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2)[:,0]/32768.0; return x
a1=rd(R+'/act1/sfx_placeholder.wav'); out[:len(a1)]+=a1*0.9
# act3 sfx (global = 30.5 + local)
G=30.5
th=lambda tl: 360*(lambda p:4*p**3 if p<.5 else 1-(-2*p+2)**3/2)(min(1,max(0,(tl-0.45)/(3.25-0.45))))
passes=[]; prev=0
for k in range(1,7):
    for i in range(1,2000):
        tl=0.45+i*0.0014
        if th(tl)>=k*360/7: passes.append(tl); break
for tl in passes:
    d=0.32; x=tt(d); nz=rng.standard_normal(len(x)); env=np.sin(np.pi*x/d)**2
    y=np.convolve(nz,np.ones(12)/12,'same'); at(G+tl-0.16,y*env,0.12)
d=0.5; x=tt(d); at(G+3.3,np.convolve(rng.standard_normal(len(x)),np.ones(8)/8,'same')*np.sin(np.pi*x/d)**2,0.2)
for k,(f,dt) in enumerate([(1046.5,0),(783.99,0.13)]):
    x=tt(0.8); at(G+5.05+dt,(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*f*2.01*x))*np.exp(-x*6),0.09)
x=tt(1.0); f=42+70*np.exp(-x*20); at(G+6.85,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*3),0.6)
x=tt(0.02); at(G+6.85,rng.standard_normal(len(x))*np.exp(-x*300),0.25)
for k,f in enumerate([659.3,493.9]):
    x=tt(0.22); at(G+7.95+k*0.22,np.sin(2*np.pi*f*x)*np.minimum(1,x/0.005)*np.minimum(1,(0.22-x)/0.03),0.12)
d=0.7; x=tt(d); at(G+9.5-d,np.convolve(rng.standard_normal(len(x)),np.ones(6)/6,'same')*(x/d)**3,0.25)
x=tt(1.6); f=40+55*np.exp(-x*16); at(G+9.5,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2),0.7)
# placeholder groove 112bpm from the drop (16.2) until "call ended" (38.45)
music=np.zeros_like(out); B=60/112; t0=16.2; tend=38.45
def mat(t,sig,g):
    i=int(t*SR); n=min(len(sig),len(music)-i)
    if n>0: music[i:i+n]+=sig[:n]*g
nb=int((tend-t0)/B)
LOG=[(0,55),(0.75,55),(1.5,65.4),(2.5,82.4),(3.25,73.4)]
for b in range(nb):
    t=t0+b*B
    x=tt(0.25); f=50+90*np.exp(-x*40); mat(t,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*12),0.5)   # kick
    for s in range(4):
        x=tt(0.05); mat(t+s*B/4,np.diff(np.r_[0,rng.standard_normal(len(x))])*np.exp(-x*90),0.05 if s%2 else 0.03)  # shaker
    if b%2==1:
        x=tt(0.18); mat(t,np.convolve(rng.standard_normal(len(x)),[1,-1],'same')*np.exp(-x*25),0.08)  # clap-ish
for bar in range(nb//4):
    for pos,f0 in LOG:
        t=t0+(bar*4+pos)*B
        if t<tend-0.1:
            x=tt(0.4); f=f0*(1+0.6*np.exp(-x*30)); mat(t,np.tanh(1.6*np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-x*6),0.32)  # log drum
duck=np.ones_like(music); a,b_=int(35.4*SR),int(37.7*SR); duck[a:b_]=0.45
i_end=int(tend*SR); music[i_end:]=0
out+=music*duck
out/=np.abs(out).max(); out*=0.89
pcm=(np.stack([out,out],1)*32767).astype('<i2')
w=wave.open(D+'/_audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',D+'/_video.mp4','-i',D+'/_audio.wav','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',D+'/animatic_v1.mp4'],check=True)
print('animatic ok')
