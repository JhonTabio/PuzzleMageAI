"""
    Simulated camera input feed for the program

    [NOTE: This is not to be used for final product.
    This is just used for testing purposes and
    simulating input feed]

    Created by: Jhon Tabio
"""
import cv2
import numpy as np
import image_processing as ip
from PIL import ImageGrab

if __name__ == "__main__":
    while True: # Camera loop
        screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1080))  # Simulate the camera feed

        frame = np.array(screenshot) # Convert image to numpy array

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # cv2 uses BRG, convert it to RGB to display
        cv2.imshow("Screen", img) # Display camera feed to user

        masked_ret, masked_img = ip.process_image(img) # Masked data feed

        if masked_ret: # If ret is false, then no frame data
            cv2.imshow("Masked", masked_img) # Display masked data to user
        
        if cv2.waitKey(1) == ord('q'): # Check if the user prompts to quit
            break

    cv2.destroyAllWindows() # Destroy all active windows
