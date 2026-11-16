import math,random
SPIRAL="M50 50 a5 5 0 0 1 10 0 a10 10 0 0 1 -20 0 a15 15 0 0 1 30 0 a20 20 0 0 1 -40 0 a25 25 0 0 1 50 0 a30 30 0 0 1 -60 0"
LIME,COB,NEO,UV='#B8FF2C','#3A6BFF','#FF3B6E','#8B5CFF'
FL={1:dict(base='#D2FF4D',band='#3DBE1E',acc=LIME,name='MAÇÃ VERDE + LIMÃO'),2:dict(base='#7B93FF',band='#2B1DB5',acc=COB,name='FRAMBOESA AZUL + LIMÃO'),3:dict(base='#FF5A78',band='#7A0F2E',acc=NEO,name='MORANGO + FRUTAS VERMELHAS')}
_n=[0]
def uid():
    _n[0]+=1;return f"u{_n[0]}"
LET="M78 27 A37 37 0 1 0 87 50 H56|M117 13 V87 H166|M387 87 V13 H418 C436 13 444 25 444 36 C444 47 436 59 418 59 H387|M475 13 L510 55 L545 13 M510 55 V87"
def logo(width,letters='silver',disc='tri',spiral='#0A0A0C',extra=''):
    u=uid();h=width*118/572
    lp=''.join(f'<path d="{d}"/>' for d in LET.split('|'))
    lstroke='url(#gl'+u+')' if letters=='silver' else letters
    dfill='url(#gd'+u+')' if disc=='tri' else disc
    sp=f'<path d="{SPIRAL}" fill="none" stroke="{spiral}" stroke-width="5"/>'
    return f"""<svg viewBox="-4 -4 572 118" width="{width}" height="{h:.1f}" style="display:block;overflow:visible;{extra}"><defs><linearGradient id="gl{u}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="100"><stop offset="0" stop-color="#EDEDF0"/><stop offset="1" stop-color="#9798A3"/></linearGradient><linearGradient id="gd{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B8FF2C"/><stop offset=".5" stop-color="#3A6BFF"/><stop offset="1" stop-color="#FF3B6E"/></linearGradient><clipPath id="a{u}"><circle cx="216" cy="50" r="50"/></clipPath><clipPath id="b{u}"><circle cx="320" cy="50" r="50"/></clipPath></defs><g fill="none" stroke="{lstroke}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round">{lp}</g><circle cx="216" cy="50" r="50" fill="{dfill}"/><g clip-path="url(#a{u})"><g transform="translate(216 52) scale(1.6) translate(-50 -50)">{sp}</g></g><circle cx="320" cy="50" r="50" fill="{dfill}"/><g clip-path="url(#b{u})"><g transform="translate(320 52) scale(1.6) translate(-50 -50)">{sp}</g></g></svg>"""
def symbol(size,fill='tri',spiral='#0A0A0C',glow=None):
    u=uid();f='url(#g'+u+')' if fill=='tri' else fill
    st=f"display:block;{'filter:drop-shadow(0 0 %spx rgba(58,107,255,.45));'%glow if glow else ''}"
    return f"""<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="{st}"><defs><linearGradient id="g{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B8FF2C"/><stop offset=".5" stop-color="#3A6BFF"/><stop offset="1" stop-color="#FF3B6E"/></linearGradient><clipPath id="c{u}"><circle cx="50" cy="50" r="50"/></clipPath></defs><circle cx="50" cy="50" r="50" fill="{f}"/><g clip-path="url(#c{u})"><g transform="translate(50 52) scale(1.6) translate(-50 -50)"><path d="{SPIRAL}" fill="none" stroke="{spiral}" stroke-width="5"/></g></g></svg>"""
def fdisc(size,n,glow=False):
    u=uid();f=FL[n]
    st="display:block;"+("filter:drop-shadow(0 0 %spx %s);"%(size*.22,f['acc']) if glow else '')
    return f"""<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="{st}"><defs><clipPath id="d{u}"><circle cx="50" cy="50" r="48"/></clipPath></defs><circle cx="50" cy="50" r="48" fill="{f['base']}"/><g clip-path="url(#d{u})"><g transform="translate(50 52) scale(1.5) translate(-50 -50)"><path d="{SPIRAL}" fill="none" stroke="{f['band']}" stroke-width="7"/></g></g></svg>"""
