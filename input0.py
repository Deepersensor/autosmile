import os
import cv2

def load_images(input_path):
    images = []
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image = cv2.imread(os.path.join(input_path, filename))
                images.append(image)
    elif os.path.isfile(input_path):
        image = cv2.imread(input_path)
        images.append(image)
    else:
        raise FileNotFoundError(f"No such file or directory: '{input_path}'")
    return images
