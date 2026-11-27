import math, sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
P='/tmp/claude-0/-home-user-tun832061-arch-github-io/1d336f03-7800-5438-a46b-f354cd03bd18/scratchpad/'
main=TTFont(P+'npmfonts/fontsource-barlow-semi-condensed-5.3.0/files/barlow-semi-condensed-latin-600-italic.woff')
sub=TTFont(P+'npmfonts/fontsource-barlow-5.3.0/files/barlow-latin-700-italic.woff')
cfg=json.load(open(P+'logo/cfg.json'))

def glyph(font,ch,x,base,scale=1.0):
    gs=font.getGlyphSet(); name=font.getBestCmap()[ord(ch)]
    pen=SVGPathPen(gs)
    tp=TransformPen(pen,(scale,0,0,-scale,x,base))
    gs[name].draw(tp)
    return pen.getCommands(), gs[name].width*scale

def bounds(font,ch):
    gs=font.getGlyphSet(); bp=BoundsPen(gs); gs[font.getBestCmap()[ord(ch)]].draw(bp); return bp.bounds

paths=[]; x=0; track=cfg['track']; pos={}
for i,ch in enumerate("SE_FMADE"):
    if ch=='_':
        pos['L']=x; x+=cfg['Ladv']; continue
    d,w=glyph(main,ch,x,700); paths.append(d); pos[ch+str(i)]=(x,w); x+=w+track
right_E=x-track
tan7=math.tan(math.radians(7))

def bez(p0,p1,p2,p3,t):
    return tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t**2*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3))

sw=cfg['stem']; Lx=pos['L']+cfg['Loff']
segs=[]
# stem: from above cap to hook start, slanted 7deg
top=(Lx+700*tan7+sw/2, -40); 
h0=(Lx+(700-cfg['hookY0'])*tan7+sw/2, cfg['hookY0'])
segs.append(((top),(top),(h0),(h0)))
c=cfg
segs.append((h0, (h0[0]-c['h1'][0],h0[1]+c['h1'][1]), (h0[0]+c['h2'][0],c['hookBot']), (h0[0]+c['h3'][0],c['hookBot'])))
p=segs[-1][3]
segs.append((p,(p[0]+c['s1'][0],c['s1'][1]),(right_E+c['s2'][0],c['s2'][1]),(right_E+c['end'][0],c['end'][1])))
pts=[]; widths=[]
N=[40,60,160]
for si,s in enumerate(segs):
    for k in range(N[si]):
        t=k/N[si]; pts.append(bez(*s,t))
        if si<2: widths.append(sw)
        else:
            u=t; widths.append(sw*(1-u)**c['taper']+c['tip']*(1-(1-u)**c['taper']))
pts.append(segs[-1][3]); widths.append(c['tip'])
L=[];R=[]
for i,(px,py) in enumerate(pts):
    a=pts[max(i-1,0)]; b=pts[min(i+1,len(pts)-1)]
    dx,dy=b[0]-a[0],b[1]-a[1]; n=math.hypot(dx,dy) or 1
    nx,ny=-dy/n,dx/n; w=widths[i]/2
    L.append((px+nx*w,py+ny*w)); R.append((px-nx*w,py-ny*w))
poly=L+R[::-1]
t7=math.tan(math.radians(7))
poly=[(x-(0-y)*t7,0.0) if y<0 else (x,y) for x,y in poly]
swash="M"+" L".join(f"{a:.1f},{b:.1f}" for a,b in poly)+"Z"
# centerline for gap stroke
center="M"+" L".join(f"{a:.1f},{b:.1f}" for a,b in pts)

# TRENDZ
ts=c['tsize']/700; letters="TRENDZ"; tw=[]; 
for ch in letters: tw.append(sub.getGlyphSet()[sub.getBestCmap()[ord(ch)]].width*ts)
total=sum(tw)+c['ttrack']*(len(letters)-1)
tx=right_E+c['tdx']-total; tbase=700+c['tgap']+c['tsize']; tpaths=[]
for ch,w in zip(letters,tw):
    d,_=glyph(sub,ch,tx,tbase,ts); tpaths.append(d); tx+=w+c['ttrack']
tm_s=c['tmsize']/700
tmx=tx-c['ttrack']+c['tmdx']
d1,w1=glyph(sub,'T',tmx,tbase-c['tsize']+c['tmsize'],tm_s); d2,_=glyph(sub,'M',tmx+w1+4,tbase-c['tsize']+c['tmsize'],tm_s)
tpaths+= [d1,d2]

sk=c['skew']; W=right_E+c['pad']*2+120; H=tbase+c['pad']*2+80
vb=f"{-c['pad']-60} {-c['pad']-60} {W} {H}"
def svg(mode):
    fill='currentColor'
    word=" ".join(paths)
    style=f'fill="{fill}"' if mode=='solid' else f'fill="none" stroke="{fill}" stroke-width="{c["ow"]}" stroke-linejoin="round"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" color="{ '#fff' }">
<defs>
 <clipPath id="top"><rect x="-500" y="0" width="5000" height="3000"/></clipPath>
 <mask id="knock" maskUnits="userSpaceOnUse" x="-500" y="-500" width="5000" height="3000">
  <rect x="-500" y="-500" width="5000" height="3000" fill="#fff"/>
  <path d="{center}" fill="none" stroke="#000" stroke-width="{c['gap']}" stroke-linecap="round" clip-path="url(#top)"/>
  <path d="{swash}" fill="#000" stroke="#000" stroke-width="{c['gap']-c['stem']+20}" clip-path="url(#top)"/>
 </mask>
</defs>
<g transform="skewX({-sk})">
 <g mask="url(#knock)"><path id="word" d="{word}" {style}/></g>
 <path id="swash" d="{swash}" {style}/>
 <path id="trendz" d="{' '.join(tpaths)}" {style}/>
</g>
</svg>'''
open(P+'logo/selfmade_logo.svg','w').write(svg('solid'))
open(P+'logo/selfmade_logo_outline.svg','w').write(svg('outline'))
print("ok", right_E)
