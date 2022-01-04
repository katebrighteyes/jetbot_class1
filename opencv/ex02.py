from OpenCV_Functions import *

def imageProcessing(image):
    result = imageCopy(image)
    result = convertColor(result, cv2.COLOR_BGR2HLS)
    h, l, s = splitImage(result)
    for i in range(0, 200):
        for j in range(0,200):
            l2 = setPixel(l,i,j,200)
    result = mergeImage(h,l2, s)
    result = convertColor(result, cv2.COLOR_HLS2BGR)
    return result

imagePath = "./solidWhiteCurve.jpg"
image = imageRead(imagePath)
imageShow("Opened Image", image)
result = imageProcessing(image)
imageShow("Result", result)
cv2.destroyAllWindows()
