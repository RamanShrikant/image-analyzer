# data_cleaner.py
# Placeholder for dataset preprocessing or cleanup routines.

import os
import cv2
import numpy as np

def resize_images(directory, size=(224, 224)):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(root, file)
                img = cv2.imread(path)
                if img is not None:
                    img = cv2.resize(img, size)
                    cv2.imwrite(path, img)

def normalize_array(arr: np.ndarray) -> np.ndarray:
    return arr / 255.0
