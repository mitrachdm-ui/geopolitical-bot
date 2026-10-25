# Redaktion – Geopolitical_

## Aufbau jedes Videos (Langformat 40–45 Sek., 5–6 Folien; Kurzformat siehe Längen-Test)

| Teil | Zeit | Inhalt |
|---|---|---|
| Hook | 0–3 s | Eine große Zahl + ein Satz. Muss ohne Ton verständlich sein. Regeln siehe „Hook-Regeln“. |
| Hauptthema | 3–25 s | Was ist passiert, warum wichtig – 2 Folien |
| Thema 2/3 | 25–40 s | Je 1 Folie, kurz |
| Markt | 40–50 s | Öl / Gold / Indizes / Zinsen – nur Fakten |
| Ausblick | 50–55 s | 2–3 Termine der nächsten Tage |
| CTA | letzte 5 s | „Folge Geopolitical_…“ + Frage für Kommentare |

## Sprache (für die KI-Stimme)

- Kurze Sätze, max. 15 Wörter. Ein Gedanke pro Satz.
- Zahlen im `say`-Text ausschreiben („hundertzehn Dollar“), auf der Folie als Ziffer.
- Abkürzungen auflösen oder erklären („die US-Notenbank Fed“).
- Geopolitical_ wird „Geopolitical“ gesprochen.

## Hook-Regeln (Pflicht, aus Analyse 18.–20.10.2026)

Alle drei ersten Videos verloren die meisten Zuschauer bei **0:01** (nach 4 s nur noch ~25 %). Darum:

1. **Die Zahl muss ohne Kontext „Wow“ sein:** Menge, Preis, Rekord, Anteil („110 $“, „1.015 Drohnen“, „10 Schiffe“). **Keine Jahreszahl** als Hook-Zahl („2027“ verwirrt).
2. **Erster gesprochener Satz = die Zahl selbst**, max. 10 Wörter („Hundertzehn Dollar. So teuer war Öl seit Mai nicht.“). Kein „Heute…“, kein Kanalname, kein Datum.
3. **Hook-Titel max. 6 Wörter.** Steht groß unter der Zahl.
4. **Top-Thema nach Relevanz fürs DACH-Publikum** (45+, eher männlich, Börse/Öl-Interesse): Krieg in Europa, Energie/Öl, Börse, Zinsen, China/Taiwan > Gipfel, Konferenzen, Personalien. Lieber das relevanteste bestätigte Thema als das neueste.
5. Die Quelle der Hook-Zahl steht nicht auf Folie 1 (Renderer blendet sie dort aus) → **auf Folie 2 wiederholen** (gleiches Thema vertiefen) und in POSTEN.txt.
6. **Länge hart:** Werktags nie über 45 s, Serien (Sa/So) nie über 50 s (Renderer warnt erst ab 60 s – die Grenze hier gilt trotzdem). Kürzere Videos hielten besser (41 s: 23 % Ø gesehen vs. 54 s: 8 %; Stand 23.10.: kurz 18 Likes je 1.000 Aufrufe vs. lang 7, Saudi-Arabien 57 s auf TikTok 261 Aufrufe vs. 41-s-Fassung auf YouTube 608).

**Animation (seit 20.10.):** Jede Folie wird animiert gerendert – Tag/Titel fliegen ein, Stichpunkte erscheinen nacheinander im Takt der Stimme (darum pro Folie 2–3 Stichpunkte, in der Reihenfolge des Sprechertexts), Fortschrittsbalken läuft mit, Zahlen zählen hoch. Dezente Soundeffekte (Wusch beim Folienwechsel, Klick je Stichpunkt, Puls im Hintergrund) – abschaltbar mit `"sfx": false` in slides.json.

**Weltkarte (seit 20.10.):** Hintergrund ist eine Weltkarte; die Länder des Themas leuchten rot und pulsieren, die Karte zoomt auf die Region. Länder werden automatisch aus dem Tag erkannt (z. B. „JEMEN · SAUDI-ARABIEN“, „RIAD“, „HORMUS“). Sonst in slides.json pro Folie `"map": ["SAU", "YEM"]` (ISO-3-Codes) setzen; `"map": []` = nur Weltkarte. Das zuerst genannte Land ist der Hauptschauplatz: Es bestimmt den Ausschnitt und leuchtet kräftig rot, weitere Länder schwächer bzw. nur umrandet. Darum im Tag den Schauplatz zuerst nennen („TAIWAN · CHINA“, nicht „CHINA · TAIWAN“). Bei Markt-/Ölfolien ohne Land bleibt die Weltkarte ohne Markierung.

