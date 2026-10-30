# Flexlijst maken

Bundelt de exports van de uitzendbureaus tot één standaard NBC-flexlijst in Excel, op basis van het goedgekeurde sjabloon *Flexlijst extern personeel*:

| Bureau | Export | Kolom *Externe partij* |
| --- | --- | --- |
| Temper | CSV met geplande diensten | Temper |
| Piekfijn | Presentielijst (PDF, *Afdrukken → Opslaan als PDF*) | Piekfijn |
| Dish | Dagplanning ZZP'ers (PDF) | Dish (ZZP) |

Sleep één of meer bestanden tegelijk op de pagina; de pagina herkent zelf welk bureau het is. Dish geeft geen eindtijd, daar komt *vanaf 08:00* te staan. Staat dezelfde persoon met dezelfde tijden in twee exports, dan blokkeert de pagina tot de dubbele export is verwijderd.

**Gebruiken:** https://marketing-nbc.github.io/flexlijst/

Alles gebeurt in de browser: de exports en de flexlijst verlaten de computer niet (de pagina mag niets via internet ophalen of versturen) en er wordt niets opgeslagen, behalve in deze browser de keuze welke onbekende functie bij welke afdeling hoort. Er wordt alleen datum, functie/afdeling, tijden en naam gelezen; telefoonnummers en e-mailadressen worden direct uit de naam gehaald (Dish zet het telefoonnummer achter de naam). Deze repository is openbaar en bevat alleen het lege sjabloon, de functie-indeling en de code — **zet hier nooit exports of ingevulde flexlijsten neer.**

## Bestanden

| Bestand | Wat |
| --- | --- |
| `index.html` | De pagina zelf (gegenereerd, niet met de hand aanpassen) |
| `bron/pagina.html` | Bron van de pagina: opmaak, indeling en logica |
| `bron/flexlijst-template.xlsx` | Het lege, goedgekeurde sjabloon |
| `bron/pdfjs/` | PDF-lezer [pdf.js](https://github.com/mozilla/pdf.js) 4.10.38 (Apache-2.0), wordt in de pagina ingebouwd |
| `build.py` | Voegt het sjabloon en pdf.js in de pagina in en schrijft `index.html` |

## Aanpassen

- **Nieuwe vaste functie:** voeg een regel toe aan `MAPPING` in `bron/pagina.html`, bijvoorbeeld `'Barmedewerker': 'Events & Hospitality',`. Piekfijn-functies (zoals *Bediening*) staan daar ook; bij Dish wordt de afdeling uit de groepsregel gebruikt (*NBC > **Keuken** > Freelance - A*).
- **Nieuw sjabloon:** vervang `bron/flexlijst-template.xlsx`. De zes afdelingen moeten op dezelfde rijen blijven staan (koppen op rij 3, 7, 11, 15, 19 en 23, elk met twee dienstregels); anders ook `SECTIONS` in `bron/pagina.html` aanpassen.

Daarna:

```bash
python build.py
git add -A && git commit -m "Beschrijving van de wijziging" && git push
```

GitHub Pages zet de nieuwe versie binnen een minuut online.
