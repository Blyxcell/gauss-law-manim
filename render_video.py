import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pydub import AudioSegment


ROOT = Path(__file__).resolve().parent
VIDEO_NAME = "Gauss_Law_1080p.mp4"
VIDEO_PATH = ROOT / VIDEO_NAME
MANIM_VIDEO = ROOT / "media" / "videos" / "gauss_law" / "1080p30" / VIDEO_NAME
AUDIO_DIR = ROOT / "audio"


def build_narration():
    chapters = sorted(AUDIO_DIR.glob("chapter_*.mp3"))
    expected = ["chapter_%02d.mp3" % index for index in range(1, 13)]
    actual = [path.name for path in chapters]
    if actual != expected:
        raise FileNotFoundError(
            "Expected all 12 narration tracks in %s; found %s" % (AUDIO_DIR, actual)
        )
    narration = AudioSegment.empty()
    for chapter in chapters:
        narration += AudioSegment.from_file(chapter)
    if len(narration) < 10 * 60 * 1000:
        raise ValueError("Narration must be at least 10 minutes; got %.1f seconds." % (len(narration) / 1000))
    return narration


def render():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "manim",
            "-r",
            "1920,1080",
            "--fps",
            "30",
            "-o",
            VIDEO_NAME,
            "gauss_law.py",
            "GaussLaw",
        ],
        cwd=str(ROOT),
        check=True,
    )
    if not MANIM_VIDEO.is_file():
        raise FileNotFoundError("Manim output not found: %s" % MANIM_VIDEO)
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise FileNotFoundError("FFmpeg was not found on PATH.")
    narration = build_narration()
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = Path(temp_dir) / "narration.wav"
        narration.export(str(audio_path), format="wav")
        file_descriptor, temp_video_name = tempfile.mkstemp(suffix=".mp4", dir=str(ROOT))
        os.close(file_descriptor)
        temp_video = Path(temp_video_name)
        try:
            subprocess.run(
                [
                    ffmpeg,
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-y",
                    "-i",
                    str(MANIM_VIDEO),
                    "-i",
                    str(audio_path),
                    "-map",
                    "0:v:0",
                    "-map",
                    "1:a:0",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-ar",
                    "48000",
                    "-movflags",
                    "+faststart",
                    str(temp_video),
                ],
                check=True,
            )
            temp_video.replace(VIDEO_PATH)
        finally:
            if temp_video.exists():
                temp_video.unlink()
    print("Created %s (%.1f minutes with continuous narration)" % (VIDEO_PATH, len(narration) / 60000))


if __name__ == "__main__":
    render()
