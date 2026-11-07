#!/usr/bin/env python3
"""Genera el reel GOTOKU: teléfono 2.5D, capturas reales y plataforma de roca."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "reel_gotoku.json").read_text(encoding="utf-8"))
OUT = ROOT / "index_gotoku.html"

shots = ["platos.png", "delivery.png", "resumen.png"]
for name in shots + ["plataforma_roca.png"]:
    if not (ROOT / "assets" / "gotoku" / name).exists():
        raise FileNotFoundError(f"Falta assets/gotoku/{name}")

vaivenes = CFG["vaivenes"]
if len(vaivenes) != 3:
    raise ValueError("El reel GOTOKU requiere exactamente 3 bloques de texto.")

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def marked(s):
    parts = s.split("*")
    return "".join(('<em>' if i % 2 else '') + esc(p) + ('</em>' if i % 2 else '') for i, p in enumerate(parts))

colors = CFG["colores"]
texts = []
for i, pair in enumerate(vaivenes):
    texts.append(f'<div class="claim" id="claim{i}"><span>{marked(pair[0])}</span><span>{marked(pair[1])}</span></div>')
screens = "".join(f'<img class="screen" id="screen{i}" src="assets/gotoku/{name}" alt="Captura real GOTOKU">' for i, name in enumerate(shots))
lineas = "".join(f'<div>{marked(x)}</div>' for x in CFG["linterna"]["lineas"])
sfx = [
    ("slide1", 1.05, .65), ("slide3", 4.0, .55), ("slide2", 7.0, .55),
    ("switch1", 9.5, .7), ("fan2", 11.1, .45), ("glass1", 12.2, .25),
    ("drop2", 14.2, .45), ("chip3", 14.65, .55), ("tick2", 15.1, .35)
]
audio = "".join(f'<audio src="assets/sfx/{name}.mp3" data-start="{start}" data-duration="1.8" data-track-index="{20+i}" data-volume="{vol}"></audio>' for i,(name,start,vol) in enumerate(sfx))
html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:Inter;src:url('assets/fonts/Inter-Variable.ttf')}}@font-face{{font-family:Serif;src:url('assets/fonts/DMSerifDisplay-Italic.ttf')}}
*{{box-sizing:border-box;margin:0;padding:0}}html,body,#root{{width:1080px;height:1920px;overflow:hidden;background:{colors['fondo']};font-family:Inter,sans-serif}}
#root{{position:relative;color:#fff;background:radial-gradient(ellipse at 50% 44%,#21172d 0%,{colors['fondo']} 76%)}}
#ambient{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,rgba(181,155,201,.15),transparent 55%)}}
#brand{{position:absolute;top:105px;width:100%;text-align:center;font-size:30px;font-weight:650;letter-spacing:.08em;color:#E4D2AE}}
#stage{{position:absolute;inset:0;perspective:1600px}}
#rock{{position:absolute;z-index:1;left:0;bottom:-10px;width:1080px;height:660px;object-fit:cover;object-position:center;filter:brightness(.72) contrast(1.12)}}
#phone{{position:absolute;z-index:2;left:50%;top:850px;width:570px;height:1120px;transform:translate(-50%,-50%) rotate(-7deg) rotateY(-9deg);transform-style:preserve-3d;border:13px solid #39323f;border-radius:76px;background:linear-gradient(135deg,#81778a,#17121e 26%,#08070b 72%,#665d70);padding:12px;box-shadow:36px 50px 70px rgba(0,0,0,.62),-10px -8px 30px rgba(181,155,201,.2),inset 0 0 0 3px #a69aac;overflow:hidden}}
#glass{{position:absolute;inset:12px;border-radius:53px;overflow:hidden;background:#0D0A12;border:2px solid #08070b}}
.screen{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;filter:saturate(.96)}}
#glare{{position:absolute;inset:0;pointer-events:none;background:linear-gradient(118deg,transparent 22%,rgba(255,255,255,.12) 37%,transparent 49%);mix-blend-mode:screen}}
#phone:after{{content:"";position:absolute;top:16px;left:50%;width:115px;height:25px;transform:translateX(-50%);border-radius:20px;background:#08070b;z-index:5}}
.claim{{position:absolute;z-index:4;top:335px;width:100%;text-align:center;font-size:108px;line-height:1.03;font-weight:900;letter-spacing:-.055em;color:#fff;opacity:0;text-shadow:0 5px 28px rgba(0,0,0,.45)}.claim span{{display:block}}.claim em{{font-style:normal;color:{colors['acento']}}}
#flash{{position:absolute;z-index:5;inset:0;opacity:0;background:radial-gradient(ellipse at 50% 48%,rgba(154,247,57,.19),transparent 52%);pointer-events:none}}
#final{{position:absolute;z-index:6;top:390px;width:100%;text-align:center;font-weight:900;font-size:92px;line-height:1.12;letter-spacing:-.045em;opacity:0;color:#fff;text-shadow:0 5px 25px #000}}#final em{{font-family:Serif;color:{colors['acento']};font-weight:400}}
#end{{position:absolute;z-index:7;top:1410px;width:100%;text-align:center;opacity:0}}#end strong{{display:block;font-size:42px;color:#fff;letter-spacing:.02em}}#end small{{display:block;margin-top:20px;font-size:30px;color:#E4D2AE}}
#metric{{position:absolute;z-index:4;right:74px;top:1040px;padding:18px 24px;border:1px solid {colors['verde']};border-radius:18px;color:{colors['verde']};font:700 25px Inter;background:rgba(13,10,18,.82);opacity:0;box-shadow:0 0 28px rgba(154,247,57,.18)} 
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="17" data-width="1080" data-height="1920">
<div id="ambient"></div><div id="brand">@gotoku.app</div><div id="stage">
{''.join(texts)}
<div id="phone"><div id="glass">{screens}<div id="glare"></div></div></div>
<img id="rock" src="assets/gotoku/plataforma_roca.png" alt="">
<div id="metric">COSTO · MARGEN · GANANCIA</div><div id="flash"></div>
<div id="final">{lineas}<div style="font:italic 76px Serif;color:{colors['acento']};margin-top:18px">{marked(CFG['linterna']['cursiva'])}</div></div>
<div id="end"><strong>{esc(CFG['cierre']['llamada'])}</strong><small>{esc(CFG['cierre']['sigue'])}</small></div>
</div>{audio}
<script>
const D=17, $=id=>document.getElementById(id);
const screens=[0,1,2].map(i=>$('screen'+i)), claims=[0,1,2].map(i=>$('claim'+i));
function fade(el,v){{el.style.opacity=v}}
function draw(t){{
  screens.forEach((el,i)=>fade(el,Math.max(0,1-Math.abs(t-(2.1+i*3.0))/1.0)));
  claims.forEach((el,i)=>{{const a=1.0+i*3.0;fade(el,Math.max(0,Math.min((t-a)/.22,(a+1.75-t)/.28,1)));}});
  const phone=$('phone'); phone.style.transform='translate(-50%,-50%) rotate('+(-7+Math.sin(t*.55)*1.1)+'deg) rotateY('+(-9+Math.sin(t*.4)*1.8)+'deg) translateY('+(-10*Math.sin(t*.8))+'px)';
  fade($('metric'),Math.max(0,Math.min((t-5.4)/.35,(7.9-t)/.35,1)));
  fade($('flash'),Math.max(0,Math.min((t-9.2)/.25,(10.1-t)/.6,1)));
  fade($('final'),Math.max(0,Math.min((t-10.1)/.45,(13.3-t)/.5,1)));
  fade($('end'),Math.max(0,Math.min((t-13.5)/.4,(16.9-t)/.3,1)));
}}
const proxy={{t:0}},tl=gsap.timeline({{paused:true}});
tl.to(proxy,{{t:D,duration:D,ease:'none',onUpdate:()=>draw(proxy.t)}},0);
draw(0);window.__timelines['main']=tl;
</script></div></body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"OK: {OUT.name} generado; duración {17}s; 3 capturas reales.")
