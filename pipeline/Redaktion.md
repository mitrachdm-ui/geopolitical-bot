# Redaktion – Geopolitical_

## Aufbau jedes Videos (45–60 Sek., 6–8 Folien)

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
6. **Länge hart:** nie über 60 s (Renderer warnt). Kürzere Videos hielten besser (41 s: 23 % Ø gesehen vs. 54 s: 8 %).

**Animation (seit 20.10.):** Jede Folie wird animiert gerendert – Tag/Titel fliegen ein, Stichpunkte erscheinen nacheinander im Takt der Stimme (darum pro Folie 2–3 Stichpunkte, in der Reihenfolge des Sprechertexts), Fortschrittsbalken läuft mit, Zahlen zählen hoch. Dezente Soundeffekte (Wusch beim Folienwechsel, Klick je Stichpunkt, Puls im Hintergrund) – abschaltbar mit `"sfx": false` in slides.json.

**Weltkarte (seit 20.10.):** Hintergrund ist eine Weltkarte; die Länder des Themas leuchten rot und pulsieren, die Karte zoomt auf die Region. Länder werden automatisch aus dem Tag erkannt (z. B. „JEMEN · SAUDI-ARABIEN“, „RIAD“, „HORMUS“). Sonst in slides.json pro Folie `"map": ["SAU", "YEM"]` (ISO-3-Codes) setzen; `"map": []` = nur Weltkarte. Das zuerst genannte Land ist der Hauptschauplatz: Es bestimmt den Ausschnitt und leuchtet kräftig rot, weitere Länder schwächer bzw. nur umrandet. Darum im Tag den Schauplatz zuerst nennen („TAIWAN · CHINA“, nicht „CHINA · TAIWAN“). Bei Markt-/Ölfolien ohne Land bleibt die Weltkarte ohne Markierung.

Der Renderer setzt automatisch um: Folie 1 ohne Kopfzeile/Datum/Fußzeile, Stimme ab 0,0 s, Zahl zählt hoch, Punch-in-Zoom, Farbschein hinter der Zahl, stärkerer Zoom auf allen Folien.

## Regionen-Mix (Pflicht, seit 20.10.2026)

Publikum: DACH, 45+. Wir sind ein Weltlage-Kanal, kein Nahost-Kanal.

1. **Höchstens 2 Top-Themen pro Kalenderwoche aus derselben Region** (Regionen: Europa/Ukraine-Russland · Nahost/Golf · Asien-Pazifik · Amerika · Afrika). Ausnahme nur bei einer klar größeren Lage (z. B. neue Kriegshandlung mit direkter Wirkung auf Europa) – Begründung in research.md.
2. **Jedes Video enthält mindestens ein Thema aus einer anderen Region** als das Top-Thema (Kurzformat: in der Markt- oder Ausblick-Zeile reicht ein Satz).
3. **Bei gleichwertigen Themen gewinnt Europa/Ukraine oder ein Thema mit direkter Folge für Deutschland** (Energiepreise, Exporte, Zölle, Sicherheit).
4. **Öl ist Markt, kein Selbstläufer:** Der Ölpreis gehört auf die Markt-Folie; Top-Thema nur bei außergewöhnlicher Bewegung.
5. Vor der Themenwahl die Spalte „Region“ in `published/log.md` der letzten 7 Tage prüfen. Jede neue Log-Zeile bekommt die Region des Top-Themas.
6. Die Sonntagsauswertung zählt den Regionen-Mix und empfiehlt keine Serien, die Regel 1 brechen.

## Hook-Formeln

- **Rekord:** „Zehn Schiffe in einer Woche angegriffen. Das gab es noch nie.“
- **Zahl + Warum:** „Öl kostet 110 Dollar. Hier sind die drei Gründe.“
- **Folge für dich:** „Darum wird Tanken nächste Woche teurer.“ (nur wenn belegt)
- **Frage:** „Warum redet plötzlich jeder über Taiwan?“

## Farben auf den Folien

- Tag rot = Konflikt/Krise · amber = Rohstoffe/Termine · blau = Märkte/Politik
- `▲` grün / `▼` rot · `!▲` = steigt, ist aber negativ (VIX, Renditen, Inflation) → rot

## Rotierende Formate (Content-Plan)

