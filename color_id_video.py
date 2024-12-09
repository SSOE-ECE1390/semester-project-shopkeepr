_import cv2
import numpy as np

# Define color ranges in HSV
color_ranges = {
    "Blue": ([98, 50, 50], [139, 255, 255]),
    "Green": ([40, 50, 50], [80, 255, 255]),
    "Red": ([0, 100, 100], [10, 255, 255]),  # Lower range for red
    "Red2": ([170, 100, 100], [180, 255, 255]),  # Upper range for red
}

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, (L_limit, U_limit) in color_ranges.items():
        # Create mask for current color
        b_mask = cv2.inRange(into_hsv, np.array(L_limit), np.array(U_limit))
        contours, _ = cv2.findContours(b_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        font = cv2.FONT_HERSHEY_SIMPLEX
        color_text = (255, 255, 255)  # White text color
        thickness = 2
        font_scale = 1

        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Filter out small contours
                continue

            # Calculate moments to find the centroid
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue  # Prevent division by zero

            # Calculate centroid coordinates
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Overlay text at the centroid, dynamically based on the color detected
            text_position = (cX - 50, cY + 10)  # Adjust to center text
            cv2.putText(frame, color_name, text_position, font, font_scale, color_text, thickness, cv2.LINE_AA)

    cv2.imshow('Detected Colors', frame)  # Display the frame with overlays

    if cv2.waitKey(1) == 27:  # Press 'Esc' to quit
        break

cap.release()
cv2.destroyAllWindows()