**Globus-Übergang (seit 22.10.):** Bei jeder Folie mit neuem Schauplatz dreht sich zuerst ein 3D-Globus vom letzten zum neuen Land (Land leuchtet), dann Zoom in die flache Karte (ca. 1,4 s). Gleicher Schauplatz wie vorher oder Folien ohne Land: kein Globus. Abschalten pro Folie mit `"globe": false`.

Der Renderer setzt automatisch um: Folie 1 ohne Kopfzeile/Datum/Fußzeile, Stimme ab 0,0 s, Zahl zählt hoch, Punch-in-Zoom, Farbschein hinter der Zahl, stärkerer Zoom auf allen Folien.

## Regionen-Mix (Pflicht, seit 20.10.2026)

Publikum: DACH, 45+. Wir sind ein Weltlage-Kanal, kein Nahost-Kanal.

1. **Höchstens 2 Top-Themen pro Kalenderwoche aus derselben Region** (Regionen: Europa/Ukraine-Russland · Nahost/Golf · Asien-Pazifik · Amerika · Afrika). Ausnahme nur bei einer klar größeren Lage (z. B. neue Kriegshandlung mit direkter Wirkung auf Europa) – Begründung in research.md.
2. **Jedes Video enthält mindestens ein Thema aus einer anderen Region** als das Top-Thema (Kurzformat: in der Markt- oder Ausblick-Zeile reicht ein Satz).
3. **Bei gleichwertigen Themen gewinnt Europa/Ukraine oder ein Thema mit direkter Folge für Deutschland** (Energiepreise, Exporte, Zölle, Sicherheit).
4. **Öl ist Markt, kein Selbstläufer:** Der Ölpreis gehört auf die Markt-Folie; Top-Thema nur bei außergewöhnlicher Bewegung.
5. Vor der Themenwahl die Spalte „Region“ in `published/log.md` der letzten 7 Tage prüfen. Jede neue Log-Zeile bekommt die Region des Top-Themas.
6. Die Sonntagsauswertung zählt den Regionen-Mix und empfiehlt keine Serien, die Regel 1 brechen.

## Frage am Ende (CTA, seit 21.10.2026)

Format: **zwei gleichwertige Optionen, Antwort per Emoji.** Leicht zu beantworten, neutral.
- Muster: „<Option A> <Emoji A> oder <Option B> <Emoji B>? Schreib <Emoji A> oder <Emoji B>.“
- Beispiel: „Mehr Marineschutz 🛡️ oder Lösung am Verhandlungstisch 🕊️? Schreib 🛡️ oder 🕊️.“
- Beide Optionen müssen legitim und gleich sachlich formuliert sein – keine Suggestivfrage, keine Wertung, keine Parteinahme, keine Personen/Parteien zur Wahl stellen.
- Kein „Muss/Soll X …?“ (zu aufwendig, politisch aufgeladen).
- **Keine Emojis auf den Folien** (slides.json: title, bullets, big, tag): Die Renderer-Schrift (Inter) hat keine Emoji-Zeichen, sie erscheinen als „NO GLYPH“-Kästchen (Fehler am 22.10.). Auf der Folie mit Worten („Schreib Schild oder Taube.“), im say-Text genauso. Emojis nur in POSTEN.txt.
- Die Frage steht vorerst **nur am Ende** des Videos (nicht in der ersten Caption-Zeile).

## Erster Kommentar (KOMMENTAR.txt, seit 24.10.2026)

