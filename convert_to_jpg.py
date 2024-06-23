from PIL import Image
import os
from pathlib import Path

import os

def delete_png_files(input_folder):
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a PNG image
        if filename.endswith(".png"):
            # Construct full file path
            file_path = os.path.join(input_folder, filename)
            # Attempt to remove the file
            try:
                os.remove(file_path)
                print(f"Deleted {filename}")
            except OSError as e:
                print(f"Error deleting {filename}: {e}")

if __name__ == "__main__":
    input_folder = "images"
    delete_png_files(input_folder)