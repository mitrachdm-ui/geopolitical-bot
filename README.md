# geopolitical-bot

Tägliche Geopolitik-Videos für TikTok **@geopolitical_8** (faceless, KI-Stimme, 9:16).

## Ablauf

1. **Claude (geplante Aufgabe)** recherchiert die Lage und legt `videos/JJJJ-MM-TT_Thema/` an mit
   `slides.json`, `sprechertext.txt`, `caption_und_quellen.txt` → Push.
2. **GitHub Actions** (`.github/workflows/render.yml`) rendert das Video mit KI-Stimme (edge-tts)
   und veröffentlicht es als Release `video-<ordner>`.
3. **Claude + Composio** lädt das Video als Entwurf in die TikTok-Inbox.
4. **Denny** prüft in der App, setzt das KI-Label und postet.

Video-URL: `https://github.com/mitrachdm-ui/geopolitical-bot/releases/download/video-<ordner>/<outfile>`

## Dateien

| Pfad | Inhalt |
|---|---|
| `pipeline/make_video.py` | Renderer (Folien → Video, Stimme pro Folie) |
| `pipeline/VORLAGE_slides.json` | Vorlage für neue Videos |
| `pipeline/Redaktion.md` | Aufbau, Regeln, Hashtags |
| `videos/` | ein Ordner pro Video |

Manuell neu rendern: Actions → „Video rendern“ → Run workflow (Ordnername optional).

Keine Anlageberatung. Alle Grafiken selbst erstellt.
