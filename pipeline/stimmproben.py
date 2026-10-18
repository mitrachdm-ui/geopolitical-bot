"""Erzeugt Hörproben verschiedener deutscher KI-Stimmen (edge-tts) als MP3."""
import asyncio, os, sys, edge_tts
TEXT = ("Zehn Schiffe in einer Woche angegriffen. Rekord seit Beginn des Iran-Kriegs. "
        "Brent schloss am Freitag bei fast hundertzehn Dollar, so hoch wie seit Mai nicht.")
VOICES = ["de-DE-ConradNeural", "de-DE-KillianNeural", "de-DE-FlorianMultilingualNeural",
          "de-DE-KatjaNeural", "de-DE-AmalaNeural", "de-DE-SeraphinaMultilingualNeural",
          "de-AT-JonasNeural", "de-CH-JanNeural"]
async def main(out):
    os.makedirs(out, exist_ok=True)
    for i, v in enumerate(VOICES, 1):
        try:
            await edge_tts.Communicate(TEXT, v, rate="+12%").save(os.path.join(out, f"{i:02d}_{v}.mp3"))
            print("ok", v)
        except Exception as e:
            print("fehlt", v, e)
asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "stimmproben"))
