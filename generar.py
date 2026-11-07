#!/usr/bin/env python3
"""Genera un reel animado de la bola (motion graphics, sin cámara) a partir de reel.json, para renderizarlo con Hyperframes.

Estructura del reel:
  1. Una bola colgada de un hilo se balancea; en cada pasada el hilo cambia el texto (un vaivén por frase).
  2. En la última pasada el hilo arrastra la oscuridad; la bola sube y hace de linterna: su haz barre y descubre la frase final.
  3. Vuelve la luz y cierra con tu @, la píldora para comentar y «sígueme».
Todo se dibuja con una sola función draw(t) desde un proxy de GSAP: cada fotograma depende solo del tiempo.

Uso:  python3 generar.py            (lee reel.json y escribe index.html en esta carpeta)
      npx hyperframes render -o reel.mp4 --fps 30
"""
import json
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(AQUI, "reel.json"), encoding="utf-8"))
SONIDOS = json.load(open(os.path.join(AQUI, "assets", "sfx", "sonidos.json"), encoding="utf-8"))

COL = {"fondo": "#EAE2CD", "tinta": "#141210", "acento": "#F2551E", "oscuro": "#14151A", "bola": "#FE6C2F"}
COL.update(CFG.get("colores", {}))
VAIVENES = CFG["vaivenes"]
N = len(VAIVENES)
assert 2 <= N <= 7, "Pon entre 2 y 7 vaivenes"
LIN = CFG["linterna"]
CIERRE = CFG.get("cierre", {})
MARCA = CFG.get("marca", "@tu_marca")


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mezcla(a, b, x):   # mezcla dos colores (#hex) en proporción x hacia b
    ra, rb = rgb(a), rgb(b)
    return "#%02X%02X%02X" % tuple(round(ra[i] + (rb[i] - ra[i]) * x) for i in range(3))


def rgba(h, a):
    r, g, b = rgb(h)
    return f"rgba({r},{g},{b},{a})"


def marcado(txt):   # *palabra* = color de acento
    out, dentro = "", False
    for parte in txt.split("*"):
        out += (f'<span class="ac">{parte}</span>' if dentro else parte)
        dentro = not dentro
    return out


def tam(lineas, base, ancho=900, k=0.72):   # tamaño que cabe: la línea más larga ocupa como mucho «ancho» px
    largo = max(len(l.replace("*", "")) for l in lineas)
    return min(base, int(ancho / (k * max(1, largo))))


BOLA = COL["bola"]
B_LUZ, B_CLARO, B_OSC, B_BORDE = mezcla(BOLA, "#FFFFFF", 0.88), mezcla(BOLA, "#FFFFFF", 0.42), mezcla(BOLA, "#000000", 0.08), mezcla(BOLA, "#000000", 0.18)
LAMP = [mezcla(COL["fondo"], "#FFFFFF", 0.12), COL["fondo"], mezcla(COL["fondo"], "#000000", 0.06), mezcla(COL["fondo"], "#000000", 0.12), mezcla(COL["fondo"], "#000000", 0.2)]

# ---------------------------------------------------------------- tiempos
TD0 = float(N)                      # empieza el vaivén de la oscuridad
SH = TD0 - 5.0                      # el barrido de la linterna está medido con la oscuridad empezando en el segundo 5
T_ON = TD0 + 1.85                   # se enciende la linterna
T_FIN_LUZ = TD0 + 4.45              # el haz se ha abierto del todo
T_OUT = T_FIN_LUZ + 1.15            # se va la frase de la linterna
T_E = T_OUT + 0.35                  # cierre
DUR = round(T_E + 3.3, 2)
PSI = [(6.85, 40), (7.1, 33), (7.15, 27), (7.2, 12.5), (7.25, -4), (7.3, -17), (7.35, -30), (7.4, -36), (7.467, -37), (7.5, -29),
       (7.533, 2), (7.567, 24), (7.6, 31), (7.667, 30), (7.7, 27), (7.75, 20), (7.8, 9), (7.833, 1), (7.867, -6.5), (7.9, -14),
       (7.95, -22), (8.0, -29), (8.05, -35), (8.1, -23), (8.133, -1), (8.167, 16), (8.2, 25), (8.267, 24), (8.3, 18), (8.333, 14.5),
       (8.367, 11), (8.4, 5.8), (8.433, 0.5), (8.467, -4.8), (8.5, -9.8), (8.533, -14.5), (8.6, -20), (8.65, -22.6), (8.7, -22),
       (8.733, -17.7), (8.767, -15.8), (8.8, -12.7), (8.833, -8.2), (8.867, -3.9), (8.9, -0.8), (8.933, 0)]
