import asyncio
import json
from pathlib import Path

import edge_tts


ROOT = Path(__file__).resolve().parent
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-5%"


async def main():
    chapters = json.loads((ROOT / "narration.json").read_text(encoding="utf-8"))
    audio_dir = ROOT / "audio"
    audio_dir.mkdir(exist_ok=True)
    for index, chapter in enumerate(chapters, start=1):
        output = audio_dir / ("chapter_%02d.mp3" % index)
        communicate = edge_tts.Communicate(chapter["text"], VOICE, rate=RATE)
        await communicate.save(str(output))
        print("Created %s" % output.name)


if __name__ == "__main__":
    asyncio.run(main())
