# YouTube-Shorts-Variante – Geopolitical_ (seit 22.10.2026)

Gilt **nur für YouTube**. TikTok bleibt unverändert (`Redaktion.md`).
Grundlage: erstes Short (21.10., NATO Schwarzes Meer): 695 Aufrufe in 9 h, 98 % aus dem Shorts-Feed,
aber **51,6 % weggewischt**, Ø Wiedergabe 0:17 von 0:31, 0 Abonnenten, 0 Kommentare.

## Ablauf

1. Die tägliche YouTube-Aufgabe nimmt den Tagesordner `videos/JJJJ-MM-TT_Thema/` (fertig recherchiert, faktengeprüft).
2. Sie legt `videos/JJJJ-MM-TT_Thema/youtube/` an mit
   - `slides.json` (YouTube-Fassung, `outfile`: `geopolitical_JJJJ-MM-TT_youtube.mp4`)
   - `TITEL.txt` (eine Zeile, max. 100 Zeichen, endet mit ` #Shorts`)
   - `POSTEN.txt` (Beschreibung)
3. Push → GitHub Actions rendert sie als Release `video-<ORDNER>-youtube`.
4. Upload privat über Composio (`YOUTUBE_MULTIPART_UPLOAD_VIDEO` zuerst – `YOUTUBE_UPLOAD_VIDEO` lieferte am 21.10. eine kaputte Datei).
5. Denny schaltet in YouTube Studio auf „Öffentlich“ und setzt dabei, was der Upload nicht setzen kann: „Veränderte oder synthetische Inhalte“ (im Zweifel JA), Zielgruppe „Nicht speziell für Kinder“, Playlist (siehe Checkliste in `Redaktion.md`).
6. Scheitert der Upload (z. B. 429 = Tageskontingent leer), bekommt Denny Video-Link, Titel und Beschreibung zum manuellen Hochladen.

## Regeln für die YouTube-Fassung

**Nur Fakten aus dem Tagesordner verwenden** (slides.json, research.md). Keine neue Recherche, keine neuen Zahlen. Kürzen und umstellen ja, neue Aussagen nein.

1. **Ein Thema, 25–35 s.** Nur das Top-Thema plus die passende Markt-Folie. Nebenthemen aus anderen Regionen entfallen
   (Ausnahme von Regionen-Mix-Regel 2, die nur für TikTok gilt). Ziel: 60–70 Wörter, 4–5 Folien (gemessen 22.10.: 80 Wörter = 40 s inkl. Übergänge).
2. **Hook (Folie 1):** große Zahl + Titel max. 6 Wörter + **Ort im ersten Satz**. Erster Satz max. 10 Wörter, beginnt mit der Zahl.
   Kein „Laut …“ am Anfang (die Quelle steht auf Folie 2). Tag mit Land setzen, damit die Karte im ersten Bild leuchtet.
3. **Offene Schleife im Hook:** ein kurzer zweiter Satz, der auf das Ende verweist („Und Öl reagiert.“, „Und die USA reagieren.“).
   Die Auflösung kommt auf der vorletzten Folie. Nur ankündigen, was im Video belegt ist.
4. **Pro Folie max. 3 Sätze, je max. 15 Wörter.** Nebendetails (Nationalitäten, Namen von Sprechern) streichen.
5. **CTA (letzte Folie, ~5 s):** „Abonniere Geopolitical, jeden Morgen die Weltlage.“ + die Frage aus der Tagesfassung
   (zwei neutrale Optionen, auf der Folie in Worten, keine Emojis auf Folien).
6. **Titel (TITEL.txt):** Kernaussage mit Zahl und Ort, sachlich, kein Clickbait, max. 1 Emoji, endet mit ` #Shorts`.
   Bei Serien vorne „Untergegangen: “ bzw. „Sonntag erklärt: “. Ohne „Laut …“ am Anfang.
7. **Beschreibung (POSTEN.txt):** Caption der Tagesfassung ohne Sätze zu entfallenen Nebenthemen, danach die Frage mit Emojis,
   eine Abo-Zeile („Jeden Morgen die Weltlage in 30 Sekunden – abonnieren.“), Quellen (nur die zu den gezeigten Aussagen,
   mit Herkunftsland), „KI-Stimme. Keine Anlageberatung. Impressum: mitrachdm-ui.github.io“, Hashtags, `#Shorts`.
8. Serien (Samstag/Sonntag): `series` übernehmen; Länge bis 45 s erlaubt.

9. **Titel-Regeln gehen hier vor:** Für YouTube gelten Regel 6 und diese Datei (`#Shorts` am Titelende, Serien-Präfix „Untergegangen: “/„Sonntag erklärt: “, kein „Laut …“ am Anfang). Andere Vorschläge (z. B. Perplexity 25.10.: `#Shorts` nur in die Beschreibung, Quelle in den Titel) erst nach Messung umstellen.
10. **Korrekturen** gelten auch hier: Fehler im TikTok-Video desselben Tages → Korrektur-Kommentar auch unter dem Short (siehe `Redaktion.md`).

11. **Erster Kommentar:** Denny postet nach dem Freischalten den Text aus `KOMMENTAR.txt` des Tagesordners und pinnt ihn an (⋮ → Anpinnen). Die Meldung der YouTube-Aufgabe nennt ihn mit.

## Messen

Nach 48 h in YouTube Studio prüfen: **„Angesehen vs. weggewischt“** (Ziel ≥ 60 % angesehen), Ø Wiedergabedauer (Ziel ≥ 70 %),
Abonnenten pro Video. Ergebnis in `analytics/` notieren.