OPEN = [(9.067, 12.5), (9.1, 15.8), (9.133, 20), (9.167, 26.5), (9.2, 38.6), (9.25, 60), (9.3, 95), (9.35, 130), (9.4, 165), (9.45, 190)]
PSI = [(round(t + SH, 3), a) for t, a in PSI]
OPEN = [(round(t + SH, 3), a) for t, a in OPEN]

# ---------------------------------------------------------------- sonido: cada golpe cae en su movimiento
sfx = []


def at(t, nombre, vol):
    if 0.02 <= t <= DUR - 0.05:
        sfx.append((round(max(0.0, t - SONIDOS[nombre]["pico"]), 3), nombre, vol))


for k in range(N):
    at(k + 0.5, ["slide1", "slide3", "slide2", "slide4"][k % 4], 0.85)    # el hilo cruza el texto
at(TD0 + 0.5, "shove2", 1.0)                                              # arrastra la oscuridad
at(TD0 + 1.5, "soft1", 0.28)                                              # la bola se para arriba
at(T_ON + 0.005, "switch1", 0.75)
at(T_ON + 0.1, "switch2", 0.35)
for i, tc in enumerate([7.233, 7.533, 7.833, 8.133, 8.433]):
    at(tc + SH, ["slide1", "slide3", "slide2", "slide4", "slide1"][i], [0.55, 0.5, 0.42, 0.36, 0.3][i])   # el haz cruza el centro
at(9.33 + SH, "fan2", 0.7)
at(9.46 + SH, "glass1", 0.3)                                              # vuelve la luz
at(T_OUT + 0.02, "soft2", 0.25)
for i in range(3):
    at(T_E + 0.03 + i * 0.14, "click3", 0.2)                              # sube tu @
at(T_E + 0.85, "drop2", 0.55)                                             # cae la bola
at(T_E + 1.22, "chip3", 0.7)                                              # píldora
at(T_E + 1.55, "tick2", 0.5)                                              # flecha


def audios():
    out = []
    for k, (t, n, v) in enumerate(sorted(sfx)):
        d = min(SONIDOS[n]["duration"], DUR - t - 0.01, 2.0)
        out.append(f'<audio id="sfx-{k:02d}" src="assets/{SONIDOS[n]["file"]}" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{10 + k}" data-volume="{v}"></audio>')
    return "\n      ".join(out)


