import os
import cv2

def save_images(images, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for idx, image in enumerate(images):
        filename = f'smiled_image_{idx}.jpg'
        cv2.imwrite(os.path.join(output_path, filename), image)
