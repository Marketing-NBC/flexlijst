# Flexlijst maken

Zet een Temper-export (CSV) om naar de standaard NBC-flexlijst in Excel, op basis van het goedgekeurde sjabloon *Flexlijst extern personeel*.

**Gebruiken:** https://marketing-nbc.github.io/flexlijst/

Alles gebeurt in de browser: de CSV en de flexlijst verlaten de computer niet. Deze repository is openbaar en bevat alleen het lege sjabloon, de functie-indeling en de code — **zet hier nooit exports of ingevulde flexlijsten neer.**

## Bestanden

| Bestand | Wat |
| --- | --- |
| `index.html` | De pagina zelf (gegenereerd, niet met de hand aanpassen) |
| `bron/pagina.html` | Bron van de pagina: opmaak, indeling en logica |
| `bron/flexlijst-template.xlsx` | Het lege, goedgekeurde sjabloon |
| `build.py` | Voegt het sjabloon in de pagina in en schrijft `index.html` |

## Aanpassen

- **Nieuwe vaste functie:** voeg een regel toe aan `MAPPING` in `bron/pagina.html`, bijvoorbeeld `'Barmedewerker': 'Events & Hospitality',`.
- **Nieuw sjabloon:** vervang `bron/flexlijst-template.xlsx`. De zes afdelingen moeten op dezelfde rijen blijven staan (koppen op rij 3, 7, 11, 15, 19 en 23, elk met twee dienstregels); anders ook `SECTIONS` in `bron/pagina.html` aanpassen.

Daarna:

```bash
python build.py
git add -A && git commit -m "Beschrijving van de wijziging" && git push
```

GitHub Pages zet de nieuwe versie binnen een minuut online.