# ---------------------------------------------------------------- texto y estilo
TS = tam([l for v in VAIVENES for l in v], 132)
TL = tam(LIN["lineas"], 120, 900, 0.7)
TC = min(176, int(820 / (0.45 * max(1, len(LIN["cursiva"])))))
TM = min(130, int(940 / (0.62 * max(1, len(MARCA)))))
LLAMADA = CIERRE.get("llamada", "comenta «REEL» y te lo paso")
TP = min(50, int(900 / (0.56 * max(1, len(LLAMADA)))))   # la píldora cabe con margen aunque la frase sea larga
CSS = f"""
@font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter-Variable.ttf") format("truetype"); font-weight: 100 900; }}
@font-face {{ font-family: "Serif"; src: url("assets/fonts/DMSerifDisplay-Italic.ttf") format("truetype"); }}
@font-face {{ font-family: "Mono"; src: url("assets/fonts/JetBrainsMono.ttf") format("truetype"); font-weight: 100 800; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {COL["fondo"]}; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {COL["fondo"]}; font-family: "Inter"; color: {COL["tinta"]}; }}
.lay {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
#vig {{ background: radial-gradient(ellipse 80% 64% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.04) 76%, rgba(0,0,0,0.16) 100%); }}
#marca {{ position: absolute; left: 78px; top: 112px; font: 500 24px/1 "Mono"; color: {mezcla(COL["fondo"], COL["tinta"], 0.45)}; z-index: 30; }}
.sw {{ visibility: hidden; }}
.sw .blk {{ position: absolute; left: 0; width: 1080px; top: {960 - TS * 1.08 + 50:.0f}px; text-align: center; font: 900 {TS}px/1.08 "Inter"; letter-spacing: -0.03em; }}
.sw .blk div {{ white-space: nowrap; }}
.ac {{ color: {COL["acento"]}; }}
#lamp, #frase {{ visibility: hidden; }}
#lamp {{ background: radial-gradient(ellipse 92% 78% at 540px 520px, {LAMP[0]} 0%, {LAMP[1]} 28%, {LAMP[2]} 52%, {LAMP[3]} 74%, {LAMP[4]} 100%); }}
#frase .blk {{ position: absolute; left: 0; width: 1080px; top: 690px; text-align: center; }}
#frase .l1 {{ font: 900 {TL}px/1.06 "Inter"; letter-spacing: -0.03em; white-space: nowrap; }}
#frase .l3 {{ font: {TC}px/1.02 "Serif"; color: {COL["acento"]}; margin-top: 6px; white-space: nowrap; }}
#sombra {{ position: absolute; width: 66px; height: 66px; margin: -33px 0 0 -33px; border-radius: 50%; background: radial-gradient(circle, rgba(0,0,0,0.26) 0%, rgba(0,0,0,0.11) 45%, rgba(0,0,0,0) 72%); filter: blur(7px); }}
#hilo, #hilosombra {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
#oscuro {{ visibility: hidden; background: radial-gradient(ellipse 110% 85% at 50% 40%, {COL["oscuro"]} 0%, {COL["oscuro"]} 55%, {mezcla(COL["oscuro"], "#000000", 0.18)} 100%); }}
#caida {{ visibility: hidden; background: radial-gradient(circle at 540px 520px, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 330px, {rgba(COL["oscuro"], 0.2)} 1300px, {rgba(COL["oscuro"], 0.26)} 1700px); }}
#polvo {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; visibility: hidden; mix-blend-mode: screen; }}
#halo {{ position: absolute; width: 300px; height: 300px; margin: -150px 0 0 -150px; border-radius: 50%; background: radial-gradient(circle, {rgba(BOLA, 0.30)} 0%, {rgba(BOLA, 0.14)} 22%, {rgba(BOLA, 0.05)} 40%, {rgba(BOLA, 0)} 58%); opacity: 0; }}
#halod {{ position: absolute; width: 270px; height: 270px; margin: -135px 0 0 -135px; border-radius: 50%; background: radial-gradient(circle, {rgba(BOLA, 0.7)} 0%, {rgba(BOLA, 0.42)} 22%, {rgba(BOLA, 0.16)} 38%, {rgba(BOLA, 0.05)} 58%, {rgba(BOLA, 0)} 75%); opacity: 0; }}
#estela {{ position: absolute; height: 30px; border-radius: 15px; transform-origin: 100% 50%; background: linear-gradient(to right, {rgba(BOLA, 0)} 0%, {rgba(BOLA, 0.45)} 100%); filter: blur(4px); opacity: 0; }}
#bola {{ position: absolute; width: 66px; height: 66px; margin: -33px 0 0 -33px; border-radius: 50%;
  background: radial-gradient(circle at 34% 30%, {B_LUZ} 0%, {B_CLARO} 14%, {BOLA} 40%, {B_OSC} 70%, {B_BORDE} 100%);
  box-shadow: inset -6px -8px 13px rgba(0,0,0,0.22), 0 3px 7px rgba(0,0,0,0.16); }}
#bola::after {{ content: ""; position: absolute; left: 16px; top: 13px; width: 14px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.82); filter: blur(1.5px); transform: rotate(-30deg); }}
#nucleo {{ position: absolute; inset: -10px; border-radius: 50%; background: radial-gradient(circle, rgba(255,240,226,0.85) 0%, rgba(255,210,180,0.4) 35%, rgba(255,200,170,0) 70%); opacity: 0; mix-blend-mode: screen; }}
#cierre {{ visibility: hidden; }}
#wm {{ position: absolute; left: 0; width: 1080px; top: 860px; text-align: center; white-space: nowrap; }}
#wm span {{ display: inline-block; font: 900 {TM}px/1.1 "Inter"; letter-spacing: -0.04em; }}
#wmclip {{ display: inline-block; overflow: hidden; padding: 0 6px 14px; }}
#pill {{ position: absolute; left: 50%; top: {860 + TM * 1.1 + 70:.0f}px; height: 130px; padding: 0 50px; border-radius: 65px; background: {COL["tinta"]}; color: {COL["fondo"]}; white-space: nowrap; display: flex; align-items: center; gap: {round(TP * 0.33)}px; transform: translateX(-50%); font: 700 {TP}px/1 "Inter"; }}
#pill .ac {{ font: {round(TP * 1.55)}px/1 "Serif"; margin-top: -6px; }}
#flecha {{ position: absolute; left: 505px; top: {860 + TM * 1.1 + 245:.0f}px; width: 70px; height: 88px; }}
#sigue {{ position: absolute; left: 0; width: 1080px; top: {860 + TM * 1.1 + 375:.0f}px; text-align: center; font: 500 30px/1 "Mono"; color: {mezcla(COL["fondo"], COL["tinta"], 0.55)}; }}
"""


