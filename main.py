import os
from ppt_presenter import content_extractor, text_to_audio, ppt_to_images, video_creator

def main():
    print("Welcome to the PPT to Video Converter")

    # Get the PPTX file path from the user
    ppt_file = input("Please enter the path to your PowerPoint file (.pptx): ").strip()

    if not os.path.exists(ppt_file):
        print("Error: File not found. Please check the path and try again.")
        return

    try:
        # Step 1: Extract content from PPT
        print("Extracting content from the PPT...")
        slide_contents = content_extractor.extract_ppt_content(ppt_file)
        print("Content extracted successfully.")

        # Step 2: Convert text content to audio
        print("Converting slide content to audio...")
        audio_folder = "slide_audios"
        os.makedirs(audio_folder, exist_ok=True)
        audio_files = text_to_audio.get_audio(slide_contents, output_folder=audio_folder)
        print("Audio files created successfully.")

        # Step 3: Convert slides to images
        print("Converting slides to images...")
        images_folder = "slide_images"
        os.makedirs(images_folder, exist_ok=True)
        ppt_to_images.convert_ppt_to_images(ppt_file)
        print("Slide images generated successfully.")

        # Step 4: Create video from images and audio
        print("Creating video from images and audio...")
        output_video = "output_video.mp4"
        video_creator.create_video_from_images_and_audio(images_folder, audio_folder, output_video)
        print(f"Video created successfully! Output file: {output_video}")

    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
