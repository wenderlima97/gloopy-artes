import sys;sys.path.insert(0,'/tmp/gloopy')
from render3 import *
which=sys.argv[1]
if which=='posts':
    P14=dict(POST,flavor='neo',title='olha de novo.',titleSize=112,sub='NÃO PISCA.',tagR='Nº 014')
    P15=dict(POST,scene='text',flavor='lime',title=['algo está','em loop.'],titleSize=140,titleY=980,cy=520,sub='O DROP É DOCE.',tagR='Nº 015',symR=170,spiralScale=17)
    P16=dict(POST,flavor='lime',title='me olha.',sub='O DOCE DO AFTER.',tagR='Nº 016')
    for n,c in (('post-14',P14),('post-15',P15),('post-16',P16)):still(c,.3,f'/tmp/gloopy/{n}.png')
elif which=='eye':video(EYE,'eye')
else:video(SIG,'sig')
print('done',which)