def lashes(P0,C,P2,n,length,color,sw,side=1,t0=.06,t1=.94):
    o=''
    for i in range(n):
        t=t0+(t1-t0)*i/(n-1)
        x=(1-t)**2*P0[0]+2*(1-t)*t*C[0]+t**2*P2[0];y=(1-t)**2*P0[1]+2*(1-t)*t*C[1]+t**2*P2[1]
        dx=2*(1-t)*(C[0]-P0[0])+2*t*(P2[0]-C[0]);dy=2*(1-t)*(C[1]-P0[1])+2*t*(P2[1]-C[1])
        l=math.hypot(dx,dy);nx,ny=(dy/l)*side,(-dx/l)*side
        if side==1 and ny>0: nx,ny=-nx,-ny
        if side==-1 and ny<0: nx,ny=-nx,-ny
        L=length(i,n) if callable(length) else length
        o+=f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+nx*L:.1f}" y2="{y+ny*L:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
    return o
def eye(n,w=260,uidn=None,lash=True):
    u=uid();f=FL[n];h=w*160/280
    la=lashes((20,80),(140,0),(260,80),19,9,f['acc'],1.33,1)+lashes((20,80),(140,160),(260,80),19,9,f['acc'],1.33,-1) if lash else ''
    return f"""<svg viewBox="0 0 280 160" width="{w}" height="{h:.0f}" style="display:block;overflow:visible" fill="none"><defs><clipPath id="e{u}"><path d="M20 80 Q140 0 260 80 Q140 160 20 80 Z"/></clipPath><clipPath id="i{u}"><circle cx="140" cy="80" r="50"/></clipPath><radialGradient id="h{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>{la}<path d="M20 80 Q140 0 260 80 Q140 160 20 80 Z" fill="#050507"/><g clip-path="url(#e{u})"><g style="filter:drop-shadow(0 0 15px {f['acc']})"><circle cx="140" cy="80" r="50" fill="{f['base']}"/></g><g clip-path="url(#i{u})"><g transform="translate(140 82) scale(1.484) translate(-50 -50)"><path d="{SPIRAL}" stroke="{f['band']}" stroke-width="7" stroke-linecap="round"/></g></g><circle cx="140" cy="80" r="50" fill="url(#h{u})"/></g><path d="M20 80 Q140 0 260 80 Q140 160 20 80 Z" stroke="{f['acc']}" stroke-width="2" stroke-linejoin="round"/></svg>"""
def waves(w,h,color,n=8):
    cx,cy=w/2,h/2;o=''
    for i in range(n):
        k=i/(n-1);hw=(w/2-4)*(0.3+0.7*k)*1.0;hh=(h/2)*(0.3+0.7*k)*1.2
        op=.85-.7*k;o+=f'<path d="M{cx-hw:.0f} {cy} Q{cx} {cy-2*hh:.0f} {cx+hw:.0f} {cy} Q{cx} {cy+2*hh:.0f} {cx-hw:.0f} {cy} Z" fill="none" stroke="{color if i<2 else "#3A3A44"}" stroke-opacity="{op:.2f}" stroke-width="{1.9-1.1*k:.2f}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;overflow:visible" fill="none">{o}</svg>'
def star(x,y,s,c,glow=3):
    return f'<path d="M0 -7 Q1 -1 7 0 Q1 1 0 7 Q-1 1 -7 0 Q-1 -1 0 -7 Z" transform="translate({x} {y}) scale({s})" fill="{c}" style="filter:drop-shadow(0 0 {glow}px {c})"/>'
def glitter(w,h,n,seed=3,avoid=None):
    r=random.Random(seed);cols=[('#EDEDF0',.9),('#EDEDF0',.5),(NEO,.6),(COB,.6),(LIME,.6)];o=''
    for _ in range(n):
        x,y=r.random()*w,r.random()*h
        if avoid and avoid(x,y):continue
        c=r.choice(cols);o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.choice([.8,1.2,1.6]):.1f}" fill="{c[0]}" fill-opacity="{c[1]}"/>'
    return o
def shadowlines(cx,cy,hw,hh,n=4,w=1.0):
    u=uid();o=f'<defs><linearGradient id="t{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B8FF2C"/><stop offset=".5" stop-color="#3A6BFF"/><stop offset="1" stop-color="#FF3B6E"/></linearGradient></defs>'
    for i in range(n):
        k=(i+1)*0.085;sw=[2.2,1.4,.9,.6,.5][i]*w;op=[1,.8,.55,.35,.25][i]
        a=hw*(1+k*1.2);b=hh*(1+k*4.6)
        o+=f'<path d="M{cx-a:.1f} {cy} Q{cx} {cy-2*b:.1f} {cx+a:.1f} {cy} Q{cx} {cy+2*b:.1f} {cx-a:.1f} {cy} Z" fill="none" stroke="url(#t{u})" stroke-width="{sw}" stroke-opacity="{op}"/>'
    return o
