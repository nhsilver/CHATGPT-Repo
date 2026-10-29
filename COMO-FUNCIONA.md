# Mi estudio de reels

Todo lo preparado aquí funciona con herramientas gratuitas. No se ha creado ninguna cuenta, contratado un servicio ni utilizado una clave de pago.

## Dónde colocar cada cosa

- `material grabado/`: vídeos originales. Conserva siempre una copia sin editar.
- `referencias/`: ejemplos, música y recursos que tengas permiso para usar.
- `resultados/`: proyectos, subtítulos y archivos intermedios.
- `3 Listos/`: vídeos terminados.
- `_herramientas/`: repositorios descargados y ayudantes del estudio.

La raíz de trabajo es `/workspace/CHATGPT-Repo`. Cada tarea de nube ya está aislada: usa esta carpeta, sin crear otro worktree de Git.

## Qué está disponible

| Herramienta | Estado y uso |
| --- | --- |
| FFmpeg y ffprobe 7.1.5 | Ya estaban instalados; montaje, conversión, audio, subtítulos y comprobación de exportaciones. |
| Node.js 24.19.0 | Ya estaba instalado; cumple el mínimo de 22. |
| Python 3.12.14 | Ya estaba instalado. |
| faster-whisper 1.2.1 | Instalado en `/workspace/reels-venv`; falta descargar el modelo de voz por el bloqueo de red. Todavía no se ha validado una transcripción. |
| rembg 2.0.86 y ONNX Runtime para CPU | Instalados; modelo `u2net_human_seg` descargado en `/workspace/modelos-reels/rembg`, verificado con la suma oficial y ejecutado sin red sobre una imagen de prueba. Falta probar la calidad con una foto real tuya. |
| yt-dlp 2026.10.26 | Instalado con dependencias recomendadas; el comando de versión funciona. No se ha probado una descarga de una plataforma. |

Las dependencias Python y sus versiones exactas están en `_herramientas/estudio/requirements.txt`. El entorno Python y los modelos están fuera del repositorio para no subir miles de archivos ni modelos pesados a GitHub.

## Para qué sirven las guías descargadas

- **reels-montage:** guía para cortar pausas y retomas, organizar el ritmo y colocar subtítulos. Copia en `_herramientas/reels-montage`.
- **HyperFrames:** composición y animación de vídeos con HTML. Copia en `_herramientas/hyperframes`.
- **Media Use:** guía incluida en `hyperframes/skills/media-use` para preparar audio, transcripciones y recortes. Elegiremos sus alternativas locales gratuitas.
- **Skills de Remotion:** consulta de buenas prácticas para animaciones y subtítulos. Copia en `_herramientas/remotion-skills`.
- **yt-dlp:** descarga de referencias utilizables legalmente. Fuente en `_herramientas/yt-dlp`.

Las guías están descargadas y leídas; no están registradas automáticamente como plugins del cliente. No he instalado el motor de Remotion, Claude Code ni los servicios online de HeyGen. Remotion tiene condiciones de licencia según el usuario o empresa; antes de usar una opción que requiera pago o cuenta, hay que consultarte. La prueba usa solamente FFmpeg.

## Empezar una sesión

```bash
cd /workspace/CHATGPT-Repo
source _herramientas/estudio/activar.sh
```

Activa Python y señala dónde está el modelo de personas. No hace falta mantener un servidor abierto.

### Recortarte de una imagen

```bash
rembg i -m u2net_human_seg 'material grabado/foto.jpg' 'resultados/persona.png'
```

El PNG conserva la transparencia. Para un vídeo hay que separar fotogramas, recortarlos con el mismo modelo y recomponerlos con su audio; puede tardar bastante en CPU. El borde se debe revisar con tu grabación real.

### Transcribir gratis y sin internet

**Pendiente:** la red bloqueó la descarga inicial desde Hugging Face. Se guardó un borrador de acceso a `huggingface.co` y `cas-bridge.xethub.hf.co`; eso no cambia automáticamente la red activa. Revisa y guarda esos dominios en los ajustes del entorno y publica los cambios cuando corresponda. No hace falta una cuenta de Hugging Face para este modelo público.

Con el acceso habilitado, ejecutar una sola vez (necesita internet):

```bash
source _herramientas/estudio/activar.sh
python _herramientas/estudio/descargar-voz.py
```

Descarga el modelo multilingüe `small`, útil para español, aproximadamente 500 MB. Este paso aún no se ha completado ni verificado. Si la descarga pide otro dominio, debe revisarse el error antes de añadirlo.

Después, transcribir localmente:

