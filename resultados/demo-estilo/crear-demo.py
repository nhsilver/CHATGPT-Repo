"""Demo original, local y gratuita. Ejecutar desde la raíz del repositorio."""
from pathlib import Path
import ctypes as C
import math
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import espeakng_loader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'resultados/demo-estilo'
W,H,FPS,DURATION = 720,1280,30,30
CREAM='#FFF4B0'; WHITE='#FFFFFF'; BG='#181818'
scenes=[
 ('Una idea.', 'Más impacto.', 'Así puede verse tu próximo vídeo.', ['Así puede verse','tu próximo','vídeo.']),
 ('Elegancia', 'con ritmo.', 'Elegante, pero con ritmo y personalidad.', ['Elegante,','pero con ritmo','y personalidad.']),
 ('Lo importante', 'se nota.', 'Las palabras importantes destacan sin competir.', ['Las palabras','importantes','destacan sin competir.']),
 ('Menos ruido.', 'Más intención.', 'Lo demás acompaña y deja respirar.', ['Lo demás','acompaña','y deja respirar.']),
 ('Cada cambio', 'aporta.', 'Cambiamos el plano cuando aporta algo.', ['Cambiamos el plano','cuando aporta','algo.']),
 ('Acércate', 'al detalle.', 'Un acercamiento suave dirige la mirada.', ['Un acercamiento','suave','dirige la mirada.']),
 ('Tu voz', 'primero.', 'Tu voz siempre se entiende con claridad.', ['Tu voz','siempre se entiende','con claridad.']),
 ('La música', 'acompaña.', 'La música acompaña y respira contigo.', ['La música','acompaña','y respira contigo.']),
 ('Un estilo.', 'Tu identidad.', 'Una identidad coherente, sin efectos de más.', ['Una identidad','coherente,','sin efectos de más.']),
 ('Una idea.', 'Más impacto.', 'Y todo vuelve a una buena idea.', ['Y todo vuelve','a una buena','idea.']),
]

def font(name,size,weight):
 f=ImageFont.truetype(str(OUT/'fuentes'/name),size)
 f.set_variation_by_axes([weight])
 return f
serif=font('LibreBaskerville.ttf',43,400)
bold=font('Montserrat.ttf',54,800)
heading=font('Montserrat.ttf',66,800)
small=font('Montserrat.ttf',19,600)
tiny=font('Montserrat.ttf',15,500)

# eSpeak NG: síntesis local española. Es voz de prueba, no imita al usuario.
lib=espeakng_loader.load_library()
lib.espeak_Initialize.argtypes=[C.c_int,C.c_int,C.c_char_p,C.c_int]
lib.espeak_Initialize.restype=C.c_int
sr=lib.espeak_Initialize(2,0,espeakng_loader.get_data_path().encode(),0)
assert sr>0
lib.espeak_SetVoiceByName(b'es')
lib.espeak_SetParameter(1,175,0)
CB=C.CFUNCTYPE(C.c_int,C.POINTER(C.c_short),C.c_int,C.c_void_p)
chunks=[]
@CB
def callback(samples,count,events):
 if count and samples: chunks.append(np.ctypeslib.as_array(samples,shape=(count,)).copy())
 return 0
lib.espeak_SetSynthCallback(callback)
lib.espeak_Synth.argtypes=[C.c_void_p,C.c_size_t,C.c_uint,C.c_int,C.c_uint,C.c_uint,C.c_void_p,C.c_void_p]
voice=np.zeros(sr*DURATION,dtype=np.float64)
for i,scene in enumerate(scenes):
 chunks.clear()
 text=scene[2].encode('utf-8')
 assert lib.espeak_Synth(text,len(text)+1,0,1,0,1,None,None)==0
 lib.espeak_Synchronize()
 a=np.concatenate(chunks).astype(np.float64)/32768
 if len(a)>int(sr*2.75):
  a=np.interp(np.linspace(0,len(a)-1,int(sr*2.75)),np.arange(len(a)),a)
 start=int((i*3+.08)*sr)
 voice[start:start+len(a)]+=a
