import numpy as np,subprocess,wave
from scipy.signal import butter,sosfilt,fftconvolve
SR=44100;DUR=8.0;N=int(SR*DUR);BPM=120;BEAT=60/BPM
rng=np.random.default_rng(11)
t=np.arange(N)/SR
def lp(x,f,o=4):return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=4):return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def bp(x,a,b,o=3):return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
def place(buf,sig,at):
    i=int(at*SR);n=len(sig)
    for k in (0,):  # circular wrap so the loop is seamless
        idx=(np.arange(n)+i)%N;buf[idx]+=sig
def kick(L=.45):
    tt=np.arange(int(SR*L))/SR;f=45+120*np.exp(-tt*32);ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*np.exp(-tt*7.5)+.35*np.sin(2*ph)*np.exp(-tt*18))*1.0+np.where(tt<.003,.6,0)*np.exp(-tt*900)
def hat(L=.07,open_=False):
    L=.28 if open_ else L;tt=np.arange(int(SR*L))/SR;return hp(rng.standard_normal(len(tt)),7500)*np.exp(-tt*(16 if open_ else 70))*.5
def clap(L=.25):
    tt=np.arange(int(SR*L))/SR;n=bp(rng.standard_normal(len(tt)),900,6000)
    env=sum(np.exp(-np.clip(tt-d,0,None)*60)*(tt>=d) for d in (0,.012,.024))*.35+np.exp(-tt*16)*.5;return n*env*.6
def whoosh(L,up=True):
    tt=np.arange(int(SR*L))/SR;n=rng.standard_normal(len(tt));out=np.zeros_like(n);steps=24
    for i in range(steps):
        a,b=i/steps,(i+1)/steps;fc=300*(40**(a if up else 1-a));seg=slice(int(a*len(tt)),int(b*len(tt)))
        out[seg]=bp(n,fc,min(fc*1.8,SR/2-100),2)[seg]
    env=np.sin(np.pi*np.clip(tt/L,0,1))**2;return out*env*1.2
def sine_ping(f,L=1.6,a=.35):
    tt=np.arange(int(SR*L))/SR;return (np.sin(2*np.pi*f*tt)+.25*np.sin(2*np.pi*2*f*tt))*np.exp(-tt*3.2)*a
def reverb(x,L=1.8,seed=1,wet=.35):
    r=np.random.default_rng(seed);n=int(SR*L);ir=r.standard_normal(n)*np.exp(-np.arange(n)/SR*3.2);ir=lp(ir,6000,2)
    X=np.fft.rfft(x);Hh=np.fft.rfft(ir/np.sqrt(np.sum(ir**2)),len(x));y=np.fft.irfft(X*Hh,len(x))  # circular -> seamless
    return x*(1-wet*.5)+y*wet
def mix(style,out_wav):
    L=np.zeros(N);Rr=np.zeros(N)
    kd=np.zeros(N);dr=np.zeros(N);fx=np.zeros(N)
    for b in range(16):place(kd,kick(),b*BEAT)
    # sidechain curve from kicks
    sc=np.ones(N)
    for b in range(16):
        i=int(b*BEAT*SR);idx=(np.arange(int(.32*SR))+i)%N;sc[idx]=np.minimum(sc[idx],1-.85*np.exp(-np.arange(int(.32*SR))/SR*9))
    # rolling bass (offbeat) A1/G1
    bass=np.zeros(N);notes=[55,55,55,61.7,55,55,49,55]
    for k in range(16):
        f=notes[k%8];at=k*BEAT+BEAT/2;L_=BEAT*.42;tt=np.arange(int(SR*L_))/SR
        s=(2*((tt*f)%1)-1)*.6+np.sin(2*np.pi*f*tt)*.7;s=lp(s,420,2)*np.exp(-tt*3.5)*.55
        place(bass,s,at)
    # pad chord Am9, slow LFO (period 8s -> loop safe)
    pad=np.zeros(N)
    for f in (110,164.8,220,261.6,329.6):
        for det in (-.004,0,.004):pad+=np.sin(2*np.pi*f*(1+det)*t+rng.random()*6)*.04
    lf=(.5-.5*np.cos(2*np.pi*t/DUR));pad=(lp(pad,700,2)*(1-lf)+lp(pad,1800,2)*lf)*(.55+.45*np.sin(np.pi*t/DUR)**2)
    # hats
    for k in range(16):place(dr,hat(open_=True)*.8,k*BEAT+BEAT/2)
    for k in range(32):place(dr,hat()*(.35 if k%2==0 else .5),k*BEAT/2+BEAT/4*0)
    for k in (1,3,5,7,9,11,13,15):place(dr,clap(),k*BEAT)
    # riser into the loop point (last 2.5s)
    ris=whoosh(2.5,True)*.9;place(fx,ris,DUR-2.5)
    place(fx,lp(rng.standard_normal(int(SR*1.2)),160)*np.exp(-np.arange(int(SR*1.2))/SR*3)*1.2,0)  # impact at loop start
    if style=='eye':
        for c in (.50,.572):
            tc=c*DUR;place(fx,whoosh(.35,False)*.7,tc-.2);place(fx,(kick(.3)*.5),tc);place(fx,hp(rng.standard_normal(int(SR*.05)),3000)*.7,tc)
        place(fx,sine_ping(1760,1.4,.22),.0);place(fx,sine_ping(880,1.4,.16),4.0)
        # glitch bursts at .25/.75
        for c in (.25,.75):
            tc=c*DUR;g=np.sign(np.sin(2*np.pi*np.arange(int(SR*.06))/SR*900))*.25*np.exp(-np.arange(int(SR*.06))/SR*30);place(fx,g,tc)
    else:
        for k in range(4):place(fx,sine_ping(1320 if k%2==0 else 990,2.0,.30),k*2.0)
        for c in (.25,.75):place(fx,whoosh(.4,True)*.5,c*DUR-.3)
        # bleep sequence
        for k,f in enumerate([880,1320,1100,1760]):place(fx,np.sin(2*np.pi*f*np.arange(int(SR*.07))/SR)*np.exp(-np.arange(int(SR*.07))/SR*35)*.18,5.0+k*BEAT/2)
    k_=kd*1.0
    bus=k_*.95+bass*sc*1.1+pad*sc*1.0+dr*.5+fx*.8
    stereo=[]
    for ch,seed in ((0,3),(1,4)):
        w=reverb(pad*sc+fx*.6+dr*.4,2.0,seed,.55)
        x=bus*.9+w*.55
        if ch==0:x=x+np.roll(dr,int(.0007*SR))*.15
        else:x=x+np.roll(dr,-int(.0007*SR))*.15
        stereo.append(x)
    y=np.stack(stereo,1);y=hp(y.T,28,2).T
    y=np.tanh(y*1.25)/np.tanh(1.25);y=y/np.max(np.abs(y))*0.89
    pcm=(y*32767).astype('<i2')
    with wave.open(out_wav,'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
if __name__=='__main__':
    mix('eye','./a_eye.wav');mix('sinal','./a_sinal.wav');print('ok')