Bisher fast keine Kommentare (Stand 23.10.: 1 Kommentar auf 6 Videos). Ein angepinnter erster Kommentar senkt die Hürde.
- Jeder Videoordner bekommt `KOMMENTAR.txt` (max. 150 Zeichen): die CTA-Frage mit den beiden Emojis **plus** ein belegter Zusatzfakt aus research.md, der nicht im Video vorkommt („Zum Vergleich: Vor einem Jahr kostete Brent 74 $. Mehr Schutz 🛡️ oder Verhandlungen 🕊️?“).
- Nur Fakten aus research.md (bestätigt), neutral, keine Links.
- **Denny** postet ihn direkt nach dem Video von Hand und pinnt ihn an (TikTok: Kommentar lange drücken → Anpinnen; YouTube: ⋮ → Anpinnen). Nie automatisch.
- Antworten auf Kommentare in der ersten Stunde (Denny, von Hand) helfen der Verteilung am meisten.

## Hook-Formeln

- **Rekord:** „Zehn Schiffe in einer Woche angegriffen. Das gab es noch nie.“
- **Zahl + Warum:** „Öl kostet 110 Dollar. Hier sind die drei Gründe.“
- **Folge für dich:** „Das kann Tanken teurer machen.“ – immer „kann“, nie „wird“, und nur mit Quelle (Stopp-Regel: keine Vorhersagen als Tatsache)
- **Frage:** „Warum redet plötzlich jeder über Taiwan?“

## Farben auf den Folien

- Tag rot = Konflikt/Krise · amber = Rohstoffe/Termine · blau = Märkte/Politik
- `▲` grün / `▼` rot · `!▲` = steigt, ist aber negativ (VIX, Renditen, Inflation) → rot

## Rotierende Formate (Content-Plan)

| Tag | Format |
|---|---|
| Mo–Fr | **Tageslage** – Top-Thema + 2 Nebenthemen + Markt |
| Samstag | **Serie „WOCHENRÜCKBLICK“ – „Untergegangen diese Woche“** (ab 24.10.2026). Aufbau (6 Folien, ≤ 50 s): Hook (z. B. `"big": "3"` + „Meldungen, die diese Woche untergingen“) → **3 Folien** mit je einem relevanten Ereignis der letzten 7 Tage, das in keinem Video Mo–Fr Top- oder Nebenthema war (published/log.md und slides.json der Woche prüfen), möglichst 3 verschiedene Regionen (Afrika, Lateinamerika, Asien, Europa bevorzugt), jedes nach 3-Quellen/2-Regionen-Regel belegt – nicht belegbare Themen weglassen, notfalls 2 statt 3 → **1 Folie „Nächste Woche wichtig“** mit 2–3 feststehenden, offiziell angekündigten Terminen (Zinsentscheide, Wahlen, Gipfel, OPEC, Fristen; `"cal"` für den wichtigsten Termin) → CTA „Folge Geopolitical_ – jeden Samstag, was untergegangen ist.“ + Frage. In slides.json `"series": "WOCHENRÜCKBLICK"` (Look: Anthrazit, Gold). Je Ereignis-Folie Land im Tag (Karte). Keine Prognosen als Tatsache. |
| Sonntag | **Serie „SONNTAG ERKLÄRT“** – in slides.json `"series": "SONNTAG ERKLÄRT"` setzen (Renderer schaltet auf den eigenen Look: helles Atlas-Papier, Türkis, nummerierte Stichpunkte, Serien-Logo). CTA: „Folge Geopolitical_ – jeden Sonntag erklären wir ein Thema.“ Format: **Erklär-Video** – ein Hintergrund (z. B. „Was ist die Straße von Hormus?“, „Wie wirken Sanktionen?“, „Wer sind die Houthis?“) |
| Bei Eilmeldung | **Breaking** – 20–30 Sek., nur ein Thema |

