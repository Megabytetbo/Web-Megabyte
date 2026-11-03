from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

site = Path.cwd()
index = site / "index.html"
page = site / "reparacion-notebooks" / "index.html"
if not index.is_file():
    raise SystemExit("ERROR: ejecutá el script desde la carpeta que contiene index.html.")
if not page.is_file():
    raise SystemExit("ERROR: falta reparacion-notebooks/index.html. Extraé esa carpeta del ZIP anterior.")
original = index.read_text(encoding="utf-8-sig")
if "<html" not in original.lower() or "</body>" not in original.lower() or "</head>" not in original.lower():
    raise SystemExit("ERROR: el index.html no parece completo. No se modificó nada.")
style = """\n<style id="megabyte-notebooks-estilos">\n#megabyte-notebooks-destacado{padding:64px 24px;background:#101810;color:#f0f0f0;border-top:1px solid #294332;border-bottom:1px solid #294332;font-family:Inter,Arial,sans-serif}\n#megabyte-notebooks-destacado .mb-wrap{max-width:1120px;margin:auto;display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center}\n#megabyte-notebooks-destacado .mb-label{color:#00e676;font-size:12px;letter-spacing:2px;text-transform:uppercase;font-weight:700}\n#megabyte-notebooks-destacado h2{font-size:clamp(27px,4vw,43px);line-height:1.15;margin:12px 0 18px}\n#megabyte-notebooks-destacado p{color:#b8c2ba;font-size:16px;max-width:660px;line-height:1.65}\n#megabyte-notebooks-destacado .mb-link{display:inline-block;background:#00e676;color:#07150b;padding:16px 24px;text-decoration:none;border-radius:8px;font-weight:800;white-space:nowrap}\n#megabyte-notebooks-destacado .mb-link:hover{background:#65ffae}\n@media(max-width:700px){#megabyte-notebooks-destacado .mb-wrap{grid-template-columns:1fr}#megabyte-notebooks-destacado .mb-link{text-align:center;white-space:normal}}\n</style>\n"""
section = """\n<section id="megabyte-notebooks-destacado" aria-labelledby="mb-notebooks-titulo">\n  <div class="mb-wrap">\n    <div>\n      <div class="mb-label">Servicio técnico especializado · Tacuarembó</div>\n      <h2 id="mb-notebooks-titulo">Reparación de notebooks y laptops</h2>\n      <p>¿Tu notebook no enciende, no carga o tiene problemas de pantalla, bisagras o rendimiento? En MegaByte realizamos diagnóstico y reparación electrónica de placas madre a nivel de componentes.</p>\n    </div>\n    <a class="mb-link" href="/reparacion-notebooks/">Conocer el servicio →</a>\n  </div>\n</section>\n"""
updated = original
if 'id="megabyte-notebooks-estilos"' not in updated:
    updated = updated.replace("</head>", style + "</head>", 1)
if 'id="megabyte-notebooks-destacado"' not in updated:
    updated = updated.replace("</body>", section + "</body>", 1)
if updated != original:
    backup = site / "index.html.respaldo_antes_notebooks"
    if not backup.exists():
        shutil.copy2(index, backup)
    index.write_text(updated, encoding="utf-8")
    print("OK: sección de notebooks agregada sin borrar la portada.")
else:
    print("OK: la sección de notebooks ya estaba agregada. No se duplicó.")
# No copiar la página sobre sí misma: ya está en su carpeta.
print("OK: página de notebooks encontrada:", page)
sitemap = site / "sitemap.xml"
if sitemap.exists():
    tree = ET.parse(sitemap)
    rt = tree.getroot()
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    target = "https://megabyte.uy/reparacion-notebooks/"
    if not any((e.text or "").strip() == target for e in rt.iter() if e.tag.endswith("loc")):
        backup_map = site / "sitemap.xml.respaldo_antes_notebooks"
        if not backup_map.exists():
            shutil.copy2(sitemap, backup_map)
        url = ET.SubElement(rt, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = target
        ET.indent(tree, space="  ")
        tree.write(sitemap, encoding="utf-8", xml_declaration=True)
        print("OK: sitemap actualizado.")
    else:
        print("OK: sitemap ya incluye la página. No se duplicó.")
print("TERMINADO: revisá la portada antes de subir los cambios a GitHub.")
