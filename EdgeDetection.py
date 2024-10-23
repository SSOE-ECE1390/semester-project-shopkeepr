import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# flags / control settings
# externalCamera = False

# if externalCamera:
#     cv.VideoCapture(1)
# else: 
#     cv.VideoCapture(0)

imgsrc = "placeholder"

cv.imread()


def edgeDetection(image: MatLike) -> MatLike:
    return cv.Sobel(image, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)