Erklär-Ideen auf Vorrat (Reihenfolge = Priorität, oberstes passendes Thema nehmen und danach streichen; Regionen-Mix beachten):
1. **Vorrang – Energie & Wirtschaft (Bezug Deutschland):** Wie funktioniert der Ölpreis – und warum zahlen wir mehr an der Tankstelle? (**Pflicht-Inhalt:** Preisbestandteile eines Liters Super/Diesel in Deutschland zerlegen – Produkt/Rohöl, Raffinerie & Händlermarge, Energiesteuer, CO₂-Preis, Mehrwertsteuer (auch auf die Steuern) – mit aktuellem Literpreis und Steueranteil; Quellen: ADAC, Zoll/BMF, Destatis/en2x + mind. eine internationale Quelle zum Rohölpreis. Dafür die animierte Preis-Zerlegung nutzen: Folie mit `"stack"` (Teile von unten nach oben, Steuerteile mit `"mark": true`, `"highlight": "X € an den Staat"`, kein Tag auf dieser Folie) – Muster: `videos/2026-10-23_Beispiel-Sonntag-Spritpreis/slides.json`.) · Was sind Sanktionen – und wirken sie? · Straße von Hormus: Nadelöhr fürs Öl der Welt
2. **Europa & Sicherheit:** Suwalki-Lücke · Kaliningrad: Russlands Exklave in der EU · NATO-Artikel 5: Was passiert im Ernstfall? · Warum die Ostsee so wichtig ist
3. **Asien:** Taiwan & Chips · Südchinesisches Meer: Wem gehört das Wasser? · Straße von Malakka
4. **Weltordnung:** BRICS – Gegenmodell zum Westen? · UN-Sicherheitsrat: Warum er sich blockiert · Arktis: Wettlauf ums Eis
5. **Weitere:** OPEC+ · Strategische Ölreserve · Houthis · Rubel/Ölpreisdeckel · Fed & Ölpreis

## Stil „Sonntag erklärt“ – spannend statt Vorlesung (ab 25.10.2026)

Seriös bleibt Pflicht, aber das Video soll Spaß machen:
- **Überraschung im Hook:** eine Zahl, die den Alltag trifft („Fast die Hälfte deines Spritpreises geht an den Staat.“) – nur wenn belegt.
- **Du-Ansprache und Alltagsvergleiche:** „Stell dir vor …“, „Beim nächsten Tanken …“, Vergleiche in Dingen, die man kennt (Tankfüllung, Döner, Monatsmiete).
- **Spannungsbogen:** jede Folie endet mit einer kleinen offenen Frage oder einem Twist, den die nächste auflöst („Und jetzt kommt der Teil, der richtig teuer ist.“).
- **Ein Aha-Moment** pro Video, der zum Weiterleiten einlädt („Wusstest du, dass auf die Steuer noch Steuer kommt?“).
- **Rhythmus:** kurze Sätze, Tempo variieren, maximal eine Zahl pro Satz.
- **Erlaubt:** leichter Humor und Ironie über Sachverhalte. **Verboten:** Spott über Personen, Parteien oder Länder, Wertungen („Abzocke“), politische Forderungen.
- **CTA-Frage** zum Mitmachen: „Was hast du zuletzt pro Liter bezahlt? Schreib's in die Kommentare.“

## Hashtags (3–5 pro Video, präzise)

- Immer 1–2 Kern: #geopolitik #weltlage
- Dazu 2–3 Thema/Region: #iran #hormus #nahost #ukraine #russland #china #taiwan #usa #israel #eu #ölpreis #börse #inflation
- Nicht verwenden: #fyp #viral #foryou #lernenmittiktok (wirkt unseriös)

## Quellen & Faktencheck (Pflicht)

**Regel:** Eine Nachricht kommt nur ins Video, wenn sie von **mindestens 3 unabhängigen Quellen aus mindestens 2 Weltregionen** bestätigt ist.

Pflicht-Abgleich bei jedem Thema:
- **Westen:** Reuters, AP, BBC, NYT, WSJ, FT, Tagesschau, Handelsblatt
- **Nahost:** Al Jazeera (Katar), Times of Israel, Arab News (Saudi-Arabien), Middle East Eye
- **Asien:** SCMP (Hongkong), Nikkei Asia (Japan), The Hindu (Indien), Straits Times (Singapur)
- **Russland/Ukraine:** Kyiv Independent, Meduza (unabhängig, russisch); Staatsmedien (TASS, RT, Xinhua, Press TV) nur als „laut russischen/chinesischen/iranischen Staatsmedien …“ – **zählen nie als unabhängige Bestätigung**
- **Fachquellen:** UKMTO, IEA, EIA, ISW, OPEC, WHO, Zentralbanken

Achtung: Viele Zeitungen übernehmen dieselbe Agenturmeldung (Reuters/AP). Das zählt als **eine** Quelle, nicht als mehrere.