def pack(n,scale=1.0,teaser=False):
    u=uid();f=FL[n];S=scale
    lash=lashes((18,128),(110,52),(202,128),15,9,f['acc'],1,1,.05,.95)+lashes((18,128),(110,204),(202,128),15,9,f['acc'],1,-1,.05,.95)
    gl=glitter(220,270,26,seed=7,avoid=lambda x,y:60<y<200 and 20<x<200 and False)
    stars=star(24,78,1.5,'#EDEDF0')+star(196,92,1,f['acc'])+star(34,188,.9,f['acc'])+star(190,196,1.6,'#EDEDF0')+star(112,70,.7,'#EDEDF0')+star(108,198,.8,'#EDEDF0')
    sl=shadowlines(110,128,92,26,4,1.0)
    band=f"""<rect x="0" y="218" width="220" height="30" fill="#0A0A0C"/><rect x="0" y="218" width="220" height="1" fill="{f['acc']}"/><g transform="translate({110-len(f['name'])*2.9-10:.0f} 225)"><svg x="0" y="0" width="16" height="16" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="{f['base']}"/><g transform="translate(50 52) scale(1.5) translate(-50 -50)"><path d="{SPIRAL}" fill="none" stroke="{f['band']}" stroke-width="7"/></g></svg><text x="22" y="12" font-family="Space Grotesk" font-weight="600" font-size="9" letter-spacing="1.08" fill="#EDEDF0">{f['name']}</text></g>"""
    stripes=''.join(f'<rect x="0" y="{y}" width="220" height="1.6" fill="#fff" fill-opacity=".14"/>' for y in list(range(0,22,5))+list(range(248,270,5)))
    return f"""<svg viewBox="0 0 220 430" width="{220*S:.0f}" height="{430*S:.0f}" style="display:block;overflow:visible;filter:drop-shadow(0 18px 24px rgba(0,0,0,.7))"><defs><mask id="m{u}"><rect width="220" height="270" fill="#fff"/><path d="M18 128 Q110 52 202 128 Q110 204 18 128 Z" fill="#000"/></mask><clipPath id="w{u}"><path d="M18 128 Q110 52 202 128 Q110 204 18 128 Z"/></clipPath><clipPath id="k{u}"><circle cx="110" cy="130" r="108"/></clipPath><clipPath id="r{u}"><rect width="220" height="270" rx="6"/></clipPath><radialGradient id="h{u}" cx=".3" cy=".25" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></radialGradient><linearGradient id="s{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".25" stop-color="#fff" stop-opacity="0"/><stop offset=".75" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient></defs>
<rect x="106" y="262" width="8" height="168" rx="4" fill="#050505" stroke="#34343C"/>
<g clip-path="url(#r{u})"><rect width="220" height="270" fill="#0A0A0C"/>
<circle cx="110" cy="130" r="108" fill="{f['base']}"/><g clip-path="url(#k{u})"><g transform="translate(110 134.5) scale(3.375) translate(-50 -50)"><path d="{SPIRAL}" fill="none" stroke="{f['band']}" stroke-width="6" stroke-linecap="round"/></g></g><circle cx="110" cy="130" r="108" fill="url(#h{u})"/>
<rect width="220" height="270" fill="#0A0A0C" mask="url(#m{u})"/><g mask="url(#m{u})">{sl}{gl}{stars}</g>
<g clip-path="url(#w{u})"><path d="M-20 290 L130 -20 L170 -20 L20 290 Z" fill="#fff" fill-opacity=".10"/><path d="M18 128 Q110 52 202 128 Q110 204 18 128 Z" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="10"/></g>
<path d="M18 128 Q110 52 202 128 Q110 204 18 128 Z" fill="none" stroke="{f['acc']}" stroke-width="1.5" stroke-linejoin="round"/>{lash}
<g transform="translate({110-46} 26)">{logo(92).replace('<svg','<svg x="0" y="0"',1)}</g>
<text x="110" y="198" text-anchor="middle" font-family="JetBrains Mono" font-weight="500" font-size="8" letter-spacing="3.2" fill="#8B8B94">ME OLHA.</text>
{band}{stripes}<rect width="220" height="270" fill="url(#s{u})"/></g></svg>"""
