import os
import cv2

def save_images(images, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for idx, image in enumerate(images):
        if image is not None:
            filename = f'smiled_image_{idx}.jpg'
            cv2.imwrite(os.path.join(output_path, filename), image)
        else:
            print(f"Skipping empty image at index {idx}")