Formulierung:
- Bestätigt (3+ Quellen, 2+ Regionen) → als Fakt, mit „laut …“
- Nur 1–2 Quellen oder nur eine Seite → „Berichten zufolge …“ oder weglassen
- Konfliktparteien widersprechen sich → beide Versionen nennen („Iran spricht von Minen, die USA von Angriffen“)
- Zahlen von Konfliktparteien (Opfer, Abschüsse) nie ungeprüft übernehmen

## Stopp-Regel

- Ist das Top-Thema nicht nach obiger Regel belegt oder widersprechen sich die Quellen ohne Klärung → **kein Video**. Stattdessen Meldung „NEEDS-VERIFICATION“ an Denny mit dem offenen Punkt.
- Laufende Ereignisse („Breaking“) erst bringen, wenn bestätigt. Lieber einen Tag später als falsch.
- Keine Vorhersagen als Tatsache („X wird passieren“), keine Wahlwerbung, keine Spendenaufrufe, keine Partei ergreifen.

## research.md (Quellenprotokoll, pro Video Pflicht)

Für jede Aussage im Video: Aussage · Quelle(n) mit URL · Veröffentlichungsdatum · Region · **Ursprung** (wer hat es zuerst/eigenständig festgestellt: z. B. „Reuters-Meldung, von AP/Al Jazeera übernommen“ oder „UKMTO-Mitteilung“, „Angabe des russischen Verteidigungsministeriums“) · **unabhängige Bestätigungen** (Anzahl eigenständiger Ursprünge) · Status (bestätigt / Berichten zufolge). Drei Medien, die dieselbe Ursprungsaussage wiedergeben, sind **eine** Bestätigung – das muss in der Tabelle erkennbar sein. Geht eine Aussage nur auf eine Konfliktpartei zurück, bleibt sie „laut …“, egal wie viele Medien sie bringen. Am Ende: offene Unsicherheiten. Dient als Beleg, falls ein Video angezweifelt wird.

## Korrekturen

Fehler im veröffentlichten Video → sofort Korrektur-Kommentar (anpinnen) bzw. Folgevideo **auf beiden Plattformen** (TikTok und YouTube-Short desselben Tages), nie still löschen. Eintrag in `published/korrekturen.md` (Datum, Plattform, Video, Fehler, Korrektur).

## Längen-Test (19.10.–01.11.2026, angepasst ab 24.10.)

- Mo / Mi / Fr: **Kurzformat** 30–35 s – 4–5 Folien, ca. 55–62 Wörter, 1 Thema
- Di / Do: **Langformat** 40–45 s – 5–6 Folien, ca. 85–95 Wörter, max. 2 Themen (hart ≤ 45 s)
- Sa (Rückblick) / So (Erklärvideo): 45–50 s – 6 Folien, ca. 95–105 Wörter (hart ≤ 50 s); beim Rückblick 3 statt 4 Ereignis-Folien
- Grund der Anpassung (Zwischenstand 23.10.): Videos über 50 s verloren deutlich gegen kurze. Der Test vergleicht jetzt 30–35 s gegen 40–45 s.
- Auswertung am 01.11. in `analytics/`: Ø gesehene Sekunden, Abschlussrate, Shares und neue Follower je 1.000 Aufrufe – jeweils kurz vs. lang. Dazu: Hinweis auf den „Fahrplan ab November“ (nächste Stufe und Startdatum).

## Satelliten-Stil (Standard für alle Videos seit 25.10.2026)

**Alle Videos** (Mo–So, auch YouTube-Fassungen) werden im **Satelliten-Stil** gerendert: in slides.json immer `"renderer": "karte"` setzen (Renderer `pipeline/make_video_karte.py`, render.yml wählt ihn automatisch). Der alte Renderer (`make_video.py`) bleibt nur als Rückfallebene. Phase E im Testprotokoll.

