import cv2
import numpy as np

# Defining lower and upper bounds of the color blue
blue_lower = np.array([98, 50, 50])
blue_upper = np.array([139, 255, 255])

# Starting video Capture
cap = cv2.VideoCapture(0)

while True:
    # Reading in the current frame
    ret, frame = cap.read()
    if not ret:
        break

    #changing formate to hsv
    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # creating the binary mask that only includes the volor blue
    blue_mask = cv2.inRange(into_hsv, blue_lower, blue_upper)

    # Defining the contours of the bitmask
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    # Defining text parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    color_text = (255, 255, 255)

    # used to determine centre of the object
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue

        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        text_position = (cX - 50, cY + 10)
        cv2.putText(frame, "Blue", text_position, font, 1, color_text, 2)

    # Displaying the manipulated fram
    cv2.imshow('Detected Blue Color', frame)

    # Checks to see if the escape key was pressed
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
