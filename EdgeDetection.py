import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# flags / control settings
# externalCamera = False

# if externalCamera:
#     cv.VideoCapture(1)
# else: 
#     cv.VideoCapture(0)

winName = "Edge Detection"

cv.namedWindow(winName)
cv.resizeWindow(winName, 100, 100)

imgsrc = "Pictures/IMG_9814.JPG"

img = cv.imread(imgsrc)

img = cv.resize(img, (0,0), fx=0.3, fy=0.3)


def edgeDetection(image: cv.typing.MatLike) -> cv.typing.MatLike:
    # newImg = cv.Sobel(image, ddepth=cv.CV_32F, dx=1, dy=1, ksize=5)

    src_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    newImg = cv.GaussianBlur(src_img, (101,101), 0)

    newImg = cv.Laplacian(src_img, cv.CV_32F, ksize=5)

    
    
    # newImg[0] = cv.medianBlur(newImg[0], 5)
    # newImg[1] = cv.medianBlur(newImg[1], 5)
    # newImg[2] = cv.medianBlur(newImg[2], 5)

    # newImg[0] = cv.convertScaleAbs(newImg[0])
    # newImg[1] = cv.convertScaleAbs(newImg[1])
    # newImg[2] = cv.convertScaleAbs(newImg[2])

    


    return newImg


cv.imshow(winName, edgeDetection(img))

key = cv.waitKey()