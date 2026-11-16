import numpy as np,wave,sys
sys.path.insert(0,'.')
import audio as A
from audio import *
rng=np.random.default_rng(21)
mf=lambda m:440*2**((m-69)/12)
STEP=BEAT/4
def swing(s): return s*STEP+(STEP*.14 if s%2==1 else 0)
def saw(f,tt,det=(0,)):return sum(2*((tt*f*(1+d))%1)-1 for d in det)/len(det)
def kick2():
    tt=np.arange(int(SR*.32))/SR;f=48+90*np.exp(-tt*40);ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*9)*.9+np.where(tt<.004,.35,0)*np.exp(-tt*600)
def chat(L=.05):
    tt=np.arange(int(SR*L))/SR;return hp(rng.standard_normal(len(tt)),8000)*np.exp(-tt*90)
def ohat():
    tt=np.arange(int(SR*.22))/SR;return hp(rng.standard_normal(len(tt)),6500)*np.exp(-tt*22)
def shaker():
    tt=np.arange(int(SR*.09))/SR;return bp(rng.standard_normal(len(tt)),5000,11000,2)*np.sin(np.pi*np.clip(tt/.09,0,1))**1.5
def rim():
    tt=np.arange(int(SR*.12))/SR;return (np.sin(2*np.pi*1750*tt)*.5+bp(rng.standard_normal(len(tt)),1200,4000,2)*.5)*np.exp(-tt*45)
def soft_clap():
    tt=np.arange(int(SR*.3))/SR;n=bp(rng.standard_normal(len(tt)),1000,5000,2);return n*(np.exp(-tt*18)*.6+(np.exp(-np.clip(tt-.012,0,None)*50)*(tt>.012))*.3)
def conga(f=330):
    tt=np.arange(int(SR*.25))/SR;fr=f*(1+.25*np.exp(-tt*40));ph=2*np.pi*np.cumsum(fr)/SR;return np.sin(ph)*np.exp(-tt*16)
