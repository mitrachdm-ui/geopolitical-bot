# Testprotokoll – Gestaltungs- und Regelstände

Zweck: Jedes Video einer Phase zuordnen, damit Vergleiche (z. B. kurz vs. lang) nur innerhalb gleicher Gestaltung gezogen werden. Neue Änderungen hier **mit Startdatum (erstes betroffenes Video)** eintragen. Quelle: Git-Historie.

| Phase | Erstes Video | Änderungen | Videos (Werktag) |
|---|---|---|---|
| A | 18.10. | Ausgangsformat: statische Folien, Kopfzeile/Datum auf Folie 1, Stimme mit Vorlauf | 18.10. (lang), 19.10. (kurz), 20.10. (lang) |
| B | 21.10. | Neuer Hook (Folie 1 ohne Kopf/Fuß, Stimme ab 0 s, Zahl zählt hoch, Zoom), Animation (Einflug, Stichpunkte im Sprechtakt, Fortschrittsbalken), Soundeffekte inkl. Puls im Hintergrund, Weltkarte mit Ländermarkierung | 21.10. (kurz) |
| B2 | 22.10. | + CTA-Frage im Format „zwei Optionen per Emoji“ | 22.10. (lang) |
| C | 23.10. | + Globus-Übergang bei Schauplatzwechsel | 23.10. (kurz) |
| D | 24.10. | Langformat 40–45 s statt 50–60 s, Serien ≤ 50 s; angepinnter erster Kommentar (KOMMENTAR.txt); Klangteppich/Puls standardmäßig aus | ab 24.10. |

**Gestaltung eingefroren bis 01.11.2026:** In Phase D keine Änderungen an Renderer-Look, Hook-Aufbau, Animation oder Ton der Werktagsvideos (nur Fehlerbehebungen, hier mit Datum eintragen). Serien (Sa/So) zählen nicht zum Längen-Test.

**Einzeltest 24.10.2026 (Samstag, Serie):** Video im **Satelliten-Stil** (Test-Renderer `pipeline/make_video_karte.py`: NASA-Satellitenkarte, Kamerafahrten, texturierter Globus, Handschrift-Labels, kompakter Text). Gleicher Inhalt/Sprechertext wie das reguläre Video; reguläre Fassung liegt im Release als `geopolitical_2026-10-24_standard.mp4`. Nicht mit Werktagsvideos mitteln. Werktags-Renderer unverändert (Phase D).

## Auswertungsregel

- Kurz vs. lang nur **innerhalb einer Phase** vergleichen. Phase-A-Videos und spätere nie kommentarlos mitteln; wenn zusammengefasst, Phase pro Video angeben.
- Für die Längen-Entscheidung am 01.11. zählt **Phase D** (24.10.–01.11.: kurz Mo/Mi/Fr 26., 28., 30.10.; lang Di/Do 27., 29.10.). A–C nur als Vorinformation.
- Plattformvergleich TikTok vs. YouTube: YouTube-Shorts sind eigene Schnitte (anderes Format) – Unterschiede nicht allein der Plattform zuschreiben.