def pill_html(txt):   # «PALABRA» va en la serif cursiva de acento
    if "«" in txt and "»" in txt:
        a, r = txt.split("«", 1)
        b, c = r.split("»", 1)
        return f'<span>{a.strip()}</span><span class="ac">«{b}»</span><span>{c.strip()}</span>'
    return f"<span>{txt}</span>"


JS = r"""
const W = 1080, H = 1920, DUR = __DUR__, N = __N__, TD0 = __TD0__, T_ON = __TON__, T_OUT = __TOUT__, T_E = __TE__;
const PSI = __PSI__, OPEN = __OPEN__;
const P = {x: 540, y: -850}, L = 1930, PHI = 16.6 * Math.PI / 180;
const $ = id => document.getElementById(id);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const u = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const eo = x => 1 - Math.pow(1 - x, 3), ei2 = x => x * x, eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const ss = (a, b, t) => { const x = u(t, a, b); return x * x * (3 - 2 * x); };
const lerp = (a, b, x) => a + (b - a) * x;
const vis = (el, on) => { el.style.visibility = on ? "visible" : "hidden"; };
function hash(i, j) { const h = Math.sin(i * 127.1 + j * 311.7) * 43758.5453; return h - Math.floor(h); }
function table(T, t) { if (t <= T[0][0]) return T[0][1]; for (let i = 1; i < T.length; i++) if (t <= T[i][0]) { const a = T[i - 1], b = T[i]; return lerp(a[1], b[1], (t - a[0]) / (b[0] - a[0])); } return T[T.length - 1][1]; }

// péndulo: un vaivén por segundo (lento en los extremos, rápido en el centro)
function pend(t) { const th = Math.PI * Math.min(t, TD0 + 1), phi = -PHI * Math.cos(th); return {x: P.x + L * Math.sin(phi), y: P.y + L * Math.cos(phi), k: Math.min(N, Math.floor(th / Math.PI + 1e-9))}; }
function lineX(B, y) { return P.x + (B.x - P.x) * (y - P.y) / (B.y - P.y); }
function poly(B, side, extra) {
  const xa = lineX(B, -200) - (extra || 0), xb = lineX(B, 2120);
  return side === "L" ? `polygon(-80px -200px, ${xa}px -200px, ${xb}px 2120px, -80px 2120px)` : `polygon(${xa}px -200px, 1160px -200px, 1160px 2120px, ${xb}px 2120px)`;
}
function bezier(a, c, b, s) { const m = 1 - s; return {x: m * m * a.x + 2 * m * s * c.x + s * s * b.x, y: m * m * a.y + 2 * m * s * c.y + s * s * b.y}; }
function ball(t) {
  if (t < TD0 + 0.95) { const b = pend(t); return {x: b.x, y: b.y, s: 1, o: 1}; }
  if (t < TD0 + 1.5) { const a = pend(TD0 + 0.95), b = bezier(a, {x: a.x + (a.x > 540 ? 30 : -30), y: a.y - 430}, {x: 540, y: 520}, eio(u(t, TD0 + 0.95, TD0 + 1.5))); return {x: b.x, y: b.y, s: 1, o: 1}; }
  if (t < T_OUT + 0.3) return {x: 540, y: 520 + 3.5 * Math.sin(2 * Math.PI * (t - TD0 - 1.5) / 2.4) * ss(TD0 + 1.5, TD0 + 1.9, t) * (1 - ss(T_OUT, T_OUT + 0.3, t)), s: 1, o: 1 - u(t, T_OUT, T_OUT + 0.3)};
  if (t < T_E + 0.5) return {x: 540, y: -80, s: 1, o: 0};
  if (t < T_E + 0.85) { const s = ei2(u(t, T_E + 0.5, T_E + 0.85)); return {x: 540, y: lerp(-80, 790, s), s: 1, o: 1}; }   // cae con gravedad
  return {x: 540, y: 790, s: 1, o: 1};
}
function torch(t) {
  let I = 0;
  if (t >= T_ON) {
    if (t < T_ON + 0.03) I = 0.75 * u(t, T_ON, T_ON + 0.03);
    else if (t < T_ON + 0.07) I = lerp(0.75, 0.12, u(t, T_ON + 0.03, T_ON + 0.07));
    else if (t < T_ON + 0.1) I = lerp(0.12, 0.9, u(t, T_ON + 0.07, T_ON + 0.1));
    else I = lerp(0.9, 1, u(t, T_ON + 0.1, T_ON + 0.2));
  }
  return {I, psi: table(PSI, t), w: table(OPEN, t)};
}
function coneDark(cx, cy, c, w, I) { const s = 1.4, a0 = c - w - s, i = 1 - I; return `conic-gradient(from ${a0}deg at ${cx}px ${cy}px, rgba(0,0,0,1) 0deg, rgba(0,0,0,${i}) ${s}deg, rgba(0,0,0,${i}) ${s + 2 * w}deg, rgba(0,0,0,1) ${2 * s + 2 * w}deg, rgba(0,0,0,1) 360deg)`; }
function coneIn(cx, cy, c, w) { const s = 1.4, a0 = c - w - s; return `conic-gradient(from ${a0}deg at ${cx}px ${cy}px, rgba(0,0,0,0) 0deg, rgba(0,0,0,1) ${s}deg, rgba(0,0,0,1) ${s + 2 * w}deg, rgba(0,0,0,0) ${2 * s + 2 * w}deg, rgba(0,0,0,0) 360deg)`; }
function setMask(el, m) { el.style.webkitMaskImage = m; el.style.maskImage = m; }
const polvo = $("polvo"), pctx = polvo.getContext("2d"); polvo.width = W; polvo.height = H;
function drawPolvo(t, cx, cy, a0) {
  pctx.clearRect(0, 0, W, H); if (a0 <= 0) return;
  const tt = t - T_ON, span = H - cy - 30;
  for (let i = 0; i < 120; i++) {
    const z = hash(i, 3);
    let x = hash(i, 1) * W + 26 * Math.sin(tt * (0.35 + 0.5 * z) + 6.283 * hash(i, 4));
    let y = cy + 30 + hash(i, 2) * span - tt * (9 + 22 * z); y = cy + 30 + (((y - cy - 30) % span) + span) % span;
    pctx.fillStyle = `rgba(255,250,240,${a0 * 0.3 * (0.35 + 0.65 * z)})`; pctx.beginPath(); pctx.arc(x, y, 1 + 2.4 * z * z, 0, 6.2832); pctx.fill();
  }
}
const TX = Array.from({length: N}, (_, i) => $("sw" + i));
const hilo = $("h"), hiloS = $("hs"), bola = $("bola"), nucleo = $("nucleo"), halo = $("halo"), halod = $("halod"), estela = $("estela"), sombra = $("sombra");
const oscuro = $("oscuro"), caida = $("caida"), lamp = $("lamp"), frase = $("frase"), cierre = $("cierre");
function draw(t) {
  // cada vaivén descubre la frase nueva del lado por donde ya ha pasado el hilo
  const B = pend(Math.min(t, TD0 + 1)), k = t < TD0 + 1 ? B.k : 99;
  for (let j = 0; j < N; j++) {
    const el = TX[j];
    if (k === j) { vis(el, true); el.style.clipPath = poly(B, j % 2 === 0 ? "L" : "R"); }
    else if (k === j + 1 && j < N - 1) { vis(el, true); el.style.clipPath = poly(B, (j + 1) % 2 === 0 ? "R" : "L"); }
    else if (k === N && j === N - 1) { vis(el, true); el.style.clipPath = "none"; }
    else vis(el, false);
  }
  vis(lamp, t >= TD0 + 0.9 && t < T_E + 0.1); lamp.style.opacity = 1 - u(t, T_OUT + 0.1, T_E + 0.1);
  vis(frase, t >= TD0 + 0.9 && t < T_OUT + 0.35);
  if (t >= T_OUT) { const x = u(t, T_OUT, T_OUT + 0.32); frase.style.filter = `blur(${20 * x}px)`; frase.style.opacity = 1 - x; } else { frase.style.filter = "none"; frase.style.opacity = 1; }
  // oscuridad y linterna
  const bs = ball(t), tr = torch(t), lado = N % 2 === 0 ? "L" : "R";
  if (t >= TD0 && t < TD0 + 4.46) {
    vis(oscuro, true);
    if (t < TD0 + 1) { oscuro.style.clipPath = poly(B, lado, (lado === "L" ? -1 : 1) * 950 * ss(TD0 + 0.6, TD0 + 1, t)); setMask(oscuro, "none"); }
    else { oscuro.style.clipPath = "none"; setMask(oscuro, tr.I > 0 ? coneDark(bs.x, bs.y, 180 + tr.psi, tr.w, tr.I) : "none"); }
  } else vis(oscuro, false);
  const on = t >= T_ON && t < TD0 + 4.52 && tr.I > 0;
  vis(caida, on); vis(polvo, on);
  if (on) { const mi = coneIn(bs.x, bs.y, 180 + tr.psi, Math.min(tr.w, 179)), f = 1 - ss(TD0 + 4.2, TD0 + 4.5, t); setMask(caida, mi); caida.style.opacity = tr.I * f; setMask(polvo, mi); polvo.style.opacity = f; drawPolvo(t, bs.x, bs.y, tr.I); }
  else drawPolvo(t, 0, 0, 0);
  // hilo, bola, halo, estela y sombra
  hilo.setAttribute("x2", bs.x); hilo.setAttribute("y2", bs.y); hilo.style.opacity = t < TD0 + 0.95 ? 1 : 1 - u(t, TD0 + 0.95, TD0 + 1.12);
  hiloS.setAttribute("x2", bs.x + 34); hiloS.setAttribute("y2", bs.y + 50); hiloS.style.opacity = t < TD0 ? 1 : 0;
  bola.style.left = bs.x + "px"; bola.style.top = bs.y + "px"; bola.style.opacity = bs.o;
  const luz = (t >= TD0 + 1 && t < TD0 + 4.45) ? 1 : (t >= TD0 + 0.95 && t < TD0 + 1 ? u(t, TD0 + 0.95, TD0 + 1) : (t >= TD0 + 4.45 && t < TD0 + 4.7 ? 1 - u(t, TD0 + 4.45, TD0 + 4.7) : 0));
  nucleo.style.opacity = luz * (t >= T_ON ? lerp(0.55, 0.9, tr.I) : 0.55);
  halod.style.left = bs.x + "px"; halod.style.top = bs.y + "px"; halod.style.opacity = luz * bs.o;
  halo.style.left = bs.x + "px"; halo.style.top = bs.y + "px"; halo.style.opacity = (1 - luz) * bs.o;
  const p0 = ball(Math.max(0, t - 1 / 30)), vx = (bs.x - p0.x) * 30, vy = (bs.y - p0.y) * 30, sp = Math.hypot(vx, vy), lt = clamp(sp * 0.05, 0, 150);
  estela.style.width = lt + "px"; estela.style.left = (bs.x - lt) + "px"; estela.style.top = (bs.y - 15) + "px";
  estela.style.transform = `rotate(${Math.atan2(vy, vx) * 180 / Math.PI}deg)`; estela.style.opacity = bs.o * clamp((sp - 250) / 1400, 0, 0.8);
  sombra.style.left = (bs.x + 34) + "px"; sombra.style.top = (bs.y + 50) + "px"; sombra.style.opacity = (t < TD0 || t >= T_E + 0.85) ? bs.o : 0;
  // cierre
  vis(cierre, t >= T_E);
  if (t >= T_E) {
    $("wm").querySelectorAll(".ch").forEach((s, i) => { const x = eo(u(t, T_E + i * 0.034, T_E + i * 0.034 + 0.34)); s.style.transform = `translateY(${(1 - x) * 110}%)`; });
    const pl = $("pill"), px = eo(u(t, T_E + 1.2, T_E + 1.48)); pl.style.opacity = u(t, T_E + 1.2, T_E + 1.25); pl.style.clipPath = `inset(0 ${(1 - px) * 50}% 0 ${(1 - px) * 50}% round 65px)`;
    $("flecha").style.opacity = u(t, T_E + 1.5, T_E + 1.64); $("flecha").style.transform = `translateY(${(1 - eo(u(t, T_E + 1.5, T_E + 1.82))) * -18}px)`;
    $("sigue").style.opacity = u(t, T_E + 1.7, T_E + 1.92);
  }
}
const tl = gsap.timeline({paused: true});
const proxy = {t: 0};
tl.to(proxy, {t: DUR, duration: DUR, ease: "none", onUpdate: () => draw(proxy.t)}, 0);
draw(0);
window.__timelines["main"] = tl;
"""


