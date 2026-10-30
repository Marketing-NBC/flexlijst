"""Bouwt index.html uit bron/pagina.html, het lege sjabloon bron/flexlijst-template.xlsx
en de PDF-lezer in bron/pdfjs/.

Gebruik (na het vervangen van het sjabloon of aanpassen van de pagina):
    python build.py
"""
import json
import pathlib
import re
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / 'bron' / 'flexlijst-template.xlsx'
PAGE = ROOT / 'bron' / 'pagina.html'
PDFJS = ROOT / 'bron' / 'pdfjs'
OUTPUT = ROOT / 'index.html'
MARKER = '/*__TEMPLATE_PARTS__*/null'
PDF_MARKER = '<!--__PDFJS__-->'

with zipfile.ZipFile(TEMPLATE) as z:
    names = z.namelist()
    # [Content_Types].xml vooraan, zoals Excel het zelf ook schrijft.
    names.sort(key=lambda n: n != '[Content_Types].xml')
    parts = {n: z.read(n).decode('utf-8') for n in names if not n.endswith('/')}

if 'xl/worksheets/sheet1.xml' not in parts:
    raise SystemExit('Sjabloon mist xl/worksheets/sheet1.xml')


def inline_module(path, global_name):
    """Maakt van een ES-module een inline <script type="module"> die zijn exports op globalThis zet.

    Zo is er geen los bestand, geen worker en geen netwerkverzoek nodig (CSP blijft dicht).
    """
    src = path.read_text(encoding='utf-8')
    m = re.search(r'export\{([^}]*)\};?\s*$', src)
    if not m or src.count('export{') != 1 or re.search(r'(^|[;}])import[\s{]', src):
        raise SystemExit(f'{path.name}: onverwachte opbouw, kan niet inline worden gezet')
    pairs = [p.strip().split(' as ') for p in m.group(1).split(',')]
    exports = ','.join(f'{alias}:{local}' for local, alias in pairs)
    src = src[:m.start()] + f'globalThis.{global_name}={{{exports}}};'
    if re.search(r'</script|<!--|<script', src, re.I):
        raise SystemExit(f'{path.name} bevat tekst die een <script>-blok kan breken')
    return f'<script type="module">{src}</script>'


page = PAGE.read_text(encoding='utf-8')
if page.count(MARKER) != 1:
    raise SystemExit('Plaatshouder voor het sjabloon niet (precies één keer) gevonden in pagina.html')
if page.count(PDF_MARKER) != 1:
    raise SystemExit('Plaatshouder voor pdf.js niet (precies één keer) gevonden in pagina.html')
# '</' escapen zodat XML-inhoud het <script>-blok nooit kan afsluiten.
embedded = json.dumps(parts, ensure_ascii=False).replace('</', '<\\/')
# Worker eerst: pdf.js gebruikt dan globalThis.pdfjsWorker in plaats van een los worker-bestand.
pdfjs = (inline_module(PDFJS / 'pdf.worker.min.mjs', 'pdfjsWorker') + '\n' +
         inline_module(PDFJS / 'pdf.min.mjs', 'pdfjsLib'))
page = page.replace(MARKER, embedded)
page = page.replace(PDF_MARKER, pdfjs)
OUTPUT.write_text(page, encoding='utf-8')
print(f'{OUTPUT.name} gebouwd ({OUTPUT.stat().st_size // 1024} KB, {len(parts)} sjabloononderdelen, pdf.js ingebouwd)')
