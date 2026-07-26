"""
Slide-to-image conversion utilities.

Converts each slide of a .pptx file into a JPG image via a
pptx -> pdf (LibreOffice headless) -> images (pdf2image/poppler) pipeline.
"""

import logging
import os
import subprocess
from typing import List

from pdf2image import convert_from_bytes

logger = logging.getLogger(__name__)


def _convert_pptx_to_pdf(pptx_path: str, out_dir: str) -> str:
    """Uses headless LibreOffice to convert a .pptx file to .pdf inside out_dir."""
    command = [
        "soffice", "--headless", "--convert-to", "pdf",
        "--outdir", out_dir, pptx_path,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")

    filename_base = os.path.basename(pptx_path)
    filename_bare = os.path.splitext(filename_base)[0]
    pdf_path = os.path.join(out_dir, f"{filename_bare}.pdf")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Expected PDF was not produced: {pdf_path}")

    return pdf_path


def convert_ppt_to_images(
    pptx_path: str,
    out_dir: str = "slide_images",
    img_format: str = "jpg",
    dpi: int = 96,
) -> List[str]:
    """
    Converts each slide of a .pptx file into a JPG image.

    Args:
        pptx_path: Path to the source .pptx file.
        out_dir: Directory to save slide images into.
        img_format: Image file extension/format.
        dpi: Rendering resolution.

    Returns:
        List of paths to the generated slide images, in slide order.
    """
    os.makedirs(out_dir, exist_ok=True)

    logger.info("Converting %s to PDF via LibreOffice", pptx_path)
    pdf_path = _convert_pptx_to_pdf(pptx_path, out_dir)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    logger.info("Rendering PDF pages to images at %d DPI", dpi)
    images = convert_from_bytes(pdf_bytes, dpi=dpi)

    image_paths: List[str] = []
    for i, img in enumerate(images, start=1):
        img_path = os.path.join(out_dir, f"slide_{i}.{img_format}")
        img.save(img_path)
        image_paths.append(img_path)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        logger.info("Removed intermediate PDF: %s", pdf_path)

    logger.info("Saved %d slide image(s) to %s", len(image_paths), out_dir)
    return image_paths
