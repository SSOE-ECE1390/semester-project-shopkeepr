import cv2
import numpy as np

blue_lower = np.array([98, 50, 50])
blue_upper = np.array([139, 255, 255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(into_hsv, blue_lower, blue_upper)
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    cv2.imshow('Detected Blue Color', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
