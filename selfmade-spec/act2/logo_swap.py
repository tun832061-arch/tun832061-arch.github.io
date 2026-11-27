# Replaces the AI-generated chest logos with the real SELF MADE Trendz logo.
import cv2, numpy as np, json, os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(D)
lw=Image.open(R+'/logo/selfmade_logo_white.png'); lw=lw.crop(lw.getbbox())
lb=Image.open(R+'/logo/selfmade_logo_black.png'); lb=lb.crop(lb.getbbox())
S=1080/1536
BOX={ # x0,y0,x1,y1 search window for the AI logo
 'prod_black':(590,795,780,880),'prod_cream':(590,795,780,880),'prod_grey':(590,795,780,880),'prod_burgundy':(590,795,780,880),
 'prod_purple':(600,400,830,500),'model_black':(630,780,830,875),'model_cream':(515,830,690,905),
 'model_grey':(540,795,700,865),'model_burgundy':(550,760,705,830),'model_purple':(585,785,745,855)}
PLACE={'prod_black':(975*S,1190*S,235*S)}   # exact spot the animated logo lands on in the crossing
DARKTEXT={'prod_cream','model_cream'}
out={}
for n,(x0,y0,x1,y1) in BOX.items():
    src=cv2.imread(f'{D}/img_orig/{n}.jpg'); g=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY).astype(float)
    roi=g[y0:y1,x0:x1]; med=np.median(roi)
    m=(roi<med-45) if n in DARKTEXT else (roi>med+45)
    mask=np.zeros(g.shape,np.uint8); mask[y0:y1,x0:x1]=m.astype(np.uint8)*255
    mask=cv2.dilate(mask,np.ones((7,7),np.uint8),2)
    ys,xs=np.where(mask>0); bx0,bx1,by0,by1=xs.min(),xs.max(),ys.min(),ys.max()
    clean=cv2.inpaint(src,mask,9,cv2.INPAINT_TELEA)
    # restore fabric grain over the patched area
    rng=np.random.default_rng(1); noise=rng.normal(0,3.0,clean.shape)
    soft=cv2.GaussianBlur(mask,(0,0),3)[...,None]/255.0
    clean=np.clip(clean+noise*soft,0,255).astype(np.uint8)
    if n in PLACE: cx,cy,w=PLACE[n]
    else: cx,cy,w=(bx0+bx1)/2,(by0+by1)/2,(bx1-bx0)*1.04
    logo=(lb if n in DARKTEXT else lw)
    h=w*logo.height/logo.width; L=logo.resize((max(1,int(w)),max(1,int(h))),Image.LANCZOS)
    a=np.asarray(L).astype(float)/255.0; alpha=a[...,3]; alpha=cv2.GaussianBlur(alpha,(0,0),0.6)*0.93
    rgb=a[...,:3]*255
    X=int(round(cx-L.width/2)); Y=int(round(cy-L.height/2))
    base=clean[Y:Y+L.height,X:X+L.width].astype(float)[...,::-1]
    tex=cv2.cvtColor(clean[Y:Y+L.height,X:X+L.width],cv2.COLOR_BGR2GRAY).astype(float); tex=(tex-tex.mean())/40.0
    rgb=np.clip(rgb*(1+0.12*tex[...,None]),0,255)
    comp=base*(1-alpha[...,None])+rgb*alpha[...,None]
    clean[Y:Y+L.height,X:X+L.width]=comp[...,::-1].astype(np.uint8)
    cv2.imwrite(f'{D}/img/{n}.jpg',clean,[cv2.IMWRITE_JPEG_QUALITY,93])
    out[n]=[int(bx0),int(by0),int(bx1),int(by1)]
print(out)
