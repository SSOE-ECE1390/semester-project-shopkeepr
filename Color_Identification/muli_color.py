import cv2
import numpy as np

# Defining the upper and lower limits of the colors we want to look for
color_ranges = {
    "Blue": ([98, 50, 50], [139, 255, 255]),
    "Red": ([0, 100, 100], [10, 255, 255]),
    "Red2": ([170, 100, 100], [180, 255, 255]),
    "Brown": ([10, 80, 30], [25, 255, 180]),
}

# Starting video capture
cap = cv2.VideoCapture(0)

while True:

    # Capturing the current frame
    ret, frame = cap.read()
    if not ret:
        break

    # Turning it into HSV format
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Looping through each color's upper and lower limits
    for name, (lower_limit, upper_limit) in color_ranges.items():

        # Creating the colors bitmask and contours
        color_mask = cv2.inRange(hsv_image, np.array(lower_limit), np.array(upper_limit))
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Defining font parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        color_text = (255, 255, 255)


        # used to determine centre of the object
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue

            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            text_position = (cX - 50, cY + 10)
            cv2.putText(frame, name, text_position, font, 1, color_text, 2)

    # Displaying the manipulated fram
    cv2.imshow("Detected",frame)

    # Checking to see if esc key was pressed
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
