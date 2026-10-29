from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[2]; project=Path(__file__).resolve().parent
assets=project/'assets';assets.mkdir(exist_ok=True)
parts=project/'partes';parts.mkdir(exist_ok=True)
sources=sorted((project/'fuentes-trabajo').glob('*.mp4'))
plan=[(4,5.,3.,'Aplicación de labial sobre el rosa'),(4,9.,3.,'Vestido rosa transformado'),(1,2.,3.,'Eva preparando el maniquí'),(5,10.,3.,'Equipo y detalles en el espejo'),(5,13.,3.,'Espejo y resultado')]
paths=[];manifest=[]
for i,(source,start,duration,reason) in enumerate(plan):
 out=parts/f'{i:02}.mp4';paths.append(out)
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(sources[source]),'-t',str(duration),'-an','-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-pix_fmt','yuv420p',str(out)],check=True)
 manifest.append({'final_start':i*3,'final_end':i*3+3,'source':sources[source].name,'source_in':start,'source_out':start+duration,'reason':reason})
 print('Plano',i+1,'/5',flush=True)
(project/'cortes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
listing=parts/'concat.txt';listing.write_text(''.join(f"file '{p.name}'\n" for p in paths))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(assets/'base.mp4')],check=True)
