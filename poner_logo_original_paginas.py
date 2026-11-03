from pathlib import Path
import re, shutil

root = Path(__file__).resolve().parent
home = root / 'index.html'
if not home.is_file():
    raise SystemExit('ERROR: colocá este script junto al index.html principal de MegaByte.')
html = home.read_text(encoding='utf-8-sig')
match = re.search(r'<div\s+class=["\']header-logo["\'][^>]*>\s*<img\b[^>]*\bsrc=["\']([^"\']+)["\']', html, re.I | re.S)
if not match:
    raise SystemExit('ERROR: no se encontró el logo original en la cabecera de la portada. No se cambió nada.')
logo_src = match.group(1)
if not (logo_src.startswith('data:image/') or logo_src.startswith('/') or logo_src.startswith('https://')):
    raise SystemExit('ERROR: formato de logo inesperado; no se cambió nada.')

pages = [root / 'reparacion-celulares' / 'index.html', root / 'reparacion-notebooks' / 'index.html']
for page in pages:
    if not page.is_file():
        raise SystemExit(f'ERROR: falta {page}. No se cambió nada.')

style = '''<style id="megabyte-logo-paginas">
/* Logo oficial de la portada: se conserva su imagen sin alterar proporciones */
header a.brand:has(img.megabyte-logo-original) { display:inline-flex;align-items:center;max-width:55%;text-decoration:none; }
header img.megabyte-logo-original { display:block;width:auto;height:82px;max-width:100%;object-fit:contain; }
@media(max-width:600px){header img.megabyte-logo-original{height:58px}header a.brand:has(img.megabyte-logo-original){max-width:55%}}
</style>'''

for page in pages:
    source = page.read_text(encoding='utf-8-sig')
    if 'class="megabyte-logo-original"' in source:
        print(f'YA ESTÁ: {page.relative_to(root)}')
        continue
    pattern = r'(<a\b(?=[^>]*\bclass=["\'][^"\']*\bbrand\b[^"\']*["\'])[^>]*>)(.*?)(</a>)'
    img = f'<img class="megabyte-logo-original" src="{logo_src}" alt="MegaByte - Soluciones en Informática">'
    updated, count = re.subn(pattern, lambda m: m.group(1) + img + m.group(3), source, count=1, flags=re.I | re.S)
    if count != 1 or '</head>' not in updated:
        raise SystemExit(f'ERROR: estructura inesperada en {page}. No se cambió ese archivo.')
    updated = updated.replace('</head>', style + '\n</head>', 1)
    backup = page.with_name('index.html.respaldo_antes_logo')
    if not backup.exists():
        shutil.copy2(page, backup)
    page.write_text(updated, encoding='utf-8')
    print(f'OK: logo oficial agregado a {page.relative_to(root)}; respaldo creado.')
print('TERMINADO. Abrí las dos páginas localmente antes de subir a GitHub.')
