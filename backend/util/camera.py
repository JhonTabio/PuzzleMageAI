"""
    Camera input feed for the program

    [NOTE: This is not to be used for final product.
    This is just used for testing purposes and
    simulating input feed]

    Created by: Jhon Tabio
"""
import cv2
import numpy as np
import image_processing as ip

if __name__ == "__main__":
    camera = cv2.VideoCapture(2) # Capture the first available camera

    if not camera.isOpened(): # Determine if we are able to retrieve data from camera
        print("There was an error loading the camera.")
        exit()

    while True: # Camera loop
        ret, frame = camera.read() # Read in information from the camera
        
        if not ret: # If ret is false, then no frame data
            print("There was an error loading the frame.")
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # cv2 uses BRG, convert it to RGB to display
        cv2.imshow("Camera", img) # Display camera feed to user

        masked_ret, masked_img = ip.process_image(img) # Masked data feed

        if masked_ret: # If ret is false, then no frame data
            cv2.imshow("Masked", masked_img) # Display masked data to user
        
        if cv2.waitKey(1) == ord('q'): # Check if the user prompts to quit
            break

    camera.release() # Release camera(s)
    cv2.destroyAllWindows() # Destroy all active windows
