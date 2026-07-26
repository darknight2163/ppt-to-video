"""
Video assembly utilities.

Combines per-slide images and per-slide narration audio into a single MP4.

Note: the original notebook wrote each image as a single OpenCV video frame
(1 frame at 8fps ~= 0.125s) and then muxed it with the full-length narration
audio using `-shortest`, which silently cut the audio down to ~0.125s per
slide. Here each image is instead held on screen via ffmpeg for the exact
duration of its matching audio file, so narration is never truncated.
"""

import logging
import os
import re
import subprocess
import tempfile
from typing import List

from pydub import AudioSegment

logger = logging.getLogger(__name__)


def _natural_key(filename: str):
    """Sort key that orders slide_2.jpg before slide_10.jpg (natural/numeric order)."""
    digits = re.findall(r"\d+", filename)
    return int(digits[-1]) if digits else filename


def _get_audio_duration_seconds(audio_path: str) -> float:
    audio = AudioSegment.from_mp3(audio_path)
    return len(audio) / 1000.0


def _build_segment(image_path: str, audio_path: str, segment_path: str, fps: int) -> None:
    """Creates one video segment: a still image held for the length of its audio."""
    duration = _get_audio_duration_seconds(audio_path)
    command = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-r", str(fps),
        "-shortest",
        segment_path,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg segment creation failed for {image_path}: {result.stderr}")


def create_video_from_images_and_audio(
    image_folder: str,
    audio_folder: str,
    output_video_file: str,
    fps: int = 8,
) -> str:
    """
    Combines per-slide images and per-slide narration audio into a single MP4.

    Each image is held on screen for the exact duration of its matching audio
    file, then all segments are concatenated in slide order.

    Args:
        image_folder: Folder containing slide_N.jpg images.
        audio_folder: Folder containing slide_N.mp3 audio files.
        output_video_file: Path to write the final MP4 to.
        fps: Frame rate for the generated segments.

    Returns:
        Path to the final video file.
    """
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
        key=_natural_key,
    )
    audio_files = sorted(
        [f for f in os.listdir(audio_folder) if f.lower().endswith(".mp3")],
        key=_natural_key,
    )

    if len(image_files) != len(audio_files):
        raise ValueError(
            f"Mismatch between number of images ({len(image_files)}) and "
            f"audio files ({len(audio_files)}); they must be equal and paired 1:1."
        )
    if not image_files:
        raise ValueError("No images/audio files found to build a video from.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        segment_paths = []
        concat_list_path = os.path.join(tmp_dir, "concat_list.txt")

        for i, (image_file, audio_file) in enumerate(zip(image_files, audio_files)):
            image_path = os.path.join(image_folder, image_file)
            audio_path = os.path.join(audio_folder, audio_file)
            segment_path = os.path.join(tmp_dir, f"segment_{i}.mp4")

            logger.info(
                "Building segment %d/%d: %s + %s",
                i + 1, len(image_files), image_file, audio_file,
            )
            _build_segment(image_path, audio_path, segment_path, fps=fps)
            segment_paths.append(segment_path)

        with open(concat_list_path, "w") as f:
            for segment_path in segment_paths:
                f.write(f"file '{segment_path}'\n")

        out_dir = os.path.dirname(os.path.abspath(output_video_file))
        os.makedirs(out_dir, exist_ok=True)

        concat_command = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list_path,
            "-c", "copy",
            output_video_file,
        ]
        result = subprocess.run(concat_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg concatenation failed: {result.stderr}")

    logger.info("Video created successfully: %s", output_video_file)
    return output_video_file
