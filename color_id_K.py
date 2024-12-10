# Based off of:
# https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e

import cv2
import numpy as np
import matplotlib.pyplot as plt


# Defining image path
img = 'Pictures/IMG_9819.JPG'

# Reading in image
img = cv2.imread(img)

# Turning the image into RGB to be able touse Kmean functions
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#Reshaping the image to use the RGB pixel values
img = img.reshape((img.shape[0] * img.shape[1], 3))
img_float = np.float32(img)

#Defining parameters for Kmean function 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
clusters = 1

_, _, centers = cv2.kmeans(img_float, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Turning the center to its RGB values to be able to display and compare them
color = np.uint8(centers)

print("Dominant Color:")
print(color)

#Defining the color boundries
lower_blue = np.array([0, 0, 80])
upper_blue = np.array([100, 100, 255])

lower_red = np.array([100, 0, 0])  
upper_red = np.array([255, 100, 100])

lower_brown = np.array([40, 20, 0])
upper_brown = np.array([139, 100, 50])

#Checking if the dominant color of the image is in these boundries
if np.all(color >= lower_blue) and np.all(color <= upper_blue):
    print("Dominant color: Blue")
elif np.all(color >= lower_red) and np.all(color <= upper_red):
    print("Dominant color: Red")
elif np.all(color >= lower_brown) and np.all(color <= upper_brown):
    print("Dominant color: Brown")
else:
    print("Dominant Color: Not Defined")

#displaying the dominant color
plt.imshow([color])
plt.axis('off')
plt.show()