Was der Satelliten-Stil kann (alles optional pro Folie):
- `"map": ["ISO3", …]` – Länder knallig markiert + Name in Handschrift; das erste Land ist Hauptschauplatz (Kamera fliegt hin). Ohne Land: Blick auf Deutschland/Mitteleuropa.
- `"marks"`: `{"type":"point","at":[lon,lat],"text":"Abuja"}` (Ort mit Puls), `{"type":"line","from":[lon,lat],"to":[lon,lat],"text":"29 km"}` (Entfernung), `{"type":"route","pts":[[lon,lat],…],"text":"40 %"}` (Route/Handelsweg), `{"type":"ring","at":[lon,lat]}`.
  **Nur verwenden, wenn Ort, Entfernung oder Route in den Quellen steht** (Faktencheck prüft auch Markierungen). Keine Wege andeuten, die niemand gemeldet hat (z. B. Ansteckungs- oder Angriffswege).
- `"label": {"text":"Bab al-Mandab","at":[lon,lat],"rot":-12}` – eigener Handschrift-Name (Meerengen, Regionen).
- `"cam": [lon, lat, breite_grad]` – Kamera manuell.
- `"stack"` (Preis-Zerlegung) funktioniert auch hier.
- Text kompakt halten: Titel ≤ 6 Wörter, max. 3 kurze Stichpunkte – die Karte soll wirken.

## Testprotokoll (seit 23.10.2026)

Jede Änderung an Gestaltung, Hook-Aufbau, Länge oder Ton wird in `analytics/testprotokoll.md` mit dem ersten betroffenen Video eingetragen (Phase). Auswertungen vergleichen nur innerhalb einer Phase. **Bis 01.11.2026 ist die Gestaltung der Werktagsvideos (Phase E, Satelliten-Stil) eingefroren** (nur Fehlerbehebungen).

## Prüf-Agent (unabhängiger Faktencheck, seit 20.10.2026)

Vor jedem Push prüft ein zweiter Agent mit frischem Kontext jede Aussage in `slides.json` und der Caption gegen die verlinkten Quellen: Zahlen, Daten, Namen, Zuordnungen, Veröffentlichungsdatum, 3-Quellen/2-Regionen-Regel, Angaben von Konfliktparteien, keine Vorhersagen/Wertungen.
Urteile: OK / FEHLER / UNBELEGT / ÜBERHOLT → alles außer OK wird korrigiert, gekennzeichnet oder gestrichen. Gesamturteil STOPP fürs Top-Thema = Stopp-Regel.
Ergebnis steht in `research.md` unter „Faktencheck (Prüf-Agent)“.

## Redaktionelle Endkontrolle (getrennt vom Faktencheck, seit 24.10.2026)

Der Faktencheck sagt nur, ob alles **stimmt** – nicht, ob das Video **funktioniert**. Darum nach dem Faktencheck ein eigener Prüfschritt (zweiter Agent mit frischem Kontext, sieht nur slides.json, KOMMENTAR.txt und diese Datei, nicht research.md) mit Urteil je Punkt OK / ÄNDERN:
1. **Hook:** erfüllt alle Hook-Regeln? Versteht man Folie 1 ohne Ton in 2 s?
2. **Eine Kernaussage:** Lässt sich in einem Satz sagen, worum es geht? Rote Linie von Folie 1 zur Frage am Ende?
3. **Verständlichkeit:** jeder Fachbegriff/jede Abkürzung beim ersten Auftreten in einem kurzen Satz erklärt; keine Sätze > 15 Wörter; maximal eine Zahl pro Satz.
4. **Text = Bild:** say-Text und Folientext erzählen dasselbe; Karte/Tag zeigt den richtigen Schauplatz.
5. **Länge:** Wortzahl im Rahmen des Formats.
6. **CTA/Kommentar:** Frage neutral, zwei gleichwertige Optionen; KOMMENTAR.txt fügt etwas hinzu.
ÄNDERN-Punkte werden umgesetzt, **ohne Fakten zu verändern** (Änderungen an Aussagen gehen zurück an den Faktencheck). Ergebnis in `research.md` unter „Redaktionelle Endkontrolle“.

## Lernschleife

Die tägliche Produktion liest vor jedem Video die neueste Datei in `analytics/` und `published/korrekturen.md` und setzt die Empfehlungen um (Themen, Hooks, CTA-Fragen, Aufbau). Die Regeln in dieser Datei haben immer Vorrang. Was umgesetzt wurde, steht in `research.md` unter „Angewandte Empfehlungen“.

## Länge (kalibriert)

