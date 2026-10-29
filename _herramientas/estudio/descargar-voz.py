"""Descarga inicial gratuita. Después, la transcripción funciona sin internet."""
import sys
import httpx
from huggingface_hub import snapshot_download

try:
    snapshot_download(
        'Systran/faster-whisper-small',
        local_dir='/workspace/modelos-reels/faster-whisper-small',
        allow_patterns=['config.json', 'model.bin', 'tokenizer.json',
                        'vocabulary.json', 'preprocessor_config.json'],
    )
except httpx.ProxyError:
    sys.exit(
        'La red del entorno impide descargar el modelo de voz. '
        'Revisa y guarda los dominios de Hugging Face en los ajustes del entorno; '
        'después vuelve a ejecutar este comando. No necesitas pagar ni crear una cuenta.'
    )
print('Modelo multilingüe small descargado.')
