import os
import cv2

def load_images(input_path):
    images = []
    filenames = []
    if os.path.isdir(input_path):
        for filename in sorted(os.listdir(input_path)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image = cv2.imread(os.path.join(input_path, filename))
                if image is not None:
                    images.append(image)
                    filenames.append(filename)
    elif os.path.isfile(input_path):
        image = cv2.imread(input_path)
        if image is not None:
            images.append(image)
            filenames.append(os.path.basename(input_path))
    else:
        raise FileNotFoundError(f"No such file or directory: '{input_path}'")
    return images, filenames
