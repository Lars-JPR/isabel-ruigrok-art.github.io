# Handleiding

## Achtergrondinformatie

### basisbegrippen internet

Zie ook [MDN: Getting Started With the Web](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web).

#### IP address

IP addressen zijn als postcodes voor computers.
Wanneer je een bericht wilt sturen van jouw computer naar een andere computer,
wordt jouw adres en het adres van de bestemming bijgevoegd,
zodat tussenstations (routers, switches) weten waar het bericht naartoe moet
en de ontvanger een bericht terug kan sturen.

Er zijn twee soorten ip-adressen die je kunt tegenkomen: IPv4-adressen hebben 32 bits (4 bytes) en worden geschreven als vier getallen tussen 0 en 255 met puntjes: `127.17.0.1`.
Met 32 bits heb je maximaal 2³² ≈ 4 miljard adressen. Dat bleek niet genoeg te zijn, dus werd IPv6 geïntroduceerd: een IPv6-adres bestaat uit 128 bits (7 bytes) en wordt meestal zo geschreven: `2001:0db8:0000:0000:0000:ff00:0042:8329.`

Zie voor meer details [IP Address op Wikipedia](https://en.wikipedia.org/wiki/IP_address).

#### Domeinnaam

IP-adressen zijn moeilijk te onthouden of controleren; daarom hebben websites een domeinnaam.
Routers en andere tussensystemen werken echter alleen met IP-adressen.
Om het IP-adres dat bij een domeinnaam hoort te vinden, stuur je een bericht naar een Domain Name Server (waarvan je het IP-adres al weet) die je het adres terugstuurt.
Onder andere om deze servers draaiende te houden betaal je voor een domeinnaam.

Zie voor meer informatie [MDN](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_domain_name).

#### HTTP

Een protocol zijn regels die de betekenis van een bericht vastleggen.
Voor websites is het meest gebruikte protocol HTTP(S).
Een HTTP-verzoek bestaat uit de method (een woord dat aangeeft wat voor verzoek het is), de url die aangeeft om welk object het gaat, het versienummer en eventueel headers en inhoud.
Om bijvoorbeeld de hoofdpagina van Wikipedia te ontvangen stuur je:

```http
GET /wiki/Hoofdpagina HTTP/2
Host: nl.wikipedia.org
Connection: keep-alive
```

Naar het ip-adres van Wikipedia.
De regels `Host:` en `Connection:` zijn headers.
Inhoud is gescheiden van de headers door een lege regel;
in het geval van een GET-verzoek is er geen inhoud.

De wikipedia-server stuurt dan een antwoord bestaande uit het versienummer,
een status-code, en eventueel headers en inhoud.

```http
HTTP/2 200 OK
Content-Language: nl
Content-Type: text/html
Content-Length: 61

<html>
    <head> ... </head>
    <body> ... </body>
</html>
```

De status-code 200 geeft aan dat alles goed is gegaan.
Een code die begint met 4 geeft een fout van jouw kant aan,
bijvoorbeeld 404 als je een url opvraagt die niet bestaat.
Een code die begint met 5 geeft ook een fout aan,
maar aan de kant van de ontvanger,
bijvoorbeeld 503 als de server tijdelijk niet beschikbaar is voor onderhoud.

Zie voor alle status-codes [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).
En voor meer informatie natuurlijk ook [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview).

#### HTML

HTML beschrijft de structuur van webpagina's. Een html-pagina bestaat uit tekst en elementen, bijvoorbeeld een paragraaf-element:

```
<p> text </p>
```

> <u>resultaat:</u> <p> text </p>

Elementen kunnen naast tekst ook andere elementen bevatten, zoals dit nadruk-element (emphasis):

```
<p> <em>text</em> </p>
```

> <u>resultaat:</u> <p> <em>text</em> </p>

Sommige elementen hebben echter geen inhoud, zoals een horizontale lijn (horizontal rule):

```html

<hr></hr>
```

Die kun je dan ook zo schrijven:

```html

<hr/>
```

> <u>resultaat:</u> <hr/>

Elementen kunnen extra informatie meekrijgen in de vorm van attributen, bijvoorbeeld het adres van een link (anchor):
`<a href="https://developer.mozilla.org/">link</a>`

> <u>resultaat:</u> <a href="https://developer.mozilla.org/">link</a>

Meerdere attributen worden gescheiden door spaties, zoals de `src` en `alt`-attributen van een afbeelding (image), die respectievelijk de locatie en een tekstuele beschrijving geven.

`<img src="https://picsum.photos/id/1/50" alt="persoon met laptop"/>`

> resultaat: <img src="https://picsum.photos/id/1/50" alt="persoon met laptop"/>

Een HTML-bestand wordt opgedeeld in een `<head>` met informatie voor computers en een `<body>` met informatie voor mensen.

```html

<html lang="NL-nl">
<head>
    <title>Mijn Website</title>
    <link rel="stylesheet" href="style/main.css"/>
</head>
<body>
<section>
    <h1> Welkom op mijn website!</h1>
    <p><img src="https://picsum.photos/id/1/100" alt="persoon met laptop"/></p>
    <p> Mijn favoriete elementen: </p>
    <ol>
        <li><i>C</i> Koolstof</li>
        <li><i>H</i> Waterstof</li>
        <li><i>O</i> Zuurstof</li>
    </ol>
    <p> Kijk ook eens op <a href="http://hyves.nl/user/karel">mijn hyves-pagina</a></p>
</section>
</body>
</html>
```

Sommige elementen zijn alleen betekenisvol in combinatie met andere; `<ol>` is een genummerde (ordered) lijst, en elementen van die lijst moeten `<li>` (list items) zijn.
Voor een volledig overzicht van alle soorten html-elementen, zie [MDN HTML Element Reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element).
En ook voor een tutorial, je raadt het al, [MDN](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started).

> <u>resultaat:</u> <section><h1> Welkom op mijn website!</h1><p><img src="https://picsum.photos/id/1/100" alt="persoon met laptop"/></p><p> Mijn favoriete elementen: </p><ol><li> <i>C</i> Koolstof </li><li> <i>H</i> Waterstof </li><li> <i>O</i> Zuurstof </li></ol><p> Kijk ook eens op <a href="http://hyves.nl/user/karel">mijn hyves-pagina</a> </p></section>

#### CSS

We hebben met HTML de structuur van onze website beschreven,
maar het ziet er nog wel een beetje saai uit. Met CSS kunnen we de stijl van onze pagina's aanpassen.
CSS ziet er zo uit:

```css
i {
    border: 1px dimgray;
    border-radius: 4px;
    background-color: gray;
    font-size: 1.1em;
    padding-inline: 4px;
}

ol {
    list-style: lower-roman;
}
```

> <u>resultaat:</u> <div><p> Mijn favoriete elementen: </p> <ol style="list-style: lower-roman"> <li> <i style="border: 1px dimgray; border-radius: 4px; background-color: gray; font-size: 1.1em; padding-inline: 4px;">C</i> Koolstof </li> <li> <i style="border: 1px dimgray; border-radius: 4px; background-color: gray; font-size: 1.1em; padding-inline: 4px;">H</i> Waterstof </li> <li> <i style="border: 1px dimgray; border-radius: 4px; background-color: gray; font-size: 1.1em; padding-inline: 4px;">O</i> Zuurstof </li> </ol></div>

Voor de `{` staat een selector, en tussen de `{...}` staan de eigenschappen van elementen die overeenkomen met de selector.
In het voorbeeld selecteren we alleen op het type element, maar er zijn allerlei andere selectoren, zoals de kind-selector, ` ` (spatie) en de klasse-selector `.`.
`li i` selecteert alleen `<i>`-elementen in een `<li>`-element.
Klasses van een element worden als spatie-gescheiden lijst gegeven in `class`-attributen, bijvoorbeeld `<i class="symbol gas">H</h>` wordt geselecteerd door `.symbol`.

Om aan de browser te vertellen welke CSS bij je HTML-bestand hoort, gebruik je een `<link>` met `rel="stylesheet"`, zoals in het [HTML-voorbeeld](#HTML)

#### Markdown

Met de hand HTML schrijven is best wel onhandig.
Markdown bied een makkelijkere notatie voor veelgebruikte html-elementen. Het [HTML-voorbeeld](#HTML) zouden we in markdown zo kunnen schrijven:

```markdown
# Welkom op mijn website!

![persoon met laptop](https://picsum.photos/id/1/100)

Mijn favoriete elementen:

1. _C_ Koolstof
2. _H_ waterstof
3. _O_ Zuurstof

Kijk ook eens op [mijn hyves-pagina](http://hyves.nl/user/karel)
```

Browsers begrijpen geen markdown, dus moet je het omzetten in HTML, bijvoorbeeld met [pandoc](https://pandoc.org/) of [python-markdown](https://pypi.org/project/Markdown/):

```shell
python3 -m markdown blog.md > blog.html
```

Hier is de [originele markdown-specificatie](https://daringfireball.net/projects/markdown/); er zijn allerlei varianten in omloop die wat extra dingen toevoegen, zoals tabellen of voetnoten.
De variant die wij gebruiken heeft onder andere [_attribute lists_](https://python-markdown.github.io/extensions/attr_list/), waarmee je klasses, id's en andere attributen aan elementen kan toevoegen, bijvoorbeeld aan een afbeelding:

- markdown: `![profile picture](images/profile-picture.webp){.rounded #profile-picture height=200px width=200px}`
- html: `<img src="images/profile-picture.webp" alt="profile picture" class="rounded" id="profile-picture" height="200px" width="200px"/>`

#### bestandsformaten

Hoge kwaliteit afbeeldingen bestaan doorgaans uit honderdduizenden pixels.
Er zijn verschillende bestandsformaten om afbeeldingen in zo min mogelijk ruimte op te slaan en zo veel mogelijk kwaliteit te behouden.

- PNG is lossless, dat wil zeggen dat elke pixel exact kan worden gereproduceert. Dit kost echter wel nog steeds veel opslagruimte.
- JPEG is lossy, waardoor je een stuk minder opslagruimte nodig hebt. Het kwaliteitsverlies is beperkt, daarom wordt JPEG vaak gebruikt door fotocameras.
- WEBP is een recenter format, met betere kwaliteit voor dezelfde opslagruimte dan JPEG, maar het werkt niet in oudere browsers.

## Het Systeem

### Benodigdheden

#### Python

Python is een simpele programmeertaal met een groot ecosysteem aan packages voor al je informatieverwerkingsproblemen.
Voor een goede introductie, zie [de officiële Python-tutorial](https://docs.python.org/3/tutorial/index.html) (Engels).
Voor een iets minder goede introductie in het Nederlands, zie [hier](https://colab.research.google.com/drive/1Z5Wfs1YCz_VQl26chtyPc11Wl4cvVyJ1?usp=sharing).

Als Python is [geïnstalleerd](https://docs.python.org/3/using/windows.html), kun je python-programma's zoals `builder/build.py` uitvoeren met

```shell
python3 builder/build.py
```

Sommige programma's gebruiken andere programma's (packages).
Deze kun je meestal vinden in de [Python Package Index (PyPI)](https://pypi.org/) en downloaden met de [Package Installer voor Python (pip)](https://pypi.org/project/pip/).
Om bijvoorbeeld het `markdown` pakket te installeren, gebruik je

```shell
python3 -m pip install markdown
```

De nodige packages voor `build.py` staan in `builder/requirements.txt`. Je kunt ze in een keer installeren met de optie `-r`:

```shell
python3 -m pip install -r builder/requirements.txt
```

Als je op deze manier installeert zijn de packages voor je hele systeem beschikbaar.
Echter, het kan voorkomen dat programma's verschillende versies van packages nodig hebben.
Om dat soort problemen te voorkomen kun je een virtuele omgeving (virtual environment) aanmaken, zodat packages geïsoleerd zijn va de rest van het systeem:

```shell
python3 -m venv venv/ # maak een virtuele omgeving in de folder venv/
. venv/bin/activate # 'activeer' de omgeving in deze shell
```

Wanneer de virtuele omgeving actief is, zie je `(venv)` voor je prompt staan. Als je nu packages installeert, komen ze in de `venv/` folder terecht.

#### Jinja Templates

De inhoud van project-pagina's wordt beschreven in markdown, maar daar omheen moet nog wat extra html (denk aan `<title>` en `<link>`s).
Hiervoor gebruiken we Templates, zie de folder `templates/`.
Deze bestaan uit gewoon HTML met extra placeholders voor de inhoud en andere data die verschilt per pagina.

Voor een volledig overzicht van de notatie kun je de [Jinja-website](https://jinja.palletsprojects.com/en/latest/templates/) bekijken,
maar de belangrijkste is `{{ ... }}`, waarbij de spatie na `{{` en voor `}}` verplicht is.
Hierbinnen staat Python-achtige code die uitgevoerd wordt waarna het resultaat in de HTML wordt geplakt.

### Structuur

De website bestaat uit de home-pagina `/`, een lijst projecten `/projects` en stukken `/pieces`, en individuele pagina's voor projecten of stukken `/projects/naam-van-project`.

Het idee is dat een stuk-pagina een enkel object beschrijft en een project-pagina een activiteit of proces, maar functioneel zijn ze vrijwel hetzelfde.

De pagina's worden door `builder.py` gemaakt op basis van de markdown en afbeeldingen in de `source` folder:

```
source
├── homepage
│   └── about.md
├── projects
│   ├── (project-naam)
│   │   ├── (project-naam).md
│   │   ├── (afbeelding-1).jpeg
│   │   └── (afbeelding-2).jpeg
│   ├── (project-naam-2)
│   ...
├── pieces
│   ├── (stuk-naam)
│   │   ├── (stuk-naam).md
│   │   ├── (afbeelding-1).jpeg
│   │   └── (afbeelding-2).jpeg
│   ├── (stuk-naam-2)
│   ...
├── homepage
│   └── about.md
├── style
│   ├── main.css
│   ├── gallery.css
│   ...
├── images
│   ├── (afbeelding-1).jpeg
│   ├── (afbeelding-2).jpeg
│   ...
├── script
│   ├── main.js
│   ...
└── templates
    ├── gallery.html
    ├── index.html
    ├── page.html
    ├── resource_index.html
    └── resource_page.html
```

#### Projecten

Elk project heeft een korte naam (slug) die gebruikt wordt als bestandsnaam en in urls.
Voor elke folder in de folder `projects/` wordt een project-pagina en een item in de lijst projecten gemaakt.
De inhoud van de pagina wordt bepaald door een markdown-bestand met de naam `index.md` of dezelfde naam als de folder.
Het lijst-item wordt ook gebaseerd op dit markdown-bestand:

- De bovenste header (`# Project Titel`) wordt gebruikt als titel.
- Als er een afbeelding is met de klasse `.headline` wordt deze gebruikt; anders de eerste afbeelding.
- Eigenschappen als prijs en grootte worden uit de metadata gelezen (<abbr title="Not Yet Implemented">NYI</abbr>).

De algemene structuur van project-pagina's wordt bepaald door `templates/resource_page.html`, en die van de lijst door `templates/resource_index.html`

#### Stukken

Stukken werken vrijwel hetzelfde als projecten, maar moeten in de folder `pieces/` geplaatst worden.

#### Home-pagina

Het stukje tekst op de homepagina komt uit `about.md`; de rest wordt bepaald door het template `templates/index.html`.

#### Images, Style, Script, favicon.ico

De folders `images/`, `style/` en `script/` en het bestand `favicon.ico` worden gekopieerd.
`images/` bevat afbeeldingen die niet bij een bepaald stuk of project horen, `style/` bevat de [stylesheets](#css) en `script/` scripts.
`favicon.ico` is het icoontje dat wordt weergegeven naast de titel van het tabblad of in je favorieten. Je kunt afbeeldingen omzetten naar `.ico`-formaat met bijvoorbeeld GIMP.

### Documenten schrijven

Markdown-documenten worden omgezet naar html volgens de [standaard markdown-regels](https://daringfireball.net/projects/markdown/syntax), met enkele extra functionaliteiten:

#### 1. Afbeeldingen

[PNG](#bestandsformaten)-afbeeldingen worden automatisch omgezet in [WebP](#bestandsformaten); de PNG-versie blijft beschikbaar voor oudere browsers door de `<img>`es om te zetten in `<figure>`s.

#### 2. Klasses

Je kunt [klasses](#css) aan bepaalde elementen zoals afbeeldingen toevoegen met `{.klasse-naam}`, bijvoorbeeld

```markdown
![vooraanzicht](/pieces/backyard/backyard.png){.left .grayscale}
```

om de afbeelding de klasses `left` en `grayscale` te geven.

Op het moment van schrijven zijn de volgende klasses gedefinieerd:

- `left`, `right`: plaats de afbeelding aan de linker- of rechterkant van de pagina en laat tekst er omheen lopen. (als de pagina breed genoeg is)
- `center`: plaats de afbeelding in het midden, zonder tekst ernaast.
- `fullwidth`: gebruik alle beschikbare breedte (dit is niet altijd de volledige breedte van de pagina)
- `halfwidth`: gebruik de helft van de beschikbare breedte

Je kunt meer klasses definiëren in `style/main.css`

#### 3. Metadata

Extra informatie die niet in de lopende text past kan worden opgenomen in een metadata-blok aan het begin van het document.
Dit blok begint en eindigt met een regel `---` en bestaat uit variabele-namen en -waarden:

```yaml
---
date: 2023-09-30
---
```

De variabele `date` geeft een datum (`yyyy-mm-dd`) die wordt gebruikt om de projecten-lijst te sorteren.

#### Tips

In HTML zijn afbeeldingen (`<img>`) inline-elementen, dat wil zeggen dat ze onderdeel zijn van de lopende tekst.
Om afbeeldingen te scheiden van de tekst moet je ze in een eigen blok-element plaatsen.
In markdown doe je dit door een lege regel voor en na de afbeelding-notatie te plaatsen:
dit start een nieuwe paragraaf (`<p>`).

```markdown
tekst tekst tekst!
![koe](https://picsum.photos/id/200/50)
```

wordt

```html
<p>tekst tekst tekst!
<img alt="koe" src="https://picsum.photos/id/200/50"/></p>
```

en omdat HTML regeleindes negeert, ziet dat er uit als:

> <p>tekst tekst tekst!
> <img alt="koe" src="https://picsum.photos/id/200/50" /></p>

maar

```markdown
tekst tekst tekst!

![koe](https://picsum.photos/id/200/50)
```

wordt

```html
<p>tekst tekst tekst!</p>
<p><img alt="koe" src="https://picsum.photos/id/200/50"/></p>
```

met twee aparte paragrafen, dus

> <p>tekst tekst tekst!</p><p><img alt="koe" src="https://picsum.photos/id/200/50" /></p>

### De site bouwen en bekijken

Wanneer je alle [benodigdheden](#benodigdheden) hebt geïnstalleerd, kun je de site bouwen met

```shell
python3 builder/build.py
```

Het resultaat wordt in de folder `generated/` geplaatst.

Als je probeert de gegenereerde pagina's te openen in je browser door het volledige pad te kopiëren, zie je wel de tekst, maar afbeeldingen en links werken niet, omdat de browser niet weet wat de basisfolder van je site is.
Je kunt een lokale server opstarten door in de `generated/` folder het volgende commando uit te voeren: `python3 -m http.server`. Als je de resulterende link opent op dezelfde computer zie je het resultaat.
Je kunt deze lokale server ook bereiken vanaf andere apparaten in je lokale netwerk (i.e. je telefoon op hetzelfde wifi-netwerk) als je het locale ip-adres van je computer weet. Dit kun je vinden met bijvoorbeeld

```shell
ip address | grep 'scope global' | grep 'inet '
```

Type het adres tot aan de `/` over, en type er de poort achter (meestal `:8000`).

Als je Visual Studio Code gebruikt, kun je een live server opstarten met de Live Preview extensie.
Verander eerst de [livePreview.serverRoot](vscode://settings/livePreview.serverRoot) instelling naar `generated/` en start dan de server vanuit het Command Pallette (F1) met 'Live Preview: Start Server'.
Het voordeel hiervan is dat de pagina automatisch wordt herladen wanneer de site veranderd.

Om je veranderingen in markdown snel om te zetten naar html, kun je een build task instellen door het volgende in `.vscode/tasks.json` te zetten:

```json5
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "venv/bin/python3 builder/build.py",
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

Nu kun je de site herbouwen door `Ctrl + Shift + B` in te drukken.

### Uploaden

De site wordt gehost met GitHub pages.
Veranderingen op de `main` branch worden automatisch verwerkt tot een nieuwe versie van de site met GitHub Actions.
'✔️ 2/2' naast een commit geeft aan dat deze versie successvol gebouwd en geupoad is.