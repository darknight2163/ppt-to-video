"""
Text-to-speech utilities: converts extracted slide text into per-slide audio.

Note: the original notebook skipped generating audio for empty slides, which
silently desynced the image/audio counts and broke the video step. Here every
slide always gets an audio file (a short placeholder for empty slides) so the
slide <-> audio pairing stays 1:1.
"""

import logging
import os
from typing import List

from gtts import gTTS
from tqdm import tqdm

logger = logging.getLogger(__name__)

# A short, near-silent placeholder used for slides with no text content, so
# every slide still gets a matching audio file.
SILENT_PLACEHOLDER_TEXT = "."


def get_audio(
    slide_contents: List[str],
    output_folder: str = "slide_audios",
    lang: str = "en",
) -> List[str]:
    """
    Converts a list of per-slide text content into per-slide MP3 audio files.

    Args:
        slide_contents: List where each element is the text content of one slide.
        output_folder: Folder to save the generated audio files into.
        lang: gTTS language code.

    Returns:
        List of paths to the generated audio files, in slide order. Always the
        same length as slide_contents.
    """
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Generating audio for %d slide(s)", len(slide_contents))

    audio_paths: List[str] = []

    for i, content in enumerate(
        tqdm(slide_contents, desc="Processing slides", unit="slide"), start=1
    ):
        audio_file = os.path.join(output_folder, f"slide_{i}.mp3")
        text = content.strip() if content and content.strip() else SILENT_PLACEHOLDER_TEXT

        if text == SILENT_PLACEHOLDER_TEXT:
            logger.warning("Slide %d has no text content; using placeholder audio.", i)

        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)
        audio_paths.append(audio_file)

    logger.info("Audio files saved in: %s", output_folder)
    return audio_paths
