from pathlib import Path
import re, shutil

root = Path(__file__).resolve().parent
page = root / 'reparacion-notebooks' / 'index.html'
if not page.is_file():
    raise SystemExit('ERROR: falta reparacion-notebooks/index.html. Ejecutá desde la carpeta Megabyte web.')
html = page.read_text(encoding='utf-8-sig')
if 'id="mb-notebooks-fallas-frecuentes"' in html:
    raise SystemExit('La nueva sección ya está instalada. No se modificó nada.')
pattern = re.compile(r'<section>\s*<div class="wrap">\s*<div class="eyebrow">Cómo trabajamos</div>\s*<h2>Tu notebook, en buenas manos</h2>.*?</section>', re.S)
if len(pattern.findall(html)) != 1:
    raise SystemExit('ERROR: no se encontró exactamente una sección original. No se modificó nada.')
new = '''<section id="mb-notebooks-fallas-frecuentes"><div class="wrap">
<div class="eyebrow">Reparaciones de notebooks y laptops</div>
<h2>Soluciones para las fallas más comunes</h2>
<p class="intro">Desde problemas de encendido hasta reparaciones electrónicas de placas madre. Evaluamos cada equipo para determinar la solución adecuada.</p>
<div class="grid">
<article class="card"><h3>Notebook que no enciende</h3><p>Diagnóstico de circuitos de alimentación, placa madre y fallas de encendido.</p></article>
<article class="card"><h3>Problemas de carga</h3><p>Revisión de conectores, alimentación, batería y circuitos de carga.</p></article>
<article class="card"><h3>Pantallas y bisagras</h3><p>Solución de problemas de imagen, pantallas dañadas y bisagras deterioradas.</p></article>
<article class="card"><h3>Lentitud y almacenamiento</h3><p>Diagnóstico de rendimiento, instalación de SSD y ampliación de memoria cuando corresponde.</p></article>
<article class="card"><h3>Sobrecalentamiento</h3><p>Limpieza, mantenimiento y revisión del sistema de refrigeración.</p></article>
<article class="card"><h3>Reparación de placa madre</h3><p>Diagnóstico electrónico y reparación a nivel de componentes, cuando es técnicamente viable.</p></article>
</div></div></section>'''
updated = pattern.sub(lambda m:new, html, count=1)
# Reuse existing card/grid style. Only add a local accent bar to distinguish the new section.
style = '''<style id="mb-notebooks-fallas-estilo">
#mb-notebooks-fallas-frecuentes .card::before{content:"";display:block;width:32px;height:3px;background:var(--accent,#00e676);margin-bottom:20px}
#mb-notebooks-fallas-frecuentes .card h3{margin-top:0}
</style>\n'''
if '</head>' not in updated:
    raise SystemExit('ERROR: falta </head>. No se modificó nada.')
updated = updated.replace('</head>', style+'</head>',1)
backup = page.with_name('index.html.respaldo_antes_cambiar_seccion')
if not backup.exists():
    shutil.copy2(page, backup)
page.write_text(updated,encoding='utf-8')
print('OK: se reemplazó únicamente la sección «Tu notebook, en buenas manos».')
print('OK: el logo y el resto de la página se conservaron.')
print('Respaldo:',backup)
print('Revisá reparacion-notebooks/index.html antes de subirlo a GitHub.')
