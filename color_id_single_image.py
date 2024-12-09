import cv2
import numpy as np

# Load the image
image = cv2.imread('Pictures/IMG_9818.JPG')

# Resize the image for faster processing
height, width, channels = image.shape
max_width = 500
scale_factor = max_width / width
new_width = max_width
new_height = int(height * scale_factor)
resized_image = cv2.resize(image, (new_width, new_height))


# Convert the image to HSV
hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

# Calculate the histogram of the hue channel
hue_hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])

# Find the hue value with the highest frequency
dominant_hue = np.argmax(hue_hist)

# Define a color in HSV based on the dominant hueimport cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('Pictures/IMG_9818.JPG')

# Resize the image for faster processing
height, width, channels = image.shape
max_width = 800
scale_factor = max_width / width
new_width = max_width
new_height = int(height * scale_factor)
resized_image = cv2.resize(image, (new_width, new_height))

# Convert the image to HSV
hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

# Calculate the histogram of the hue channel
hue_hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])

# Plot the histogram using matplotlib to visualize hue distribution
plt.figure(figsize=(10, 6))
plt.title("Hue Histogram")
plt.xlabel("Hue Value")
plt.ylabel("Frequency")
plt.bar(range(180), hue_hist.flatten(), width=1)
plt.show()

# Define red color ranges in HSV (two ranges for red: near 0 and 180)
lower_red1 = np.array([0, 100, 100])  # Lower range of red
upper_red1 = np.array([10, 255, 255])  # Upper range of red

lower_red2 = np.array([170, 100, 100])  # Another range of red
upper_red2 = np.array([180, 255, 255])  # Another upper range for red

# Create masks to isolate red regions in the image
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

# Combine the two red masks
mask = cv2.bitwise_or(mask1, mask2)

# Find the contours of the red areas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes around red areas
for contour in contours:
    if cv2.contourArea(contour) > 1000:  # Filter small contours
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green rectangle

# Display the result
cv2.imshow('Red Color Detection', resized_image)
cv2.imshow('Red Mask', mask)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# You can adjust the saturation and value ranges based on your specific image
dominant_color_hsv = np.array([dominant_hue, 255, 255])

# Convert the dominant color from HSV to BGR for display purposes
dominant_color_bgr = cv2.cvtColor(np.uint8([[dominant_color_hsv]]), cv2.COLOR_HSV2BGR)[0][0]



# Show the images
cv2.imshow('Dominant Color Display', resized_image)
cv2.imshow('Dominant Color', np.ones((200, 200, 3), dtype=np.uint8) * dominant_color_bgr)

# Print the dominant color in RGB format
print(f"Dominant Color (BGR): {dominant_color_bgr}")

cv2.waitKey(0)
cv2.destroyAllWindows()
