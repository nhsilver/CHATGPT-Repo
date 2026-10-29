# Demo de estilo provisional

Salida: `3 Listos/demo-mi-estilo-provisional.mp4`, 30 segundos, 1080 × 1920 a 30 fps.

El usuario eligió resultado primero. Se propone cierre conectado con el inicio. Gráficos y textos originales; sin marcas ni mensajes de los vídeos de referencia.

La demo permite revisar paleta, tipografías, jerarquía, subtítulos cortos, cambios cada tres segundos, acercamientos de 5–8 % y voz por encima de la música. Usa Libre Baskerville y Montserrat con licencia SIL OFL (copias en `fuentes`). La voz española de prueba se sintetiza localmente con eSpeak NG, sin cuenta, imitación de voz ni servicios externos; es deliberadamente una voz de prueba y no representa el timbre final del usuario. La música es una composición sintética original de acordes y pulso generada por el script.

No hay planos de una persona: esta prueba no valida la colocación de subtítulos sobre tu cara, ropa o producto. Tampoco sustituye una revisión auditiva humana; escucha el MP4 para decidir si el carácter y los niveles te gustan.

Reproducir desde la raíz del repositorio, con FFmpeg y el entorno Python preparado:

```bash
source _herramientas/estudio/activar.sh
python resultados/demo-estilo/crear-demo.py
```

El script sobrescribe solo sus archivos de demo. Requiere Pillow, NumPy y espeakng-loader, incluidos en el registro de dependencias del estudio. `mezcla.wav` es la mezcla local reutilizable. `vista-previa.jpg` muestra una imagen de la demo.

## Prueba sobre tus grabaciones

Al sincronizar GitHub aparecieron seis vídeos nuevos en `1 Brutos`. La segunda prueba, `3 Listos/demo-estilo-grabaciones.mp4`, usa esas imágenes: 12 planos de 2,5 segundos, encuadre vertical, rótulos con las dos tipografías, blanco/crema y tres acercamientos suaves. Empieza mostrando el resultado y conecta el cierre con ese mismo momento.

Los rótulos son textos editoriales originales, **no una transcripción de lo dicho**. No se reutilizó el audio de cámara porque no se ha verificado su contenido: esta versión lleva solo la música instrumental original. El equilibrio música/voz se puede valorar por separado en la demo gráfica con voz sintética. Los originales no se modifican.

Recrear: `python resultados/demo-estilo/crear-montaje-real.py`. El script usa temporalmente archivos `parte-*`, `rotulo-*` y `montaje.txt` dentro de esta carpeta; los elimina al terminar correctamente. La música original se conserva como `musica-original.wav`.
