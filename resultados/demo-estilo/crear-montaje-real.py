"""Prueba visual sobre grabaciones reales: rótulos editoriales, sin transcribir ni reutilizar el diálogo."""
from pathlib import Path
import math,subprocess,wave
import numpy as np
from PIL import Image,ImageFont,ImageDraw
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'resultados/demo-estilo'
clips=sorted((ROOT/'1 Brutos').glob('WhatsApp*.mp4'))
# Resultado, preparación y vuelta al resultado. Solo se leen los originales.
plan=[(3,.3,'Un día','diferente.'),(5,19,'Todo empieza','con una idea.'),(1,1,'Elegir.','Probar.'),(1,7,'Mirar','los detalles.'),(4,.4,'Dar forma','a la idea.'),(4,7,'Un toque','personal.'),(0,.3,'Los detalles','importan.'),(5,9,'Y también','la actitud.'),(2,7,'Un cambio','de mirada.'),(2,10.8,'Un poco','de juego.'),(5,15,'Todo cobra','sentido.'),(3,.3,'Un día','diferente.')]
def font(name,size,weight):
 f=ImageFont.truetype(str(OUT/'fuentes'/name),size); f.set_variation_by_axes([weight]); return f
base=font('LibreBaskerville.ttf',64,400); bold=font('Montserrat.ttf',80,800)
outputs=[]
for i,(idx,start,line,key) in enumerate(plan):
 im=Image.new('RGBA',(1080,1920)); d=ImageDraw.Draw(im)
 for txt,y,f,c in [(line,1260,base,'white'),(key,1350,bold,'#FFF4B0')]:
  x=(1080-d.textbbox((0,0),txt,font=f)[2])/2
  d.text((x,y),txt,font=f,fill=c,stroke_width=3,stroke_fill='#181818')
 overlay=OUT/f'rotulo-{i:02}.png'; im.save(overlay)
 out=OUT/f'parte-{i:02}.mp4'; outputs.append(out)
 # Encuadre vertical normalizado; zoom leve solo en segmentos seleccionados.
 zoom='1+0.0006*on' if i in (2,5,8) else '1'
 filt=f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,zoompan=z={zoom}:x=iw/2-iw/zoom/2:y=ih/2-ih/zoom/2:d=1:s=1080x1920:fps=30[v];[v][1:v]overlay=x=0:y=8*(1-min(t/0.18\\,1)):eval=frame,format=yuv420p[out]'
 cmd=['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(clips[idx]),'-loop','1','-i',str(overlay),'-filter_complex',filt,'-map','[out]','-an','-t','2.5','-r','30','-c:v','libx264','-preset','fast','-crf','20','-threads','2',str(out)]
 subprocess.run(cmd,check=True)
 print(f'Plano {i+1}/12',flush=True)
# Música original instrumental, sin servicios externos ni diálogo no verificado.
sr=44100;t=np.arange(sr*30)/sr; a=np.zeros_like(t)
for j,freqs in enumerate([(220,261.63,329.63),(174.61,220,261.63),(130.81,164.81,196),(196,246.94,293.66),(220,261.63,329.63)]):
 m=(t>=j*6)&(t<(j+1)*6); u=t[m]-j*6
 a[m]=sum(np.sin(2*np.pi*f*u) for f in freqs)/3*np.minimum(u/.2,1)*np.minimum((6-u)/.3,1)
a+=.15*np.sin(2*np.pi*65.4*t)*np.exp(-((t%.625)*12))
a*=.25/max(abs(a));a*=np.minimum(t/.1,1)*np.minimum((30-t)/.1,1)
with wave.open(str(OUT/'musica-original.wav'),'wb') as w:
 w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes((a*32767).astype('<i2').tobytes())
listing=OUT/'montaje.txt';listing.write_text(''.join(f"file '{p.name}'\n" for p in outputs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(OUT/'musica-original.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-t','30','-movflags','+faststart',str(ROOT/'3 Listos/demo-estilo-grabaciones.mp4')],check=True)
for p in outputs:p.unlink()
for p in OUT.glob('rotulo-*.png'):p.unlink()
listing.unlink()
print('Montaje real terminado.',flush=True)
