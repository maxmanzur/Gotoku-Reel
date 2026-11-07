# GOTOKU Reel

Proyecto independiente para adaptar la plantilla de Reel animado a la identidad de GOTOKU.

## Objetivo

Recrear el ritmo, la tipografía, las entradas/salidas y la sincronización de la referencia original, reemplazando su concepto visual por un teléfono 3D/2.5D con capturas reales de GOTOKU sobre una plataforma de roca oscura.

## Dirección visual confirmada

- Fondo: `#0D0A12`.
- Paleta GOTOKU: `#0D0A12`, `#1A1322`, `#FC0360`, `#9AF739`, `#FF7A5C`, `#E4D2AE`, `#4A4B4F`, `#B59BC9`.
- Teléfono suspendido visualmente e inclinado; no usar hilo ni movimiento de péndulo.
- Usar exclusivamente capturas reales de la aplicación dentro del teléfono.
- Mockup PNG multicapa con CSS para reflejos, sombras y profundidad.
- No usar GLB, Three.js ni rotación 360°.

## Material fuente pendiente de incorporar

- `generar.py`: generador original que se adaptará.
- `SKILL.md`: instrucciones de la plantilla original.
- `reel.json`: textos, colores y configuración adaptados a GOTOKU.
- `assets/`: capturas reales, mockup y sonidos autorizados.

No reemplazar ni modificar los archivos fuente originales hasta tener una copia completa y revisar sus dependencias.

## Seguridad del proyecto

Este repositorio es independiente de `maxmanzur/Gotoku`, la aplicación principal. No contiene ni modifica el código de la app GOTOKU.


## Generador GOTOKU (adaptación independiente)

La plantilla original de la bola se conserva sin cambios. Para generar la versión GOTOKU con teléfono 2.5D y capturas reales:

1. Ejecutar desde la raíz: `python generar_gotoku.py`.
2. Se crea `index_gotoku.html`.
3. Revisar el HTML y validar con Hyperframes antes de renderizar.
4. Los textos y la paleta oficial se editan en `reel_gotoku.json`.

El generador usa las capturas de `assets/gotoku/`, la plataforma `plataforma_roca.png`, las fuentes y los sonidos existentes. La generación y el render final todavía deben ejecutarse y revisarse visualmente; este commit no equivale a una prueba de render.
