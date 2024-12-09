# Based off of:
# https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e

import cv2
import numpy as np
import matplotlib.pyplot as plt



img = 'Pictures/IMG_9819.JPG'
clusters = 1

img = cv2.imread(img)


img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img = img.reshape((img.shape[0] * img.shape[1], 3))

img_float = np.float32(img)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
_, labels, centers = cv2.kmeans(img_float, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

color = np.uint8(centers)

print("Dominant Color:")
print(color)


lower_blue = np.array([0, 0, 80])
upper_blue = np.array([100, 100, 255])

lower_red = np.array([100, 0, 0])  
upper_red = np.array([255, 100, 100])

lower_brown = np.array([40, 20, 0])
upper_brown = np.array([139, 100, 50])


if np.all(color >= lower_blue) and np.all(color <= upper_blue):
    print("Dominant color: Blue")
elif np.all(color >= lower_red) and np.all(color <= upper_red):
    print("Dominant color: Red")
elif np.all(color >= lower_brown) and np.all(color <= upper_brown):
    print("Dominant color: Brown")
else:
    print("Dominant Color: Not Defined")


plt.imshow([color])
plt.axis('off')
plt.show()