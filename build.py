"""Bouwt index.html uit bron/pagina.html en het lege sjabloon bron/flexlijst-template.xlsx.

Gebruik (na het vervangen van het sjabloon of aanpassen van de pagina):
    python build.py
"""
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / 'bron' / 'flexlijst-template.xlsx'
PAGE = ROOT / 'bron' / 'pagina.html'
OUTPUT = ROOT / 'index.html'
MARKER = '/*__TEMPLATE_PARTS__*/null'

with zipfile.ZipFile(TEMPLATE) as z:
    names = z.namelist()
    # [Content_Types].xml vooraan, zoals Excel het zelf ook schrijft.
    names.sort(key=lambda n: n != '[Content_Types].xml')
    parts = {n: z.read(n).decode('utf-8') for n in names if not n.endswith('/')}

if 'xl/worksheets/sheet1.xml' not in parts:
    raise SystemExit('Sjabloon mist xl/worksheets/sheet1.xml')

page = PAGE.read_text(encoding='utf-8')
if page.count(MARKER) != 1:
    raise SystemExit('Plaatshouder voor het sjabloon niet (precies één keer) gevonden in pagina.html')
# '</' escapen zodat XML-inhoud het <script>-blok nooit kan afsluiten.
embedded = json.dumps(parts, ensure_ascii=False).replace('</', '<\\/')
OUTPUT.write_text(page.replace(MARKER, embedded), encoding='utf-8')
print(f'{OUTPUT.name} gebouwd ({OUTPUT.stat().st_size // 1024} KB, {len(parts)} sjabloononderdelen)')
