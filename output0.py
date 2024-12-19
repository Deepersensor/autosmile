import os
import cv2

def save_images(images, output_path, filenames):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for idx, (image, filename) in enumerate(zip(images, filenames)):
        if image is not None:
            output_filename = f'smiled_{filename}'
            cv2.imwrite(os.path.join(output_path, output_filename), image)
        else:
            print(f"Skipping empty image at index {idx}")
