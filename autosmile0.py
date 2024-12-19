import argparse
import json
from input0 import load_images
from output0 import save_images
import cv2
import numpy as np
import face_recognition
from scipy.interpolate import interp1d

def main():
    parser = argparse.ArgumentParser(description='Add or enhance smiles in images.')
    parser.add_argument('--config', type=str, default='config.json', help='Path to configuration file.')
    parser.add_argument('--input', type=str, help='Input image or directory.')
    parser.add_argument('--output', type=str, help='Output directory.')
    parser.add_argument('--smile_intensity', type=float, help='Intensity of the smile effect.')
    args = parser.parse_args()

    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)

    # Override config with CLI arguments if provided
    if args.input:
        config['input_folder'] = args.input
    if args.output:
        config['output_folder'] = args.output
    if args.smile_intensity is not None:
        config['smile_intensity'] = args.smile_intensity

    # Load images and filenames
    images, filenames = load_images(config['input_folder'])
    # Process images
    processed_images = []
    for image in images:
        # Apply smile effect
        processed_image = add_smile(image, config['smile_intensity'])
        processed_images.append(processed_image)

    # Save images
    save_images(processed_images, config['output_folder'], filenames)

def add_smile(image, intensity):
    # Convert BGR to RGB for face_recognition
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect facial landmarks
    face_landmarks_list = face_recognition.face_landmarks(rgb_image)
    
    if not face_landmarks_list:
        print("No face detected in image")
        return image
    
    # Work on a copy of the image
    result_image = image.copy()
    
    for face_landmarks in face_landmarks_list:
        # Get mouth points
        top_lip = np.array(face_landmarks['top_lip'])
        bottom_lip = np.array(face_landmarks['bottom_lip'])
        
        # Get mouth corners
        left_corner = top_lip[0]
        right_corner = top_lip[6]
        
        # Calculate mouth center
        mouth_center = np.mean([top_lip.mean(axis=0), bottom_lip.mean(axis=0)], axis=0)
        
        # Apply smile transformation to bottom lip
        x_new, y_new = create_smile_curve(
            bottom_lip,
            intensity,
            mouth_center
        )

        # Update bottom lip points with new y-values
        bottom_lip_new = np.column_stack((x_new, y_new))

        # Combine updated lip points
        updated_lip_points = np.vstack((top_lip, bottom_lip_new))

        # Create convex hull for the mouth region
        mouth_landmarks_np = np.array(updated_lip_points, dtype=np.int32)
        hull = cv2.convexHull(mouth_landmarks_np)
        
        # Create mask for smooth blending
        mask = np.zeros_like(image)
        cv2.fillConvexPoly(mask, hull, (255, 255, 255))
        
        # Extract the mouth region
        rect = cv2.boundingRect(hull)
        x, y, w, h = rect
        mouth_roi = image[y:y+h, x:x+w]
        mask_roi = mask[y:y+h, x:x+w]
        
        # Warp the mouth region
        original_points = mouth_landmarks_np - [x, y]
        destination_points = mouth_landmarks_np.copy()
        destination_points[:len(top_lip), 1] -= int(15 * intensity)
        destination_points[len(top_lip):, 1] += int(15 * intensity)
        destination_points -= [x, y]
        
        # Apply affine transformation to the mouth region
        warped_mouth = warp_region(mouth_roi, original_points, destination_points, (w, h))
        
        # Blend the warped mouth back into the image
        result_image[y:y+h, x:x+w] = blend_regions(result_image[y:y+h, x:x+w], warped_mouth, mask_roi)
    
    return result_image

def create_smile_curve(points, intensity, center):
    x = points[:, 0]
    y = points[:, 1]

    # Remove duplicates and sort the arrays
    x_unique, index = np.unique(x, return_index=True)
    y_unique = y[index]
    sorted_indices = np.argsort(x_unique)
    x_sorted = x_unique[sorted_indices]
    y_sorted = y_unique[sorted_indices]

    if len(x_sorted) < 2:
        return x_sorted, y_sorted  # Not enough points to interpolate

    # Create interpolation of current curve
    curve = interp1d(x_sorted, y_sorted, kind='quadratic', fill_value='extrapolate')

    # Generate new points
    new_x = np.linspace(x_sorted.min(), x_sorted.max(), len(x_sorted))
    base_y = curve(new_x)

    # Apply smile transformation
    smile_factor = intensity * 0.1  # Adjust factor for natural effect
    dx = new_x - center[0]
    dy = -smile_factor * (dx ** 2)  # Negative to curve upwards

    return new_x, base_y + dy

def warp_region(mouth_roi, src_points, dst_points, size):
    # Compute the affine transform matrix
    src_tri = np.float32(src_points[:3])
    dst_tri = np.float32(dst_points[:3])
    warp_mat = cv2.getAffineTransform(src_tri, dst_tri)
    # Apply the affine transformation
    warped = cv2.warpAffine(mouth_roi, warp_mat, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return warped

def blend_regions(target_roi, warped_roi, mask):
    # Convert mask to grayscale and create an inverse mask
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_inv = cv2.bitwise_not(mask_gray)
    # Black-out the area of mouth in target ROI
    img_bg = cv2.bitwise_and(target_roi, target_roi, mask=mask_inv)
    # Take only region of mouth from warped ROI
    img_fg = cv2.bitwise_and(warped_roi, warped_roi, mask=mask_gray)
    # Combine the background and foreground
    combined = cv2.add(img_bg, img_fg)
    return combined

if __name__ == '__main__':
    main()