```bash
python _herramientas/estudio/transcribir.py 'material grabado/video.mp4' 'resultados/subtitulos.srt'
```

El ayudante fuerza el modo sin internet y usa CPU. Si falta el modelo, muestra un aviso en vez de intentar descargarlo. Revisa nombres propios y sincronización antes de publicar.

### Descargar una referencia

```bash
yt-dlp --js-runtimes node -P referencias 'URL_DEL_VIDEO'
```

Requiere internet y acceso al sitio. Si pide pago, clave o cuenta, parar y consultarte. No se han habilitado dominios de plataformas de vídeo indiscriminadamente.

## La prueba real

`3 Listos/prueba-reel-5s.mp4`: 1080 × 1920, 30 fps, H.264, cinco segundos exactos, subtítulo con entrada, fundido y resaltado progresivo de palabras. Incluye una pista de audio silenciosa; no contiene locución ni material tuyo porque aún no hay grabaciones.

Se verificaron dimensiones y duración con ffprobe, se decodificó completo sin errores y se revisó un fotograma. Fuente editable del subtítulo: `resultados/prueba/subtitulos.ass`.

Para volver a generarlo (sobrescribe únicamente el MP4 de prueba):

```bash
bash resultados/prueba/crear-prueba.sh
```

## Si falta algo: restaurar el estudio

En este entorno Linux, con Python 3.12, Node.js 22 o superior, Git, curl, FFmpeg con libass y la fuente DejaVu Sans disponibles:

```bash
cd /workspace/CHATGPT-Repo
bash _herramientas/estudio/preparar.sh
source _herramientas/estudio/activar.sh
```

El script reinstala las versiones Python registradas, comprueba el modelo de personas y recupera los repositorios ausentes sin sustituir copias existentes. Se probó una segunda ejecución satisfactoria con las dependencias ya instaladas. Recupera la versión actual de cada guía; sus revisiones de esta sesión están en `_herramientas/estudio/repositorios.txt`.

Si faltan herramientas del sistema, en Debian/Ubuntu una persona con permisos de administración puede instalar `ffmpeg`, `fonts-dejavu-core`, `python3-venv`, `git` y `curl` con apt. Para Node usa una distribución oficial de versión 22 o superior. No desactives las verificaciones TLS ni de modelos para solucionar errores.

El modelo de voz se descarga aparte con el comando anterior: la preparación básica no oculta ese pendiente. Si se pierde `/workspace`, también deben recuperarse estos ayudantes y tus vídeos desde una copia de seguridad. Las carpetas del estudio se guardan en GitHub; las herramientas externas se incluyen como submódulos. Para recuperarlas tras clonar, ejecuta `git submodule update --init --recursive`. Los modelos y el entorno Python se restauran por separado con las instrucciones anteriores. Publicar el entorno guarda su estado preparado, pero los procesos no sobreviven y la transcripción seguirá pendiente hasta descargar y probar su modelo.

## Última revisión del estudio

Se volvió a ejecutar la preparación: dependencias sin conflictos, modelo de personas con suma correcta, Node.js 24, Python 3.12 y yt-dlp disponibles. El vídeo conserva sus dimensiones 1080 × 1920 y cinco segundos. Después se sincronizaron seis grabaciones nuevas desde GitHub.

Se reintentó la descarga real del modelo de voz y el acceso continúa bloqueado. Los dominios están guardados en el borrador, pero no figuran en la configuración activa. Falta revisar y guardar ese cambio en ajustes y publicar el entorno. Hasta descargar y probar el modelo, la transcripción sin internet no está lista.

## Mi ficha de estilo y la demo

La ficha `2 Mi estilo/mi-estilo.md` tiene aprobación provisional. Antes de cada edición hay que recordar las tres opciones de arranque, recomendar una y dejar que el usuario elija. El cierre se elige entre conclusión con acción y bucle según el vídeo.

La demo original de 30 segundos está en `3 Listos/demo-mi-estilo-provisional.mp4`. Usa las fuentes gratuitas Libre Baskerville y Montserrat, voz española sintética de eSpeak NG y música original generada localmente. Se reproduce con `python resultados/demo-estilo/crear-demo.py` después de activar el entorno. Es una prueba de estilo con gráficos, no una edición de material grabado del usuario. Las fuentes y sus licencias se conservan en `resultados/demo-estilo/fuentes`.

También está `3 Listos/demo-estilo-grabaciones.mp4`: montaje visual de 30 segundos con las seis grabaciones nuevas, música original y rótulos editoriales. No incluye el diálogo de cámara ni pretende transcribirlo. Se reproduce con `python resultados/demo-estilo/crear-montaje-real.py`.