Gemessen: 76 Wörter / 4 Folien = 40 s · 128 Wörter / 7 Folien = 54 s. Richtwerte: KURZ ca. 55–62 Wörter, LANG ca. 85–95 Wörter, SERIE ca. 95–105 Wörter. Nach dem Rendern wird die Dauer gemessen; zu lang (kurz > 38 s, lang > 47 s, Serie > 52 s) → einmal kürzen und neu rendern.

## Uhrzeit-Test (geplant 02.–08.11.2026, nach dem Längen-Test)

Bisher alle Posts 07:00–08:00 → kein Vergleich. Damit sich die Tests nicht überlagern, erst nach dem Längen-Test:
- Mo/Mi/Fr 07:30 wie bisher, Di/Do 18:30 (Entwurf liegt ab ~07:05 bereit, Denny postet abends).
- Auswertung in der Sonntagsauswertung 08.11.: Aufrufe nach 24 h und Anteil nach 3 s, morgens vs. abends.

## Fahrplan ab November 2026 (eine Änderung pro Woche)

Grund: Pro Test nur einen Faktor ändern, sonst ist nicht messbar, was wirkt. Jede Stufe gilt **erst ab ihrem Startdatum** (Europe/Berlin); vorher nicht anwenden. Die Sonntagsauswertung bewertet jeweils die Stufe der Vorwoche und schlägt vor, ob sie bleibt.

| Stufe | Start | Änderung | Messgröße |
|---|---|---|---|
| 0 | 02.11. | Uhrzeit-Test (siehe oben) | Aufrufe nach 24 h, Anteil nach 3 s |
| 0b | 02.11. | **Publikum neu beschrieben** (von Denny am 25.10. freigegeben): Hook-Regel 4 gilt ab hier mit „DACH, 25–55, Männer und Frauen etwa gleich“ statt „45+, eher männlich“ (Grund: Zuschauerprofile 21.–23.10., siehe analytics/2026-KW43-Zwischenstand.md). Bei gleichwertigen Themen das mit **Alltagsbezug** wählen: Energie/Spritpreis, Sicherheit in Europa, Jobs/Wirtschaft in Deutschland. Fachbegriffe aus Börse/Öl erklären statt voraussetzen. Regionen-Mix und Faktencheck unverändert. Stört den Uhrzeit-Test nicht (gilt morgens wie abends gleich). | Zuschauerprofil je Video (Alter, Geschlecht), Anteil nach 3 s |
| 1 | 09.11. | **Einordnungs-Satz:** Tageslage bekommt auf der Folie vor dem CTA genau einen Satz „Was das bedeutet“ **oder** „Was noch unklar ist“. Nur belegte Folgen oder ausdrücklich offene Punkte, als solche gekennzeichnet („Unklar ist bisher …“, „Laut … könnte …“). Keine eigene Prognose, keine Wertung. Zählt zur Wortgrenze (kein Längenzuschlag). | Ø Wiedergabe, Abschlussrate, Shares |
| 2 | 15.11. (So) | **Serie „BEHAUPTUNG IM CHECK“** an jedem zweiten Sonntag (15.11., 29.11., …), im Wechsel mit „SONNTAG ERKLÄRT“: eine verbreitete, konkrete Aussage zu einem geopolitischen Thema (z. B. Zahl, Zitat, Karte), aufgeteilt in **belegt / nicht belegt / offen**, jedes mit Quelle. Nur Aussagen über Sachverhalte, keine Personen bloßstellen, keine Parteien; Behauptung neutral zitieren und Herkunft nennen. `"series": "BEHAUPTUNG IM CHECK"` (bis der Renderer einen eigenen Look hat, nutzt er den Standard-Look). Faktencheck-Regel gilt für jede Einstufung. ≤ 50 s. | Follower je 1.000 Aufrufe, Shares |
| 3 | 16.11. | **Zuschauerfrage:** Gibt es seit dem letzten Video eine sachliche Verständnisfrage in den Kommentaren (Denny trägt sie in `published/fragen.md` ein), wird sie höchstens einmal pro Woche als Tageslage-Ersatz beantwortet (Einstieg: „Ihr habt gefragt: …“; Frage ohne Nutzernamen). Ohne eingetragene Frage entfällt die Stufe. | Kommentare je Video |

