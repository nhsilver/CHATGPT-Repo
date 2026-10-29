#!/usr/bin/env bash
set -euo pipefail
cd /workspace/CHATGPT-Repo
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) process.exit(1)'
python3 -m venv /workspace/reels-venv
/workspace/reels-venv/bin/python -m pip install -r _herramientas/estudio/requirements.txt
mkdir -p '1 Brutos' referencias resultados '3 Listos' Instrumental 'Efectos de sonido' /workspace/modelos-reels/rembg
if [ ! -f /workspace/modelos-reels/rembg/u2net_human_seg.onnx ]; then
  curl -fL --retry 2 -o /workspace/modelos-reels/rembg/u2net_human_seg.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx
fi
printf '%s\n' 'c09ddc2e0104f800e3e1bb4652583d1f  /workspace/modelos-reels/rembg/u2net_human_seg.onnx' | md5sum -c -
while read -r remote folder; do
  if [ ! -e "_herramientas/$folder" ]; then
    GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 "https://github.com/$remote.git" "_herramientas/$folder"
  fi
done <<'REPOS'
itpartypattaya/reels-montage reels-montage
heygen-com/hyperframes hyperframes
remotion-dev/skills remotion-skills
yt-dlp/yt-dlp yt-dlp
REPOS
/workspace/reels-venv/bin/python -m pip check
