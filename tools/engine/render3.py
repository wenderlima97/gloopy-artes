import sys,os
sys.path.insert(0,'/tmp/gloopy')
from engine3 import build
from playwright.sync_api import sync_playwright
def still(cfg,t,out):
    open('/tmp/_p3.html','w').write(build(cfg))
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':cfg['w'],'height':cfg['h']})
        pg.goto('file:///tmp/_p3.html');pg.wait_for_timeout(500);pg.evaluate(f'draw({t},3)');pg.wait_for_timeout(150);pg.screenshot(path=out);b.close()
def video(cfg,name,N=240):
    d=f'/tmp/gloopy/fr_{name}';os.makedirs(d,exist_ok=True)
    open(f'/tmp/_v3_{name}.html','w').write(build(cfg))
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':cfg['w'],'height':cfg['h']})
        pg.goto(f'file:///tmp/_v3_{name}.html');pg.wait_for_timeout(500)
        for i in range(N):
            pg.evaluate(f'draw({i/N},{i})');pg.screenshot(path=f'{d}/f{i:04d}.jpg',type='jpeg',quality=94)
        b.close()
STARS=[[120,330,1.6,0,'#EDEDF0'],[950,420,1.1,.3,None],[90,1180,1.0,.6,None],[980,1250,1.9,.1,'#EDEDF0'],[540,1500,.9,.8,'#EDEDF0']]
EYE=dict(w=1080,h=1920,scene='eye',flavor='lime',cy=800,eyeHW=430,eyeHH=180,title='me olha.',titleX=90,titleY=1370,titleSize=130,sub='SABOR · EM BREVE'.replace('SABOR · EM BREVE','O DOCE DO AFTER.'),tagY=1500,tagL='LOTE 001',tagR='2027',logoY=270,logoW=360,stars=STARS,spiralScale=14)
SIG=dict(EYE,scene='sinal',flavor='cob',title='sinal.',sub='O DROP É DOCE.',tagL='LOTE 001',tagR='00:00',eyeHH=170)
if __name__=='__main__':
    still(EYE,.30,'/tmp/gloopy/t_eye.png');still(SIG,.30,'/tmp/gloopy/t_sig.png')

POST=dict(EYE,h=1350,cy=600,logoY=90,logoW=340,titleY=1090,tagY=1270,static=True,noblink=True,stars=[[120,230,1.6,0,'#EDEDF0'],[960,300,1.1,.3,None],[90,900,1.0,.6,None],[980,950,1.9,.1,'#EDEDF0']],spiralScale=14)
