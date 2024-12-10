import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pytesseract as ts
import easyocr

# flags / control settings
# externalCamera = False

# if externalCamera:
#     cv.VideoCapture(1)
# else: 
#     cv.VideoCapture(0)

# Tesseract OCR Path
ts.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Init CV Window
winName = "Edge Detection"

cv.namedWindow(winName)
cv.resizeWindow(winName, 100, 100)

imgsrc = "Pictures/IMG_9810.JPG"

img = cv.imread(imgsrc)
img = cv.resize(img, (0,0), fx=0.3, fy=0.3) # downsize image


# main edge detection function
def edgeDetection(image: cv.typing.MatLike) -> cv.typing.MatLike:
    # newImg = cv.Sobel(image, ddepth=cv.CV_32F, dx=1, dy=1, ksize=5)

    # image = cv.resize(image, (300,300))

    image = easyocrDetection(image)
    # return watershedding(image)
    # return HoughLinesCircles(image)
    masks = cannyContourRemoval(image)

    for mask in masks:
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        watershedding(np.bitwise_and(image, mask))
    # return kmeansDetection(image)
    return watershedding(image)

    # return removeTextBG(image)

    # return image

    # cv.rectangle()

    src_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    newImg = cv.GaussianBlur(src_img, (7,7), 25, None, 15)

    # newImg = cv.Laplacian(newImg, cv.CV_32F, ksize=7)

    newImg = cv.Canny(newImg, 50, 80, 3)

    # for i in range(3):
    #     newImg = cv.GaussianBlur(newImg, (7,7), 15)
        # newImg = cv.Canny(newImg, 30, 30, 3)

    return watershedding(newImg)
    

    # corners = cv.goodFeaturesToTrack(src_img, 100, .5, 15)


    return HoughLinesCircles(newImg)
    # for i in corners:
    #     x, y = int(i[0][0]), int(i[0][1])
        
    #     cv.circle(newImgColor, (x,y), 3, 255, 1)


    # newImg = cv.cornerHarris(newImg, 5, 7, .1)


    # newImgColor = cv.dilate(newImgColor, None)

    # image[newImgColor > 0.01 * max(newImgColor)] = [0, 0, 255]
    

    

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = np.cos(theta)
    #         b = np.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #         cv.line(newImgColor, pt1, pt2, (0,0,255), 3, cv.LINE_AA)

    

    return newImgColor
    # return newImg

