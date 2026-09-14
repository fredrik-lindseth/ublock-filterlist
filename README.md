# Norsk støyliste for [uBlock Origin](https://ublockorigin.com/)

En personlig, norsk filterliste som skjuler cookie- og samtykkedialoger,
nyhetsbrevpopuper og annen unødvendig støy på norske nettsteder. Reklame
overlates i hovedsak til de vanlige uBlock-listene.

Listen dekker `.no`-domener og norske virksomheter som bruker andre
toppdomener, for eksempel `spond.com`. Regler for utenlandske nettsteder
hører hjemme i uBlocks **My filters**, ikke her.

## Installer

1. Åpne uBlock Origin → **Dashboard** → **Filter lists**.
2. Lim inn denne URL-en under **Custom**:

   ```text
   https://raw.githubusercontent.com/fredrik-lindseth/ublock-filterlist/main/filterlist
   ```

3. Trykk **Apply changes**.

## Hva listen gjør

- skjuler cookie- og samtykkebannere
- fjerner popuper, kampanjer og annet sideinnhold som forstyrrer lesingen
- reparerer scrolling på nettsteder der en skjult dialog fortsatt låser siden
- har enkelte bevisste tilpasninger for norske medier, som sport- og
  abonnementspromotering

## Legg til en regel

Bruk uBlocks elementvelger eller logger for å finne en konkret regel. Test i
en ren fane etterpå: dialogen skal være borte, siden skal kunne scrolles, og
vanlige knapper og innlogging skal fortsatt fungere.

Er scrolling låst etter at en dialog er skjult, legg domenet til i den
kommaseparerte scroll-regelen i `filterlist`, slik at vi beholder én regel:

```text
eksempel.no,andre-eksempel.no##body,html:style(overflow: auto !important)
```

Ikke legg inn globale regler som `###coiOverlay` eller globale
nettverksblokker. Avgrens alltid regelen til nettstedet den er observert på.

## Vedlikehold

Kjør den lokale, avhengighetsfrie kontrollen før du publiserer endringer:

```sh
python3 -m unittest discover
python3 scripts/audit_filterlist.py filterlist
```

Kontrollen avviser åpenbare filterfeil og varsler om globale regler,
nettverksregler uten domeneavgrensning og selektorer som kan slås sammen.
Den kan ikke avgjøre om en regel fortsatt treffer en levende side; det må
verifiseres i uBlock Origins logger eller elementvelger.
