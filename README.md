# PPT-to-Video Converter

This repository provides:
- A Python library for converting PowerPoint presentations (`.pptx`) into videos.
- A `main.py` file for testing the library functionality.
- A `.ipynb` file for quick testing and usage in Jupyter Notebooks.

---

## Features
- **Extract Content**: Extracts text content from PowerPoint slides.
- **Text-to-Audio Conversion**: Converts extracted text into audio files.
- **Slides-to-Images**: Converts each slide into an image.
- **Video Generation**: Combines images and audio to create a video.

---

## Prerequisites

### 1. Python Requirements
- **Python Version**: Ensure you have Python >= 3.9 installed on your system.

### 2. System Dependencies
Before using the library, the following dependencies must be installed:
- **libreoffice**
- **poppler-utils**
- **ffmpeg**

#### Installing System Dependencies
- **For Debian/Ubuntu**:
Run the following commands:
  ```bash
  sudo apt-get update
  sudo apt-get install -y libreoffice poppler-utils ffmpeg
  
---

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/ppt-to-video-converter.git
cd ppt-to-video-converter

### 2. Create a Python Virtual Environment (Recommended)
```bash
python -m venv env
source env/bin/activate   # On Linux/Mac

### 3. Install the Library
```python
pip install dist/ppt_presenter-<version>-py3-none-any.whl

## Running the application
Option 1: Run main.py
The main.py script provides a user-friendly way to test the library:

```bash
python main.py

You will be prompted to provide a .pptx file, and the script will:

1. Extract text from slides.
2. Convert text to audio.
3. Generate images from slides.
4. Create a video combining the images and audio.

Option 2: Use the Jupyter Notebook
If you prefer an interactive approach, use the provided .ipynb file
