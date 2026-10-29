"""Uso: python _herramientas/estudio/transcribir.py grabacion.mp4 salida.srt"""
import os
os.environ['HF_HUB_OFFLINE'] = '1'
import sys
from pathlib import Path
from faster_whisper import WhisperModel
model_path = Path('/workspace/modelos-reels/faster-whisper-small')
if not (model_path / 'model.bin').is_file():
    sys.exit('Falta descargar el modelo de voz. Consulta COMO-FUNCIONA.md.')
model = WhisperModel(str(model_path), device='cpu', compute_type='int8', cpu_threads=2, local_files_only=True)
segments, info = model.transcribe(sys.argv[1], beam_size=5, word_timestamps=True)
def stamp(t):
    ms = round(t * 1000)
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{ms:03}'
with open(sys.argv[2], 'w', encoding='utf-8') as out:
    for i, segment in enumerate(segments, 1):
        out.write(f'{i}\n{stamp(segment.start)} --> {stamp(segment.end)}\n{segment.text.strip()}\n\n')
print('Subtítulos guardados en', sys.argv[2])