def main():
    capas = "\n      ".join(f'<div id="sw{i}" class="lay sw"><div class="blk"><div>{marcado(a)}</div><div>{marcado(b)}</div></div></div>' for i, (a, b) in enumerate(VAIVENES))
    lineas = "".join(f'<div class="l1">{marcado(x)}</div>' for x in LIN["lineas"])
    wm = "".join(f'<span class="ch">{c}</span>' for c in MARCA)
    js = (JS.replace("__DUR__", str(DUR)).replace("__N__", str(N)).replace("__TD0__", str(TD0)).replace("__TON__", str(T_ON))
          .replace("__TOUT__", str(T_OUT)).replace("__TE__", str(T_E)).replace("__PSI__", json.dumps(PSI)).replace("__OPEN__", json.dumps(OPEN)))
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="vig" class="lay"></div>
      {capas}
      <div id="lamp" class="lay"></div>
      <div id="frase" class="lay"><div class="blk">{lineas}<div class="l3">{marcado(LIN["cursiva"])}</div></div></div>
      <svg id="hilosombra" class="lay" viewBox="0 0 1080 1920"><defs><filter id="sb" x="-50%" y="-5%" width="200%" height="110%"><feGaussianBlur stdDeviation="3.2" /></filter></defs><line id="hs" x1="574" y1="-800" x2="0" y2="0" stroke="rgba(0,0,0,0.14)" stroke-width="4" filter="url(#sb)" /></svg>
      <div id="sombra"></div>
      <div id="cierre" class="lay">
        <div id="wm"><span id="wmclip">{wm}</span></div>
        <div id="pill">{pill_html(LLAMADA)}</div>
        <svg id="flecha" viewBox="0 0 70 88"><path d="M35 4 V80 M10 56 L35 81 L60 56" fill="none" stroke="{COL["tinta"]}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
        <div id="sigue">{CIERRE.get("sigue", "sígueme para más")}</div>
      </div>
      <div id="oscuro" class="lay"></div>
      <div id="caida" class="lay"></div>
      <canvas id="polvo"></canvas>
      <svg id="hilo" class="lay" viewBox="0 0 1080 1920"><line id="h" x1="540" y1="-850" x2="0" y2="0" stroke="{mezcla(COL["tinta"], COL["fondo"], 0.1)}" stroke-width="2.6" stroke-linecap="round" /></svg>
      <div id="halo"></div>
      <div id="halod"></div>
      <div id="estela"></div>
      <div id="bola"><div id="nucleo"></div></div>
      <div id="marca">{MARCA}</div>
      {audios()}
    </div>
    <script>
{js}
    </script>
  </body>
</html>
"""
    open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8").write(html)
    print(f"index.html listo: {N} vaivenes, {DUR} s, {len(sfx)} sonidos")


if __name__ == "__main__":
    main()
