"""
    Image Processing functions

    By: Jhon Tabio
"""
import cv2
import numpy as np
import numpy.typing as npt

def process_image(img: np.ndarray) -> tuple[bool, npt.NDArray[any]]: # Return function success and image
    """
        Takes in and processes image data, outlines and returns
        a simplified version of the image.

        Args:
            img: Image
        Return:
            tuple: Size 2, first index returns whether the function was sucessful
                second index returns the modified image
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert our image to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # Apply a blur to our image
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # Apply a threshold to our image
                                   cv2.THRESH_BINARY_INV, 11, 2)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, # Find all contours in our image
                                cv2.CHAIN_APPROX_SIMPLE)[0]

    if contours == None: # If no contours, we have no interest
        return False, None

    max_cnt = max(contours, key=cv2.contourArea) # Store our largest contour

    if cv2.contourArea(max_cnt) < 250 * 250: # Check if the contour is greater than 250 ** 2 pixel squared
        return False, None

    mask = np.zeros(gray.shape, np.uint8) # Generate a black mask
    cv2.drawContours(mask, [max_cnt], 0, 255, -1) # Fill within contours all white
    cv2.drawContours(mask, [max_cnt], 0, 0, 2) # The rest is filled with black

    out = 255 * np.ones_like(gray) # Generate a white mask
    out[mask == 255] = gray[mask == 255]

    return True, out