# Uses Canny Edge Detection, Tries to get the biggest, most external
# contours from the edge detection and outputs these filled contours as masks
def cannyContourRemoval(image: cv.typing.MatLike) -> cv.typing.MatLike:

    # TODO: separate into its own functions

    # ensure gray and regular image are used no matter the function input
    if isinstance(image[0][0], np.ndarray) :
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray, image = image, cv.cvtColor(image, cv.COLOR_GRAY2BGR)

    newImg = cv.GaussianBlur(gray, (7,7), 50, None, 50)
    newImg = cv.Canny(newImg, 50, 90, 5)

    # potentially dilate the lines
    cannyKernel = np.ones((3, 3), np.uint8)
    newImg = cv.dilate(newImg, cannyKernel, iterations=6)

    # newImg = cv.GaussianBlur(newImg, (7,7), 50, None, 50)


    # testing the output
    cv.imshow(winName, newImg)
    key = cv.waitKey()
    
    # Contour filtering
    contours, hierarchy = cv.findContours(newImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print(len(contours))

    outer_contours = []

    for i, contour in enumerate(contours):
        if hierarchy[0][i][3] == -1 and cv.contourArea(contour) > 10000:
            print(cv.contourArea(contour))
            outer_contours.append(contour)

    print(len(outer_contours))

    item_masks = []

    # outputting as a set of masks
    for contour in outer_contours:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv.drawContours(mask, contour, -1, 255, -1)
        cv.drawContours(image, contour, -1, (0, 0, 255), 10)
        item_masks.append(mask)

    # output image with all masks on it
    cv.imshow(winName, image)
    key = cv.waitKey()

    return item_masks

# Watershedding Tutorial from G4Gs tailored to the dataset (attempted)
# Separate into BackGnd & ForeGnd and partition accordingly
def watershedding(image: cv.typing.MatLike) -> cv.typing.MatLike:
    
    # print(type(image[0][0]))

    if isinstance(image[0][0], np.ndarray) :
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray, image = image, cv.cvtColor(image, cv.COLOR_GRAY2BGR)

    # separate into main lines and thicken them
    cannyKernel = np.ones((3, 3), np.uint8)
    newImg = cv.GaussianBlur(gray, (7,7), 50, None, 30)
    newImg = cv.Canny(newImg, 50, 90, 3)
    newImg = cv.dilate(newImg, cannyKernel, iterations=2)

    cv.imshow(winName, newImg)
    key = cv.waitKey()


    gray = cv.GaussianBlur(gray, (7,7), 30, None, 25)
    _, thresh_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)


    thresh_img = np.bitwise_and(thresh_img, np.bitwise_not(newImg))

    cv.imshow(winName, thresh_img)
    key = cv.waitKey()

    # create bg & fg
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    thresh_img = cv.morphologyEx(thresh_img, cv.MORPH_OPEN, kernel, iterations=6)

    cv.imshow(winName, thresh_img)
    key = cv.waitKey()

    sure_bg = cv.dilate(thresh_img, kernel, iterations=3)

    cv.imshow(winName, sure_bg)
    key = cv.waitKey()

    dist = cv.distanceTransform(thresh_img, cv.DIST_L2, 5)
    cv.imshow(winName, dist)
    key = cv.waitKey()

    _, sure_fg = cv.threshold(dist, 20, 255, cv.THRESH_BINARY)
    sure_fg = sure_fg.astype(np.uint8)
    cv.imshow(winName, sure_fg)
    key = cv.waitKey()

    unknown = cv.subtract(sure_bg, sure_fg)
    cv.imshow(winName, unknown)
    key = cv.waitKey()


    _, markers = cv.connectedComponents(sure_fg)

    markers += 1

    markers[unknown == 255] = 0

    markers = cv.watershed(image, markers)

    objects = []
    labels = np.unique(markers)

    # unique contours
    for label in labels[2:]:
        target = np.where(markers == label, 255, 0).astype(np.uint8)

        contours, hierarchy = cv.findContours(target, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        objects.append(contours[0])

    print(len(objects))
    image = cv.drawContours(image, objects, -1, (0, 0, 255), thickness=2)

    return image

# try to separate image into objects to be able to count them
# (does not work correctly)
def kmeansDetection(image: cv.typing.MatLike) -> cv.typing.MatLike:
    
    # preprocessing
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pixel_vals = image.reshape((-1, 3))
    pixel_vals = np.float32(pixel_vals)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, .85)
    k = 21

    # K Means w/ Random Center for Generalizability
    _, labels, centers = cv.kmeans(pixel_vals, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    # Segment image off centers
    centers = np.uint8(centers)
    segment_data = centers[labels.flatten()]
    seg_image = segment_data.reshape((image.shape))

    return cv.cvtColor(seg_image, cv.COLOR_RGB2BGR)

# Find Hough Lines & Circles to try and identify boxes & cans
def HoughLinesCircles(image: cv.typing.MatLike) -> cv.typing.MatLike:
    
    if isinstance(image[0][0], np.ndarray) :
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray, image = image, cv.cvtColor(image, cv.COLOR_GRAY2BGR)

    # Find Lines & Circles and Plot them on the image
    newImg = cv.GaussianBlur(gray, (7,7), 50, None, 30)
    imageGray = cv.Canny(newImg, 50, 90, 3)
    lines = cv.HoughLinesP(imageGray, 1, np.pi / 180, 150, None, 50, 10)
    circles = cv.HoughCircles(imageGray, cv.HOUGH_GRADIENT, 1, 500, None, 50, 30, 20, 200)


    if lines is not None:
        for points in lines:
        # Extracted points nested in the list
            x1,y1,x2,y2=points[0]
            # Draw the lines joing the points
            # On the original image
            cv.line(image,(x1,y1),(x2,y2),(255,255,0),2)
            # Maintain a simples lookup list for points
            # lines_list.append([(x1,y1),(x2,y2)])

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(image,(i[0],i[1]),2,(0,0,255),3)

    return image

# OCR to find text to be able to block it out
# Tesseract does not work well anytime I use it which is frustrating
def tesseractDetection(image: cv.typing.MatLike) -> cv.typing.MatLike:
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    
    ocrdict = ts.image_to_data(image, output_type=ts.Output.DICT)
    n_boxes = len(ocrdict['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (ocrdict['left'][i], ocrdict['top'][i], ocrdict['width'][i], ocrdict['height'][i])
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return image

# Find Closed Shapes and Count Them to get a face count
# Due to Canny ED, most boxes are never closed which messes this method up
def count_closed_shapes(image: cv.typing.MatLike) -> int:

    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    count = 0

    for contour in contours:
        if cv.isContourConvex(contour):
            count += 1

    return count

# OCR to find text
# Dynamic Blocking Textbox - average color @ the pts 
def easyocrDetection(image: cv.typing.MatLike) -> cv.typing.MatLike:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)

    for box, _, _ in result:
        coord1 = tuple(map(int, box[0]))
        coord2 = tuple(map(int, box[2])) #I made these and did not use them

        # This function finds the text to block the color
        color = tuple([np.average([image[int(box[0][1])][int(box[0][0])][i], image[int(box[2][1])][int(box[2][0])][i]])  for i in range(len(image[0][0]))])

        cv.rectangle(image, coord1, coord2, color, cv.FILLED)
    # print(result)
    return image

# Trying to remove text in the Background
def removeTextBG(image: cv.typing.MatLike) -> cv.typing.MatLike:
    
    # find the kernels to process the image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    close_kernel = cv.getStructuringElement(cv.MORPH_RECT, (15,3))
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, close_kernel, iterations=1)

    dilate_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,3))
    dilate = cv.dilate(close, dilate_kernel, iterations=1)

    # find contours & if they're within a certain size, then block them
    cnts = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area > 800 and area < 15000:
            x,y,w,h = cv.boundingRect(c)
            cv.rectangle(image, (x, y), (x + w, y + h), (222,228,251), -1)

    return image

# TODO: put in a if name is main line
cv.imshow(winName, edgeDetection(img))
# plt.figure()
# plt.imshow(edgeDetection(img))
# print(count_closed_shapes(img))

key = cv.waitKey()