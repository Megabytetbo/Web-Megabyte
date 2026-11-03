from pathlib import Path
import re, shutil, xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
index = root / 'index.html'
if not index.is_file():
    raise SystemExit('ERROR: colocá este script junto al index.html de tu web.')
html = index.read_text(encoding='utf-8-sig')
if 'id="megabyte-dos-servicios-css"' in html:
    raise SystemExit('La integración ya existe. No se modificó nada.')
if '<div class="services-grid"' not in html:
    raise SystemExit('ERROR: no encontré la grilla original de servicios. No se modificó nada.')
if '</head>' not in html or '</body>' not in html:
    raise SystemExit('ERROR: HTML incompleto. No se modificó nada.')
start = html.index('<div class="services-grid"')
opening_end = html.index('>', start)+1
# Recorrer las etiquetas DIV anidadas para identificar únicamente las tarjetas.
pat = re.compile(r'<(/?)div\b[^>]*>', re.I)
level=1
cards=[]
card_start=None
end=None
for m in pat.finditer(html, opening_end):
    closing = bool(m.group(1))
    if not closing:
        if level==1: card_start=m.start()
        level+=1
    else:
        level-=1
        if level==1 and card_start is not None:
            cards.append((card_start,m.end()))
            card_start=None
        if level==0:
            end=m.end()
            break
if end is None or len(cards)!=3:
    raise SystemExit(f'ERROR: esperaba 3 tarjetas originales y encontré {len(cards)}. No modifiqué nada.')
original_cards=[html[a:b] for a,b in cards]
if not all(re.search(r'<h3[^>]*>\s*'+title+r'\s*</h3>', card, re.I) for title,card in zip(('Celulares','Notebooks','Microelectrónica'),original_cards)):
    raise SystemExit('ERROR: el orden de las tarjetas cambió. No modifiqué nada.')

def link_card(card,url,label):
    # Enlace visible, con área clicable extendida sobre toda la tarjeta.
    link=f'\n<a class="mb-servicio-enlace" href="{url}" aria-label="{label}">Ver reparaciones <span aria-hidden="true">→</span></a>\n'
    pos=card.lower().rfind('</div>')
    return card[:pos]+link+card[pos:]

first=link_card(original_cards[0],'/reparacion-celulares/','Ver reparaciones de celulares')
second=link_card(original_cards[1],'/reparacion-notebooks/','Ver reparaciones de notebooks y laptops')
# Añadir el enfoque técnico sin cambiar el texto anterior de las tarjetas.
first=first.replace('Pantallas', 'Pantallas',1)
new_grid='<div class="services-grid mb-dos-servicios">'+first+second+'</div>'
updated=html[:start]+new_grid+html[end:]
css='''\n<style id="megabyte-dos-servicios-css">
.services-grid.mb-dos-servicios{grid-template-columns:repeat(2,minmax(0,1fr))}
.mb-dos-servicios .service-card{position:relative;cursor:pointer}
.mb-dos-servicios .service-card:focus-within{outline:2px solid #00e676;outline-offset:3px}
.mb-dos-servicios .mb-servicio-enlace{display:inline-flex;gap:8px;align-items:center;margin-top:22px;color:#00e676;text-decoration:none;font-size:14px;font-weight:700}
.mb-dos-servicios .mb-servicio-enlace::after{content:"";position:absolute;inset:0}
.mb-dos-servicios .service-card:hover .mb-servicio-enlace{text-decoration:underline}
@media(max-width:768px){.services-grid.mb-dos-servicios{grid-template-columns:1fr}}
</style>\n'''
updated=updated.replace('</head>',css+'</head>',1)
# Quitar solo el banner promocional redundante de notebooks si existe.
# Se conserva el resto del sitio y todas sus funciones.
updated,n_removed=re.subn(r'\s*<section id="megabyte-notebooks-destacado"\b.*?</section>','',updated,count=1,flags=re.S)
if n_removed:
    updated=re.sub(r'\s*<style id="megabyte-notebooks-estilos"\b.*?</style>','',updated,count=1,flags=re.S)

cellpage=root/'reparacion-celulares'/'index.html'
notepage=root/'reparacion-notebooks'/'index.html'
if not cellpage.is_file():
    raise SystemExit('ERROR: falta reparacion-celulares/index.html. Extraé el ZIP completo.')
if not notepage.is_file():
    raise SystemExit('ERROR: falta la página existente reparacion-notebooks/index.html. No se modificó nada.')
# Preparar sitemap en memoria antes de escribir.
sitemap=root/'sitemap.xml'
xmlbytes=None
if sitemap.exists():
    tree=ET.parse(sitemap)
    rt=tree.getroot()
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    target='https://megabyte.uy/reparacion-celulares/'
    if not any((el.text or '').strip()==target for el in rt.iter() if el.tag.endswith('loc')):
        url=ET.SubElement(rt,f'{{{ns}}}url')
        ET.SubElement(url,f'{{{ns}}}loc').text=target
        ET.indent(tree,space='  ')
        import io
        buffer=io.BytesIO()
        tree.write(buffer,encoding='utf-8',xml_declaration=True)
        xmlbytes=buffer.getvalue()
# Respaldos únicos; no reemplazar respaldos anteriores.
import datetime
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(index,root/f'index_respaldo_{stamp}.html')
if xmlbytes is not None: shutil.copy2(sitemap,root/f'sitemap_respaldo_{stamp}.xml')
index.write_text(updated,encoding='utf-8')
if xmlbytes is not None: sitemap.write_bytes(xmlbytes)
print('OK: portada conservada; dos tarjetas con enlaces a celulares y notebooks.')
print('OK: microelectrónica integrada en las páginas de reparación.')
print('OK: sitemap actualizado si correspondía. Respaldo creado.')
print('Revisá index.html localmente ANTES de subir a GitHub.')
