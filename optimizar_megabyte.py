from pathlib import Path
import re

original = Path('index.html')
if not original.exists():
    raise SystemExit('Colocá este script junto al index.html original y ejecutalo desde esa carpeta.')
html = original.read_text(encoding='utf-8')

# SEO: limpiar sitemap duplicado sin alterar estilos ni estructura.
sitemap = '<link rel="sitemap" type="application/xml" href="/sitemap.xml">'
html = re.sub(r'(?m)^\s*<link rel="sitemap" type="application/xml" href="/sitemap\.xml">\s*\n', '', html)
html = html.replace('<meta name="viewport"', '  '+sitemap+'\n<meta name="viewport"', 1)

# JSON-LD: quitar URL de imagen de un dominio antiguo; se puede reponer al confirmar URL pública actual.
html = re.sub(r'(?m)^\s*"image": "https://megabytetacuarembo\.com/logo\.png",\s*\n', '', html)

# La etiqueta meta keywords no es utilizada por Google; eliminarla sin afectar el contenido visible.
html = re.sub(r'(?m)^\s*<meta name="keywords"[^>]*>\s*\n', '', html)

# Añadir color de navegador y mejor carga de tipografía (sin cambiar apariencia).
needle = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
if needle in html and 'name="theme-color"' not in html:
    html = html.replace(needle, needle+'\n  <meta name="theme-color" content="#0d0d0d">', 1)

# OG image se agrega solo cuando exista una imagen pública verificable; no apuntar a un recurso inexistente.
output = Path('index_SEO_optimizado.html')
output.write_text(html, encoding='utf-8')
print(f'Generado: {output} ({output.stat().st_size:,} bytes)')
