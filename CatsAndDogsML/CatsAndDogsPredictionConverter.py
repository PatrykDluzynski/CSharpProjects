import numpy as np
import os
import cv2

def convert_data(image):
    try:
        LENGTH = 70
        image_array = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        new_image_array = cv2.resize(image_array, (LENGTH, LENGTH))
        data = np.array(new_image_array).reshape(-1, LENGTH, LENGTH, 1)
        return data
    except Exception:
        pass