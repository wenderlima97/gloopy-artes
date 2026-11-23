import sys;sys.path.insert(0,'/tmp/gloopy')
from render3 import *
which=sys.argv[1]
EYE4=dict(EYE,flavor='neo',title='de olho aberto.',titleSize=112,sub='O DOCE DO AFTER.',tagL='LOTE 001',tagR='Nº 004')
if which=='posts':
    P17=dict(POST,flavor='cob',title='sem pressa.',titleSize=124,sub='O DROP É DOCE.',tagR='Nº 017')
    P18=dict(POST,scene='text',flavor='neo',title=['quase','na hora.'],titleSize=140,titleY=980,cy=520,sub='O DOCE DO AFTER.',tagR='Nº 018',symR=170,spiralScale=17)
    for n,c in (('post-17',P17),('post-18',P18)):still(c,.3,f'/tmp/gloopy/{n}.png')
elif which=='still':still(EYE4,.30,'/tmp/gloopy/t_eye4.png')
else:video(EYE4,'eye4')
print('done',which)
