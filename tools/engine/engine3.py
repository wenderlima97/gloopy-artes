import sys,json
sys.path.insert(0,'/tmp/gloopy');sys.path.insert(0,'.')
from assets import logo,SPIRAL
from lib import SG,JB,b64
JS=r"""
const C=CFG,W=C.w,H=C.h,TAU=Math.PI*2;
const FLV={lime:{base:'#D2FF4D',band:'#3DBE1E',acc:'#B8FF2C'},cob:{base:'#7B93FF',band:'#2B1DB5',acc:'#3A6BFF'},neo:{base:'#FF5A78',band:'#7A0F2E',acc:'#FF3B6E'}};
const F=FLV[C.flavor],ACC=F.acc;
const alm=(cx,cy,hw,hh)=>`M${cx-hw} ${cy} Q${cx} ${cy-2*hh} ${cx+hw} ${cy} Q${cx} ${cy+2*hh} ${cx-hw} ${cy} Z`;
const g=(t,c,w)=>Math.exp(-Math.pow((t-c)/w,2));
const blink=t=>C.noblink?0:Math.max(g(t,.50,.022),g(t,.572,.016));
const gl=t=>C.static?0:Math.max(g(t,.50,.02),g(t,.75,.012),g(t,.25,.008),g(t,.572,.012));
function rnd(s){let x=Math.sin(s*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function lashes(cx,cy,hw,hh,n,col,sw,t,dir,amp){let o='';for(let i=0;i<n;i++){const u=.05+.9*i/(n-1);
 const x=(1-u)*(1-u)*(cx-hw)+2*(1-u)*u*cx+u*u*(cx+hw);const y=cy+dir*(2*(1-u)*u*(-2*hh*-1))*-1*-1;
 const py=cy+dir*2*(1-u)*u*(2*hh)*-1*-1;
 const yy=cy-dir*(2*(1-u)*u*2*hh)*1; // y on curve (dir=1 top)
 const dx=2*(1-u)*(cx-(cx-hw))+2*u*((cx+hw)-cx),dy=-dir*(2*(1-u)*(2*hh)*-1)*0; 
 // tangent
 const tx=2*(1-u)*(hw)+2*u*(hw), ty=dir*(-1)*2*hh*2*(1-2*u)*-1*-1;
 const tl=Math.hypot(tx,2*hh*2*(1-2*u)),nx=(2*hh*2*(1-2*u))/tl*dir*-1, ny=-tx/tl*dir;
 const base=[40,10,60,20,34,8,28,50][i%8]*amp;const k=.45+.55*Math.abs(Math.sin(TAU*(t*4*(1+(i%3)*.5)+i*.31)));
 const L=base*k*(1+.5*Math.exp(-((t*16)%1)*5));
 o+=`<line x1="${x.toFixed(1)}" y1="${yy.toFixed(1)}" x2="${(x+nx*L*(dir>0?1:1)).toFixed(1)}" y2="${(yy+ny*L).toFixed(1)}" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-opacity="${(.5+.5*k).toFixed(2)}"/>`}return o}
function stars(t){const S=C.stars||[];let o='';S.forEach((s,i)=>{const k=.55+.45*Math.sin(TAU*(t*(1+(i%3))+s[3]));o+=`<path d="M0 -7 Q1 -1 7 0 Q1 1 0 7 Q-1 1 -7 0 Q-1 -1 0 -7 Z" transform="translate(${s[0]} ${s[1]}) scale(${(s[2]*k*1.15).toFixed(2)}) rotate(${C.static?0:(t*90).toFixed(1)})" fill="${s[4]||'#EDEDF0'}" style="filter:drop-shadow(0 0 5px ${s[4]||'#EDEDF0'})"/>`});return o}
function glitter(t){let o='';const cols=['#EDEDF0','#EDEDF0',ACC,'#3A6BFF','#FF3B6E'];const n=C.glitter||90;
 for(let i=0;i<n;i++){const x=rnd(i+1)*W,y0=rnd(i+77)*H,k=1+Math.floor(rnd(i+9)*2);let y=(y0-k*t*H*.5+H*4)%H;
  const tw=.4+.6*Math.abs(Math.sin(TAU*(t*(2+(i%4))+rnd(i+5))));
  o+=`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(1.3+rnd(i+3)*2.4).toFixed(1)}" fill="${cols[i%5]}" fill-opacity="${(tw*.75).toFixed(2)}"/>`}return o}
function draw(t,fr){
 const cx=W/2,cy=C.cy,hw=C.eyeHW,hh=C.eyeHH*(1-.97*blink(t)),kick=Math.exp(-((t*16)%1)*6),ga=gl(t);
 const rot=C.static?C.rot||0:t*360, sc=1+.025*kick;
 let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs>
 <radialGradient id="vg" cx=".5" cy="${(cy/H).toFixed(2)}" r=".75"><stop offset="0" stop-color="#15151C"/><stop offset=".6" stop-color="#0A0A0C"/><stop offset="1" stop-color="#050507"/></radialGradient>
 <linearGradient id="tri" gradientUnits="userSpaceOnUse" x1="${cx-hw*1.6}" y1="0" x2="${cx+hw*1.6}" y2="0"><stop offset="0" stop-color="#B8FF2C"/><stop offset=".5" stop-color="#3A6BFF"/><stop offset="1" stop-color="#FF3B6E"/></linearGradient>
 <clipPath id="eyc"><path d="${alm(cx,cy,hw,hh)}"/></clipPath><clipPath id="irc"><circle cx="${cx}" cy="${cy}" r="${C.eyeHH*1.25}"/></clipPath>
 <radialGradient id="hl" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/></radialGradient>
 <filter id="gb" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
 <filter id="gr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="${fr%12}"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0"/></filter></defs>
 <rect width="${W}" height="${H}" fill="url(#vg)"/>`;
 // tone-on-tone spiral background
 s+=`<g transform="translate(${cx} ${cy}) rotate(${rot.toFixed(2)}) scale(${(C.spiralScale||17).toFixed(2)}) translate(-50 -50)"><path d="${SPIRAL}" fill="none" stroke="#1B1B20" stroke-width="${C.spiralW||1.1}" stroke-linecap="round" stroke-opacity=".85"/><path d="M50 50 a5 5 0 0 1 10 0 a10 10 0 0 1 -20 0 a15 15 0 0 1 30 0" fill="none" stroke="${ACC}" stroke-width="${(C.spiralW||1.1)*.7}" stroke-linecap="round" stroke-opacity=".35"/></g>`;
 if(C.scene!=='text'){
 // waves
 for(let k=0;k<8;k++){const ph=((t*8)+k/8)%1,sx=1+ph*(C.waveGrow||1.5);s+=`<path d="${alm(cx,cy,hw*sx,hh0(C)*sx*1.05)}" fill="none" stroke="${k%4==0?ACC:'#8B8B94'}" stroke-opacity="${((1-ph)*(k%4==0?.55:.28)).toFixed(2)}" stroke-width="${(2.4*(1-ph)+.6).toFixed(2)}"/>`}
 // shadow lines
 for(let i=0;i<4;i++){const k=(i+1)*.085*(1+.15*kick),a=hw*(1+k*1.2)*sc,b=hh0(C)*(1+k*4.6)*sc*(1-.5*blink(t));s+=`<path d="${alm(cx,cy,a,b)}" fill="none" stroke="url(#tri)" stroke-width="${[3.4,2.2,1.4,1][i]}" stroke-opacity="${[1,.8,.55,.35][i]}"/>`}
 s+=lashes(cx,cy,hw,hh,46,ACC,2.6,t,1,C.lash||1.7)+lashes(cx,cy,hw,hh,46,ACC,2.6,t,-1,C.lash||1.7);
 s+=`<path d="${alm(cx,cy,hw,hh)}" fill="#050507"/>`;
 if(C.scene==='eye'){
  s+=`<g clip-path="url(#eyc)"><circle cx="${cx}" cy="${cy}" r="${C.eyeHH*1.25}" fill="${F.base}" filter="url(#gb)" opacity=".55"/><circle cx="${cx}" cy="${cy}" r="${C.eyeHH*1.25}" fill="${F.base}"/><g clip-path="url(#irc)"><g transform="translate(${cx} ${cy+3}) rotate(${(-rot).toFixed(2)}) scale(${(C.eyeHH*1.25/50*1.484).toFixed(3)}) translate(-50 -50)"><path d="${SPIRAL}" fill="none" stroke="${F.band}" stroke-width="7" stroke-linecap="round"/></g></g><circle cx="${cx}" cy="${cy}" r="${C.eyeHH*1.25}" fill="url(#hl)"/></g>`;
 } else { // sinal: disc with pulsing rings
  const r=C.eyeHH*.95;for(let k=0;k<3;k++){const ph=((t*8)+k/3)%1;s+=`<circle cx="${cx}" cy="${cy}" r="${(r*(1.05+ph*.9)).toFixed(1)}" fill="none" stroke="${ACC}" stroke-opacity="${((1-ph)*.55).toFixed(2)}" stroke-width="3"/>`}
  s+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="${F.base}" filter="url(#gb)" opacity=".5"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="${F.base}"/><g clip-path="url(#sc)"><g transform="translate(${cx} ${cy+3}) rotate(${rot.toFixed(2)}) scale(${(r/50*1.5).toFixed(3)}) translate(-50 -50)"><path d="${SPIRAL}" fill="none" stroke="${F.band}" stroke-width="7" stroke-linecap="round"/></g></g><circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#hl)"/>`;
  s=s.replace('<g clip-path="url(#sc)">',`<clipPath id="sc"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath><g clip-path="url(#sc)">`);
 }
 s+=`<path d="${alm(cx,cy,hw,hh)}" fill="none" stroke="${ACC}" stroke-width="4" stroke-linejoin="round"/>`;
 } else {
  const r=C.symR||150;s+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="${F.base}" opacity=".5" filter="url(#gb)"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="${F.base}"/><clipPath id="sc2"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath><g clip-path="url(#sc2)"><g transform="translate(${cx} ${cy+3}) scale(${(r/50*1.5).toFixed(3)}) translate(-50 -50)"><path d="${SPIRAL}" fill="none" stroke="${F.band}" stroke-width="7" stroke-linecap="round"/></g></g><circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#hl)"/>`;
 }
 s+=glitter(t)+stars(t);
 // title
 const lines=Array.isArray(C.title)?C.title:[C.title],fs=C.titleSize;
 const T=(dx,fill,op,mode)=>lines.map((L,i)=>`<text x="${C.titleX+dx}" y="${C.titleY+i*fs*1.04}" font-family="Space Grotesk" font-weight="700" font-size="${fs}" letter-spacing="${-.03*fs}" fill="${fill}" fill-opacity="${op}" ${mode?`style="mix-blend-mode:screen"`:''}>${L}</text>`).join('');
 if(ga>.06){s+=T(-ga*14,'#FF3B6E',.8,1)+T(ga*14,'#3A6BFF',.8,1)}
 s+=T(0,'#EDEDF0',1,0);
 const ty=C.titleY+(lines.length-1)*fs*1.04+54;
 s+=`<text x="${C.titleX}" y="${ty}" font-family="JetBrains Mono" font-weight="500" font-size="30" letter-spacing="12" fill="#8B8B94">${C.sub||''}</text>`;
 s+=`<text x="${C.titleX}" y="${C.tagY}" font-family="JetBrains Mono" font-weight="500" font-size="28" letter-spacing="9" fill="#8B8B94">${C.tagL||''}</text><text x="${W-C.titleX}" y="${C.tagY}" text-anchor="end" font-family="JetBrains Mono" font-weight="500" font-size="28" letter-spacing="9" fill="${ACC}">${C.tagR||''}</text>`;
 if(ga>.3){for(let y=0;y<H;y+=6)s+=`<rect x="0" y="${y}" width="${W}" height="2" fill="#000" fill-opacity="${(ga*.18).toFixed(2)}"/>`}
 s+=`<rect width="${W}" height="${H}" filter="url(#gr)" opacity=".07"/></svg>`;
 document.getElementById('root').innerHTML=s;
 document.getElementById('logo').style.opacity=ga>.6?.6:1;
}
function hh0(C){return C.eyeHH}
"""
def build(cfg):
    css=f"@font-face{{font-family:'Space Grotesk';src:url(data:font/ttf;base64,{b64(SG)});font-weight:400 700}}@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{b64(JB)});font-weight:400 500}}html,body{{margin:0;background:#0A0A0C}}#root{{position:absolute;left:0;top:0}}#logo{{position:absolute;left:0;right:0;top:{cfg['logoY']}px;display:flex;justify-content:center}}"
    spiral=SPIRAL
    return f"<html><head><meta charset='utf-8'><style>{css}</style></head><body><div id='root'></div><div id='logo'>{logo(cfg.get('logoW',340))}</div><script>const CFG={json.dumps(cfg)};const SPIRAL={json.dumps(spiral)};{JS}</script></body></html>"