def mix3(style,outp):
    kd=np.zeros(N);hats=np.zeros(N);perc=np.zeros(N);bass=np.zeros(N);pad=np.zeros(N);arp=np.zeros(N);fx=np.zeros(N)
    for b in range(16):place(kd,kick2(),b*BEAT)
    sc=np.ones(N)
    for b in range(16):
        i=int(b*BEAT*SR);m=int(.34*SR);idx=(np.arange(m)+i)%N;sc[idx]=np.minimum(sc[idx],1-.92*np.exp(-np.arange(m)/SR*7))
    for b in range(16):place(hats,ohat()*.5,b*BEAT+BEAT/2)
    for s in range(64):
        if s%4!=2:place(hats,chat()*(.22 if s%2==0 else .34),swing(s))
    for s in range(64):
        if (s*5)%7 in (0,3):place(perc,shaker()*.32,swing(s))
    for b in (1,3,5,7,9,11,13,15):place(perc,soft_clap()*.34,b*BEAT)
    for s in (7,15,23,31,39,47,55,63):place(perc,rim()*.22,swing(s))
    for s,f in ((10,330),(26,392),(42,330),(58,294)):place(perc,conga(f)*.2,swing(s))
    roots=[33,29,36,31];chords=[(57,60,64,67,71),(53,57,60,64,67),(60,64,67,71,74),(55,59,62,66,69)]
    for bar in range(4):
        r=mf(roots[bar]+12)
        for s in range(16):
            if s%4 in (2,3):
                at=bar*4*BEAT+swing(s);L_=STEP*2.6;tt=np.arange(int(SR*L_))/SR
                x=(saw(r,tt)*.5+np.sin(2*np.pi*r*tt)*.9);x=lp(x,520,2)*np.exp(-tt*3.2)*np.sin(np.minimum(tt*900,np.pi/2));place(bass,x*(1.0 if s%4==2 else .7),at)
        # pad chord
        L_=4*BEAT+.4;tt=np.arange(int(SR*L_))/SR;p=np.zeros_like(tt)
        for m in chords[bar]:p+=saw(mf(m),tt,(-.012,-.006,.006,.012))*.075
        env=np.minimum(tt/.35,1)*np.minimum((L_-tt)/.4,1);p=lp(p,3200,2)*env;place(pad,p,bar*4*BEAT-.05)
        # arp pluck
        notes=[chords[bar][i%4]+12 for i in (0,2,1,3,2,1,3,2)]
        for k in range(16):
            if k%8 in (0,3,6) or k%2==1 or True:
                if (k%8) in (1,5,7):continue
                m=notes[k%8]+(12 if k%8==4 else 0);at=bar*4*BEAT+swing(k)*1.0
                tt=np.arange(int(SR*.4))/SR;x=saw(mf(m),tt,(-.004,.004))*np.exp(-tt*11);x=lp(x,3200,2);place(arp,x*.26,at)

    lead=np.zeros(N)
    M=[[(0,76,1.5),(1.5,81,.5),(2,79,1),(3,76,1)],[(0,77,1.5),(1.5,81,.5),(2,84,1),(3,81,1)],[(0,79,1.5),(1.5,84,.5),(2,83,1),(3,79,1)],[(0,74,1),(1,79,1),(2,83,1),(3,86,1)]]
    for bar in range(4):
        for bp_,m,d in M[bar]:
            L_=d*BEAT+.5;tt=np.arange(int(SR*L_))/SR;f=mf(m)
            x=saw(f,tt,(-.005,.005))*.55+np.sin(2*np.pi*f*tt)*.7+np.sin(2*np.pi*2*f*tt)*.15
            env=np.minimum(tt/.015,1)*np.exp(-np.clip(tt-d*BEAT*.5,0,None)*3.0)*np.minimum(np.clip(L_-tt,0,None)/.25,1)
            place(lead,lp(x,5000,2)*env*.24,bar*4*BEAT+bp_*BEAT)
    leadd=lead+.5*np.roll(lead,int(BEAT*.75*SR))+.3*np.roll(lead,int(BEAT*1.5*SR))

    snr=np.zeros(N)
    def snare():
        tt=np.arange(int(SR*.2))/SR;return (bp(rng.standard_normal(len(tt)),1800,9000,2)*np.exp(-tt*22)*.7+np.sin(2*np.pi*190*tt)*np.exp(-tt*30)*.4)
    for k in range(8):place(snr,snare()*(.35+.08*k),(4.0*2*BEAT/4*0)+ (8*BEAT)+k*BEAT)  # 8ths? beats 8..15
    for k in range(16):place(snr,snare()*(.25+.04*k),12*BEAT+k*BEAT/4*1.0*0+k*BEAT/4) if False else None
    for k in range(8):place(snr,snare()*(.5+.06*k),14*BEAT+k*BEAT/4)
    # delay (circular, dotted 8th ping-pong) on arp
    dl=int(BEAT*.75*SR);arpd=arp+.45*np.roll(arp,dl)+.25*np.roll(arp,2*dl)
    # fx subtle
    place(fx,lp(rng.standard_normal(int(SR*1.5)),150)*np.exp(-np.arange(int(SR*1.5))/SR*3.0)*.9,0)
    tt=np.arange(int(SR*2.2))/SR;nz=rng.standard_normal(len(tt));sw_=np.zeros_like(nz)
    for i in range(20):
        a,b=i/20,(i+1)/20;fc=400*(12**a);seg=slice(int(a*len(tt)),int(b*len(tt)));sw_[seg]=bp(nz,fc,fc*1.7,2)[seg]
    place(fx,sw_*(tt/2.2)**2*.45,DUR-2.2)
    if style=='eye':
        for c in (.50,.572):
            tc=c*DUR;tt=np.arange(int(SR*.09))/SR;place(fx,lp(rng.standard_normal(len(tt)),3500)*np.exp(-tt*50)*.5,tc);place(fx,np.sin(2*np.pi*(70-200*tt)*tt)*np.exp(-tt*25)*.45,tc)
        for c in (.25,.75):
            tc=c*DUR;tt=np.arange(int(SR*.04))/SR;place(fx,np.sign(np.sin(2*np.pi*tt*1200))*.1*np.exp(-tt*60),tc)
    else:
        for k in range(4):
            tt=np.arange(int(SR*1.6))/SR;f=mf(81 if k%2==0 else 76);place(fx,np.sin(2*np.pi*f*tt)*np.exp(-tt*3.2)*np.minimum(tt/.01,1)*.10,k*2.0+.5*BEAT)
    drums=kd*1.05+hats*.6+perc*.75+snr*.7
    bus=drums+bass*sc*.9+pad*sc*1.5+arpd*sc*.8+leadd*sc*.9+fx*.5
    chs=[]
    for ch,seed in ((0,3),(1,4)):
        w=reverb(pad*sc*1.5+arpd*.7+fx*.5+perc*.3,2.4,seed,.6)
        x=bus+w*.5;sh=int(.0006*SR)*(1 if ch==0 else -1);x=x+np.roll(hats,sh)*.1+np.roll(arpd,sh*6)*.08;chs.append(x)
    y=np.stack(chs,1);y=hp(y.T,30,2).T;y=np.tanh(y*1.1)/np.tanh(1.1)
    rms=np.sqrt(np.mean(y**2));y=y*(0.075/rms);pk=np.max(np.abs(y))
    if pk>.8:y=y*(.8/pk)
    print(style,'rms dBFS',20*np.log10(np.sqrt(np.mean(y**2))),'peak',20*np.log10(np.max(np.abs(y))))
    pcm=(y*32767).astype('<i2')
    with wave.open(outp,'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
if __name__=='__main__':
    mix3('eye','/tmp/gloopy/d_eye.wav');mix3('sinal','/tmp/gloopy/d_sinal.wav')