| Tag | Format |
|---|---|
| Mo–Fr | **Tageslage** – Top-Thema + 2 Nebenthemen + Markt |
| Samstag | **Wochenrückblick** – die 5 Ereignisse der Woche |
| Sonntag | **Erklär-Video** – ein Hintergrund (z. B. „Was ist die Straße von Hormus?“, „Wie wirken Sanktionen?“, „Wer sind die Houthis?“) |
| Bei Eilmeldung | **Breaking** – 20–30 Sek., nur ein Thema |

Erklär-Ideen auf Vorrat: Straße von Hormus · OPEC+ · Strategische Ölreserve · Sanktionspakete der EU · Houthis · Taiwan & Chips · Seltene Erden · Rubel/Ölpreisdeckel · NATO-Artikel 5 · Fed & Ölpreis

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
- **Russland/Ukraine:** Kyiv Independent, Meduza (unabhängig, russisch); Staatsmedien (TASS, RT, Xinhua, Press TV) nur als „laut russischen/chinesischen/iranischen Staatsmedien …“
- **Fachquellen:** UKMTO, IEA, EIA, ISW, OPEC, Zentralbanken

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

Für jede Aussage im Video: Aussage · Quelle(n) mit URL · Veröffentlichungsdatum · Region · Status (bestätigt / Berichten zufolge). Am Ende: offene Unsicherheiten. Dient als Beleg, falls ein Video angezweifelt wird.

## Korrekturen

Fehler im veröffentlichten Video → sofort Korrektur-Kommentar (anpinnen) bzw. Folgevideo, nie still löschen. Eintrag in `published/korrekturen.md` (Datum, Video, Fehler, Korrektur).

## Längen-Test (19.10.–01.11.2026)

- Mo / Mi / Fr: **Kurzformat** 30–35 s – 4–5 Folien, ca. 55–62 Wörter, 1 Thema
- Di / Do: **Langformat** 50–60 s – 6–8 Folien, ca. 115–130 Wörter (hart ≤ 60 s)
- Sa (Rückblick) / So (Erklärvideo): Langformat
- Auswertung am 01.11. in `analytics/`: Ø gesehene Sekunden, Abschlussrate, Shares und neue Follower je 1.000 Aufrufe – jeweils kurz vs. lang.

## Prüf-Agent (unabhängiger Faktencheck, seit 20.10.2026)

Vor jedem Push prüft ein zweiter Agent mit frischem Kontext jede Aussage in `slides.json` und der Caption gegen die verlinkten Quellen: Zahlen, Daten, Namen, Zuordnungen, Veröffentlichungsdatum, 3-Quellen/2-Regionen-Regel, Angaben von Konfliktparteien, keine Vorhersagen/Wertungen.
Urteile: OK / FEHLER / UNBELEGT / ÜBERHOLT → alles außer OK wird korrigiert, gekennzeichnet oder gestrichen. Gesamturteil STOPP fürs Top-Thema = Stopp-Regel.
Ergebnis steht in `research.md` unter „Faktencheck (Prüf-Agent)“.

## Lernschleife

Die tägliche Produktion liest vor jedem Video die neueste Datei in `analytics/` und `published/korrekturen.md` und setzt die Empfehlungen um (Themen, Hooks, CTA-Fragen, Aufbau). Die Regeln in dieser Datei haben immer Vorrang. Was umgesetzt wurde, steht in `research.md` unter „Angewandte Empfehlungen“.

## Länge (kalibriert)

Gemessen: 76 Wörter / 4 Folien = 40 s · 128 Wörter / 7 Folien = 54 s. Richtwerte: KURZ ca. 55–62 Wörter, LANG ca. 120–135 Wörter. Nach dem Rendern wird die Dauer gemessen; zu lang (kurz > 38 s, lang > 63 s) → einmal kürzen und neu rendern.

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

- Ø Wiedergabedauer (Ziel > 50 %) · Abschlussrate · Follower pro Video · Kommentare
- Hook schlecht = Absprung in den ersten 3 Sek. → Hook-Formel wechseln
- Wöchentliche Auswertung automatisch sonntags in `analytics/JJJJ-KWnn.md`

## Checkliste vor dem Posten (Denny, in der App)

- [ ] Video komplett angesehen (Ton, Zahlen, Folien)
- [ ] POSTEN.txt komplett eingefügt (Caption + Quellen + Hashtags)
- [ ] „KI-generierte Inhalte“ eingeschaltet
- [ ] Öffentlich
- [ ] **Nie „Promote“/Werbung nutzen** – politische Werbung ist auf TikTok verboten
- [ ] Likes, Kommentare, Antworten nur von Hand