| 4 | 23.11. | **Ein Thema pro Tageslage:** Mo–Fr nur noch das Top-Thema, keine Nebenthemen; Markt nur als direkte Folge des Themas (z. B. Angriff auf Ölfeld → Ölpreis), kein eigener Markt-Block. Regionen-Mix-Regel 2 (zweite Region im Video) entfällt dann für Werktage; Regel 1 (max. 2 Top-Themen pro Region und Woche) bleibt. Wortgrenzen laut Ergebnis des Längen-Tests. Vorschlag aus Perplexity-Überarbeitung 25.10.; Datenbasis dort nicht nachprüfbar → erst messen. | Abschlussrate, Angesehen vs. weggewischt |

Längere Erklärvideos (> 50 s) erst wieder testen, wenn der Anteil nach 3 s stabil über 50 % liegt.

## Breaking (Zusatzvideo auf Zuruf)

- Auslöser: Denny schreibt im Projekt-Chat „Breaking: <Thema>“.
- Nur wenn bestätigt (3 Quellen, 2 Regionen) – sonst Antwort „noch nicht bestätigt“ mit Stand.
- 20–30 s, 3–4 Folien, max. 70 Wörter, ein Thema, Tag „EILMELDUNG“ (RED).
- Ordner `videos/JJJJ-MM-TT_Breaking-Thema/`, sonst gleicher Ablauf (Push → Render → Entwurf → POSTEN.txt, research.md, Log).
- Normalfall bleibt 1 Video pro Tag.

## POSTEN.txt (pro Video, fertig zum Kopieren)

Jeder Videoordner enthält `POSTEN.txt`: Caption + Quellenliste mit Herkunftsland + „KI-Stimme. Keine Anlageberatung. Impressum: mitrachdm-ui.github.io“ + Hashtags.
Denny kopiert den kompletten Inhalt 1:1 in die TikTok-Beschreibung. Max. 2.200 Zeichen.

## Kennzahlen (wöchentlich prüfen)

- **Hauptgröße: Anteil Zuschauer nach 3 s** (Ziel > 50 %; seit neuem Hook ~50 %, vorher ~25 %)
- Ø Wiedergabedauer (Ziel > 50 %) · Abschlussrate · Follower pro Video · Kommentare
- **TikTok und YouTube** werden beide ausgewertet, getrennt pro Plattform. YouTube Studio → Inhalte → Shorts: „Angesehen vs. weggewischt“ (Ziel ≥ 60 %), Ø Wiedergabe (Ziel ≥ 70 %); Zielgruppe: neue Abos je 1.000 Aufrufe. Klickrate der Impressionen bei Shorts ignorieren (Shorts-Feed zählt nicht als Impression).
- Viele Weggewischte = Hook/erste Folie schwach · niedrige Abschlussrate bei guter Ansehen-Quote = Mitte zu lang → kürzen
- Hook schlecht = Absprung in den ersten 3 Sek. → Hook-Formel wechseln
- Wöchentliche Auswertung automatisch sonntags in `analytics/JJJJ-KWnn.md`

## Checkliste vor dem Posten (Denny, in der App – gleiche Fassung im Projekt-Handbuch)

**Beide Plattformen**
- [ ] Video komplett angesehen (Ton, Zahlen, Folien)
- [ ] KOMMENTAR.txt als ersten Kommentar posten und anpinnen
- [ ] **Nie „Promote“/Werbung nutzen** – politische Werbung ist verboten
- [ ] Likes, Kommentare, Antworten nur von Hand

**TikTok** (Entwurf in der Inbox)
- [ ] POSTEN.txt komplett eingefügt (Caption + Quellen + Hashtags)
- [ ] „KI-generierte Inhalte“ eingeschaltet
- [ ] Öffentlich

**YouTube** (Short liegt privat in YouTube Studio; Titel/Beschreibung sind schon gesetzt)
- [ ] „Veränderte oder synthetische Inhalte“: im Zweifel JA (KI-Stimme)
- [ ] Zielgruppe: „Nein, nicht speziell für Kinder“
- [ ] Playlist „Tageslage“ bzw. „Erklärt“ (sobald angelegt)
- [ ] Sichtbarkeit „Öffentlich“ → Speichern
