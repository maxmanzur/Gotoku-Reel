---
name: reel-animado
description: Crea reels verticales de motion graphics, sin cámara ni editor, a partir de una descripción. Una bola colgada de un hilo se balancea y cambia el texto en cada pasada, luego hace de linterna para descubrir la frase final y cierra con tu @ y la llamada a comentar. Renderiza el MP4 con Hyperframes (gratis, Apache-2.0). Úsala cuando pidan un reel animado, un vídeo de motion graphics para Instagram o TikTok, o «el reel de la bola».
---
# Reel animado (la bola)

Hace un reel vertical (1080×1920, 30 fps) que dura unos 9 s más 1 s por frase:
1. Una bola colgada de un hilo se balancea y, en cada pasada, el hilo cambia el texto (una frase por vaivén).
2. En la última pasada, el hilo arrastra la oscuridad. La bola sube y hace de linterna: su haz barre y descubre la frase final.
3. Vuelve la luz y cierra con el @, la píldora para comentar y «sígueme».

Cada movimiento lleva su sonido. Todo se dibuja con código: no hay vídeo grabado.

## Qué necesitas
- Node.js 18 o superior, ffmpeg y Python 3. Si falta algo, pide permiso e instálalo.
- Hyperframes se usa con `npx hyperframes` y se descarga solo la primera vez.

## Pasos
1. **Carpeta nueva:** copia la carpeta `plantilla/` de esta skill a una carpeta para el reel, por ejemplo `~/reels/<nombre>/`. No trabajes dentro de la skill.
2. **Textos y colores:** a partir de lo que pida el usuario, rellena `reel.json`.
   - `vaivenes`: de 2 a 7 frases, cada una en dos líneas cortas (11-12 letras como mucho por línea). Cuentan la idea a golpes: promesa, prueba, giro.
   - La palabra que va en color de acento se escribe entre asteriscos: `*EDITOR.*`.
   - `linterna`: tres líneas cortas (`lineas`) y la frase final en cursiva (`cursiva`).
   - `colores`: `fondo` claro, `tinta` oscura, `acento`, `oscuro` (la escena de la linterna) y `bola`. Comprueba que la tinta y el acento se leen bien sobre el fondo.
   - `marca`: el @ del usuario. `cierre.llamada`: la frase de la píldora, con la palabra para comentar entre « ». `cierre.sigue`: la última línea.
   - Si el usuario no da los textos, propón unos y enséñaselos antes de renderizar.
3. **Genera:** `python3 generar.py` crea `index.html`.
4. **Comprueba antes de renderizar:**
   - `npx hyperframes lint` tiene que dar 0 errores.
   - Saca fotogramas con `npx hyperframes snapshot --at 0.5,2,<N+2.5>,<N+5>,<final-1> --no-end` (N = número de frases) y míralos.
   - Los textos se tienen que leer enteros. Si una línea no cabe, acórtala y vuelve al paso 3.
5. **Renderiza:** `npx hyperframes render -o reel.mp4 --fps 30`.
6. **Entrega:** `reel.mp4`, diciendo qué textos y colores has usado.

## Cambios
- **Textos o colores:** edita `reel.json` y repite los pasos 3 a 5.
- **Ritmo o efectos:** se tocan en `generar.py`. Los tiempos están arriba (`TD0`, `T_ON`, `T_OUT`, `T_E`) y el barrido de la linterna en `PSI` y `OPEN`.
- **Tu logo en el cierre:** añádelo como `<img>` dentro de `#cierre`, encima del @.

## Licencias
- Hyperframes: Apache-2.0.
- Fuentes Inter, DM Serif Display y JetBrains Mono: SIL Open Font License.
- Sonidos de Kenney: CC0.

Detalle en `LICENCIAS.md`.
