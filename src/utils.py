import cv2
import numpy as np
import os
from datetime import datetime
import os
import shutil
from datetime import datetime
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def split_image_by_empty_space(image_path, output_folder, min_area=1000):
    """
    Splits an image into smaller segments based on empty space and saves the segments as separate image files.

    This function processes an input image to identify distinct regions of content separated by empty space.
    It extracts these regions, filters out small noise based on a minimum area threshold, and saves each
    region as a separate image file in the specified output folder.

    Args:
        image_path (str): The file path to the input image to be processed.
        output_folder (str): The directory where the cropped image segments will be saved.
        min_area (int, optional): The minimum area (in pixels) for a region to be considered valid. 
                                  Regions smaller than this threshold will be ignored. Default is 1000.

    Steps:
        1. Load the input image from the specified file path.
        2. Convert the image to grayscale for easier processing.
        3. Apply a binary threshold to distinguish content (black) from the background (white).
        4. Optionally clean up small noise using morphological operations.
        5. Detect contours (connected components) in the binary image.
        6. Sort the detected contours from top-left to bottom-right for consistent ordering.
        7. For each contour:
            - Compute its bounding rectangle.
            - Check if the area of the rectangle exceeds the `min_area` threshold.
            - If valid, extract the corresponding region from the original image.
            - Save the extracted region as a separate image file in the output folder.
        8. Print a summary of the operation, including the number of saved images.

    Raises:
        FileNotFoundError: If the input image file does not exist.
        ValueError: If the input image cannot be read or processed.

    Example:
        split_image_by_empty_space(
            image_path="/path/to/image.png",
            output_folder="/path/to/output",
            min_area=500
        )
        This will split the image into segments and save them in the specified output folder.

    Note:
        - The function assumes that the input image has a clear distinction between content and background.
        - The output folder will be created if it does not already exist.
        - The saved image files will be named in the format `cell_001.png`, `cell_002.png`, etc.
    """
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to binary: white = background, black = content
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Optional: clean up small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Find contours (connected components)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from top-left to bottom-right
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

    os.makedirs(output_folder, exist_ok=True)

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > min_area:  # Filter out noise
            sub_img = image[y:y+h, x:x+w]
            cv2.imwrite(f"{output_folder}/cell_{i+1:03d}.png", sub_img)

    print(f"✅ Done! Saved {len(contours)} cropped images to {output_folder}")


def remove_small_images(folder_path, size_threshold_ratio=0.5):
    """
    Removes images that are significantly smaller than the average size in the folder.

    Args:
        folder_path (str): Path to the folder containing images.
        size_threshold_ratio (float): Ratio of the average size below which images are removed.
    """
    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("No image files found in the folder.")
        return

    # Calculate the area of each image
    areas = []
    image_dimensions = {}
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Skipping invalid image file: {image_file}")
            continue
        height, width = image.shape[:2]
        area = width * height
        areas.append(area)
        image_dimensions[image_file] = area

    if not areas:
        print("No valid images found in the folder.")
        return

    # Calculate the average area
    average_area = sum(areas) / len(areas)
    size_threshold = average_area * size_threshold_ratio
    print(f"Average area: {average_area:.2f}")
    print(f"Size threshold (below which images will be removed): {size_threshold:.2f}")

    # Remove images smaller than the threshold
    removed_count = 0
    for image_file, area in image_dimensions.items():
        if area < size_threshold:
            image_path = os.path.join(folder_path, image_file)
            os.remove(image_path)
            removed_count += 1
            print(f"Removed small image: {image_file} (Area: {area})")

    print(f"✅ Process completed. {removed_count} images removed.")

    
def resize_images_to_fixed_size(folder, target_size=(340, 340)):
    """
    Resize all images in a specified folder to a fixed size and save them.

    This function processes all image files in the given folder, resizes them to the specified
    target size, and saves the resized images back to their original file paths. Only files with
    extensions '.png', '.jpg', and '.jpeg' are processed. Non-image files are ignored.

    Args:
        folder (str): The path to the folder containing the images to be resized.
        target_size (tuple, optional): The target size for resizing the images, specified as
            a tuple of (width, height). Defaults to (340, 340).

    Raises:
        Exception: If an error occurs while processing an image, the error is caught and
            logged, but the function continues processing other images.

    Notes:
        - The function uses the LANCZOS resampling filter for high-quality resizing.
        - Resized images overwrite the original files in the folder.
    """
    """Resize images to a fixed size (16:16 aspect ratio) with a background color."""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            with Image.open(file_path) as img:
                # Resize the image to the target size (340x340)
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

                # Save the resized image
                resized_img.save(file_path)
                print(f"Resized and saved: {file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

def resize_images_with_background_no_ar(folder, target_size=(340, 340)):
    """
    Resize images to fit within a fixed size (16:16 aspect ratio) by adding a background color.

    This function processes all image files in the given folder, resizes them to fit within the
    specified target size while maintaining their aspect ratio, and adds a background color to
    fill the remaining space. The resized images are saved back to their original file paths.

    Args:
        folder (str): The path to the folder containing the images to be resized.
        target_size (tuple, optional): The target size for resizing the images, specified as
            a tuple of (width, height). Defaults to (340, 340).

    Raises:
        Exception: If an error occurs while processing an image, the error is caught and
            logged, but the function continues processing other images.

    Notes:
        - The function uses the LANCZOS resampling filter for high-quality resizing.
        - The background color is taken from the top-left pixel of the original image.
        - Resized images overwrite the original files in the folder.
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            with Image.open(file_path) as img:
                # Calculate the new size while maintaining the aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)

                # Create a new image with the target size and background color
                background = Image.new("RGB", target_size, img.getpixel((0, 0)))
                offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
                background.paste(img, offset)

                # Save the resized image
                background.save(file_path)
                print(f"Resized and saved: {file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")


def resize_images_with_background(folder, target_width=340):
    """Resize images to the target width and extend with background color if needed."""
    for filename in os.listdir(folder):
        # Construct the full file path for the current image file
        file_path = os.path.join(folder, filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            with Image.open(file_path) as img:
                # Calculate new dimensions while maintaining aspect ratio
                aspect_ratio = img.height / img.width
                new_width = target_width
                new_height = int(new_width * aspect_ratio)

                # Resize the image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Extend the image with background color if needed
                if new_height < new_width:
                    background = Image.new("RGB", (new_width, new_width), img.getpixel((0, 0)))
                    background.paste(resized_img, (0, (new_width - new_height) // 2))
                    resized_img = background

                # Save the resized image
                resized_img.save(file_path)
                print(f"Resized and saved: {file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

def describe_and_rename_images(folder):
    """Describe images in the folder and rename them based on the description."""
    
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            # Open the image and generate a description
            with Image.open(file_path) as img:
            
                inputs = processor(images=img, return_tensors="pt")
                outputs = model.generate(**inputs)
                caption = processor.decode(outputs[0], skip_special_tokens=True)
                print(caption)

                # Create a short, sanitized name
                # short_name = "_".join(description.split()[:3]).replace(" ", "_").replace("/", "_")
                # new_filename = f"{short_name}_{serial_number}.png"
                # new_file_path = os.path.join(folder, new_filename)

                # # Save the image with the new name
                # img.save(new_file_path, format="PNG")
                # os.remove(file_path)  # Remove the old file
                serial_number += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")