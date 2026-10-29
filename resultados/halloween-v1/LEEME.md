# Halloween en evsaboutique — edición v1

El usuario aprobó explícitamente el guion `3 Listos/halloween-evsaboutique_guion_v2.md` con «Perfecto, con los videos que hay en 1 brutos, edita el video con este guion».

## Estado

Previsualización visual de 15 segundos: `3 Listos/halloween-evsaboutique_v1_PREVIA-sin-audio.mp4`. No es el máster final listo para publicar.

No hay archivos de voz preparados ni canciones o efectos en las carpetas del estudio en esta revisión. No se ha generado voz, música o efectos ni se ha reutilizado audio de las demos anteriores. El audio de cámara no contiene la locución aprobada y no se ha utilizado como sustituto. El usuario eligió terminar esta edición con su voz preparada. Falta recibir ese archivo; la previa silenciosa es únicamente un avance visual.

Los textos de la previa son rótulos del guion aprobado, con tiempos orientativos por bloques. **No son una transcripción ni subtítulos alineados a una voz que aún no se ha entregado.** La transcripción palabra a palabra y su sincronización quedan pendientes. No hay medición de -14 LUFS: el archivo es silencioso y esa medición no aplica hasta disponer de mezcla.

## Trabajo realizado

- Originales conservados; copias verificadas por SHA-256 en `fuentes-trabajo/`, excluidas de Git para no duplicar los brutos.
- Selección de planos y montaje con FFmpeg: origen y salida exactos en `cortes.json`.
- Animaciones de texto localmente con HyperFrames 0.8.216, GSAP y fuentes libres del estudio. Se utiliza Chromium instalado; no se necesita una cuenta ni renderizado de pago.
- Rótulos altos en las tomas del rosa para dejar libres las manos; bajos en los planos de Eva y espejo para dejar las caras visibles. La colocación se revisa por muestras y debe comprobarse de nuevo al incorporar la voz y los subtítulos definitivos.
- Sin recorte de fondo: se mantiene el ambiente real de la tienda. Sin correcciones de color añadidas, para conservar un aspecto natural.

## Reproducir

1. Copiar los archivos actuales de `1 Brutos/` a `fuentes-trabajo/` sin modificar los originales.
2. Con el entorno Python del estudio: `python preparar-montaje.py` desde cualquier directorio. Genera `assets/base.mp4` y `cortes.json`.
3. En esta carpeta: `npm install` para instalar la versión fijada de HyperFrames. Node 22+ y FFmpeg son requisitos.
4. Configurar `HYPERFRAMES_BROWSER_PATH` con el Chromium disponible (en esta máquina `/usr/bin/chromium`). Mantener verificación TLS y proxy del entorno.
5. Ejecutar `npm run check`, revisar sus resultados y después `npm run render`. El destino indicado es solo la previa v1; para cualquier corrección, elegir una ruta v2 nueva sin sobrescribir v1.

La instalación actual del motor está en `/workspace/reels-node`, fuera del repositorio; los comandos de esta sesión usan su ejecutable. Las dependencias npm pueden recuperarse a partir de package.json; no se suben node_modules, las copias de trabajo ni las cachés.

## Antes de publicar

- [ ] Recibir el audio de voz preparado: el usuario confirmó esta opción.
- [ ] Incorporar y alinear palabras al audio; revisar grafías y sincronización completa.
- [ ] Elegir canciones y efectos aportados o la opción de música desde Instagram, comprobando permisos.
- [ ] Mezclar con voz por encima del resto y medir -14 LUFS integrados si lleva audio.
- [ ] Revisar el vídeo completo en reproducción; la revisión por muestras y la decodificación técnica no la sustituyen.
- [ ] Confirmación del usuario de que lo ha visto entero en el móvil.

El inicio debe comprenderse sin sonido dentro de los primeros dos segundos. No añadir datos, logos o escenas de terceros. Conservar todas las versiones.
