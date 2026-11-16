import math
import os
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','fonts')+'/'
SG=F+'SpaceGrotesk-Bold.ttf'
JB=F+'JetBrainsMono-Medium.ttf'
import base64
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
CSS=f"""
@font-face{{font-family:SG;src:url(data:font/ttf;base64,{b64(SG)});font-weight:700}}
@font-face{{font-family:JB;src:url(data:font/ttf;base64,{b64(JB)});font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0A0A0C;overflow:hidden}}
.lab{{font-family:JB;font-weight:500;color:#8B8B94;letter-spacing:.4em;font-size:26px;text-transform:uppercase}}
.ttl{{font-family:SG;font-weight:700;color:#EDEDF0;letter-spacing:-.02em}}
"""
SPIRAL="M50 50 a5 5 0 0 1 10 0 a10 10 0 0 1 -20 0 a15 15 0 0 1 30 0 a20 20 0 0 1 -40 0 a25 25 0 0 1 50 0 a30 30 0 0 1 -60 0"
def eye(cx,cy,hw,hh,open_=1.0,iris='#B8FF2C',rot=0,glow=True,uid='e'):
    h=hh*max(open_,0.02)
    d=f"M {cx-hw} {cy} Q {cx} {cy-2*h} {cx+hw} {cy} Q {cx} {cy+2*h} {cx-hw} {cy} Z"
    r=min(hh*1.0,hw*.5)*1.0
    s=r/38
    return f"""
<defs><clipPath id="c{uid}"><path d="{d}"/></clipPath>
<radialGradient id="g{uid}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{iris}" stop-opacity=".95"/><stop offset=".6" stop-color="{iris}" stop-opacity=".55"/><stop offset="1" stop-color="#0A0A0C"/></radialGradient>
<filter id="f{uid}" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="22"/></filter></defs>
{'<path d="'+d+'" fill="'+iris+'" opacity=".28" filter="url(#f'+uid+')"/>' if glow and open_>.1 else ''}
<path d="{d}" fill="#1B1B20"/>
<g clip-path="url(#c{uid})">
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g{uid})"/>
<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-50 -50)"><path d="{SPIRAL}" fill="none" stroke="#0A0A0C" stroke-width="3.2" stroke-linecap="round"/></g>
</g>
<path d="{d}" fill="none" stroke="{iris}" stroke-width="5" stroke-linejoin="round"/>
"""
def page(w,h,body):
    return f"<html><head><style>{CSS}</style></head><body><div style='width:{w}px;height:{h}px;position:relative'>{body}</div></body></html>"
def svg(w,h,inner): return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' style='position:absolute;left:0;top:0'>{inner}</svg>"