voice *= .78/max(np.max(np.abs(voice)),1e-6)
# Música original: acordes suaves y pulso discreto, sin archivos de terceros.
t=np.arange(sr*DURATION)/sr
music=np.zeros_like(t)
for j,freqs in enumerate([(220,261.63,329.63),(174.61,220,261.63),(130.81,164.81,196),(196,246.94,293.66),(220,261.63,329.63)]):
 mask=(t>=j*6)&(t<(j+1)*6)
 u=t[mask]-j*6
 env=np.minimum(u/0.3,1)*np.minimum((6-u)/0.5,1)
 music[mask]=sum(np.sin(2*np.pi*f*u)+.13*np.sin(2*np.pi*2*f*u) for f in freqs)*env/3
music += .10*np.sin(2*np.pi*65.4*t)*np.exp(-((t%.625)*13))
# Ducking con ventana RMS: -21 dB respecto al RMS vocal, +4.5 dB en pausas.
window=max(1,int(sr*.08))
level=np.sqrt(np.convolve(np.pad(voice**2,(window//2,window//2)),np.ones(window)/window,mode='valid')[:len(t)])
active=level>.012
vrms=np.sqrt(np.mean(voice[active]**2))
music*=vrms*10**(-21/20)/np.sqrt(np.mean(music**2))
gain=np.where(active,1.,10**(4.5/20))
k=np.ones(int(sr*.12))/int(sr*.12)
gain=np.convolve(np.pad(gain,(len(k)//2,len(k)//2),mode='edge'),k,mode='valid')[:len(t)]
fade=np.minimum(t/.08,1)*np.minimum((DURATION-t)/.08,1)
mix=(voice+music*gain)*fade
assert np.max(np.abs(mix))<1
with wave.open(str(OUT/'mezcla.wav'),'wb') as f:
 f.setparams((1,2,sr,0,'NONE','not compressed'))
 f.writeframes((mix*32767).astype('<i2').tobytes())
print('Audio local generado. Pico:',round(float(np.max(np.abs(mix))),3),flush=True)

def center(d,text,y,f,fill):
 box=d.textbbox((0,0),text,font=f)
 d.text(((W-(box[2]-box[0]))/2,y),text,font=f,fill=fill,stroke_width=0)

def frame(t):
 i=min(9,int(t/3)); u=t-i*3
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
 d.text((54,55),'ESTILO / EN PRUEBA',font=small,fill=CREAM)
 d.text((588,57),f'{i+1:02}/10',font=small,fill=WHITE)
 d.line((54,101,666,101),fill='#45443D',width=1)
 # Entrada breve y controlada de los titulares.
 shift=round(14*(1-min(u/.2,1))**2)
 center(d,scenes[i][0],142+shift,heading,WHITE)
 center(d,scenes[i][1],220+shift,heading,CREAM)
 # Gráficos originales que ilustran cada decisión de montaje.
 panel=Image.new('RGB',(612,420),'#24241F'); q=ImageDraw.Draw(panel)
 if i in (0,9):
  q.text((38,32),'EL RESULTADO',font=small,fill=CREAM)
  q.text((38,94),'Una buena',font=serif,fill=WHITE)
  q.text((38,160),'IDEA',font=heading,fill=CREAM)
  for n,label in enumerate(['RITMO','CONTRASTE','CLARIDAD']):
   y=282+n*37
   q.line((38,y+10,100+int(190*min((u+.2+n*.2)/1.2,1)),y+10),fill=CREAM,width=3)
   q.text((346,y-1),label,font=tiny,fill=WHITE)
 elif i in (1,4):
  q.text((38,32),'CADA CAMBIO TIENE UN MOTIVO',font=small,fill=CREAM)
  for n,label in enumerate(['PLANO','DETALLE','ZOOM SUAVE']):
   x=38+n*180
   q.rounded_rectangle((x,112,x+166,247),radius=10,fill=CREAM if n==int(u)%3 else '#424237')
   q.text((x+10,157),label,font=tiny,fill=BG if n==int(u)%3 else WHITE)
   q.text((x+10,262),f'{n*3:02} s',font=small,fill=WHITE)
  q.line((38,333,574,333),fill='#88846A',width=2)
  x=38+int(536*u/3)
  q.line((x,313,x,353),fill=CREAM,width=3)
 elif i in (2,3,8):
  q.text((38,32),'JERARQUÍA QUE SE ENTIENDE',font=small,fill=CREAM)
  q.text((38,108),'Una palabra',font=serif,fill=WHITE)
  q.text((38,180),'IMPORTA',font=heading,fill=CREAM)
  q.line((38,282,574,282),fill='#666454',width=1)
  q.text((38,319),'El resto deja espacio.',font=small,fill=WHITE)
 elif i==5:
  q.text((38,32),'ACERCARSE PARA MOSTRAR',font=small,fill=CREAM)
  for n in range(5):
   q.line((80+n*104,112,80+n*104,350),fill='#4D4C3E',width=1)
  for n in range(4):
   q.line((80,112+n*79,496,112+n*79),fill='#4D4C3E',width=1)
  q.rounded_rectangle((179,151,397,309),radius=12,outline=CREAM,width=3)
  q.text((205,209),'DETALLE',font=small,fill=WHITE)
  q.line((166,137,206,137),fill=WHITE,width=2)
  q.line((166,137,166,177),fill=WHITE,width=2)
  q.line((410,322,370,322),fill=WHITE,width=2)
  q.line((410,322,410,282),fill=WHITE,width=2)
 else:
  q.text((38,32),'LA VOZ SIEMPRE DELANTE',font=small,fill=CREAM)
  q.text((38,87),'VOZ',font=tiny,fill=WHITE)
  for n in range(64):
   at=min(len(voice)-1,int((i*3+u)*sr)+n*64)
   v=abs(float(voice[at]))
   h=8+min(60,v*110)
   q.line((40+n*8,173-h,40+n*8,173+h),fill=CREAM,width=4)
  q.text((38,268),'MÚSICA DE FONDO',font=tiny,fill=WHITE)
  for n in range(64):
   h=3+7*(1+math.sin(n*.5+u*2))/2
   q.line((40+n*8,335-h,40+n*8,335+h),fill='#88846A',width=3)
 # Zoom 5–8 %, movimiento lento, sin sacudidas.
 scale=1+(.08 if i in (2,5,8) else .05)*min(u/2.7,1)
 sw,sh=round(612*scale),round(420*scale)
 panel=panel.resize((sw,sh),Image.Resampling.BICUBIC)
 panel=panel.crop(((sw-612)//2,(sh-420)//2,(sw+612)//2,(sh+420)//2))
 im.paste(panel,(54,360)); d=ImageDraw.Draw(im)
 # La palabra clave contrasta con la base editorial.
 group=min(2,int(max(0,u-.08)/.92))
 txt=scenes[i][3][group]
 key=group==1
 f=bold if key else serif
 while d.textbbox((0,0),txt,font=f)[2]>610:
  f=font('Montserrat.ttf' if key else 'LibreBaskerville.ttf',f.size-2,800 if key else 400)
 elapsed=(max(0,u-.08)%.92)
 dy=round(9*(1-min(elapsed/.18,1))**2)
 center(d,txt,844+dy,f,CREAM if key else WHITE)
 # Segunda línea discreta permite comparar jerarquías.
 center(d,'Elegante. Ágil. Con intención.',970,small,'#B9B7AC')
 d.line((54,1110,666,1110),fill='#45443D',width=1)
 d.line((54,1110,54+int(612*t/30),1110),fill=CREAM,width=3)
 center(d,'DEMO ORIGINAL · VOZ SINTÉTICA',1150,tiny,'#B9B7AC')
 # Un breve hold idéntico en ambos extremos hace visible la conexión del bucle.
 return im

cmd=['ffmpeg','-hide_banner','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(OUT/'mezcla.wav'),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','30','-movflags','+faststart',str(ROOT/'3 Listos/demo-mi-estilo-provisional.mp4')]
with open(OUT/'render.log','w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 try:
  for n in range(FPS*DURATION):
   p.stdin.write(frame(n/FPS).tobytes())
   if n%150==0: print(f'Vídeo: {n//FPS}/30 segundos',flush=True)
 finally:
  p.stdin.close()
 assert p.wait()==0,'Falló FFmpeg: consultar render.log'
frame(7.3).save(OUT/'vista-previa.jpg')
print('Demo terminada.',flush=True)
