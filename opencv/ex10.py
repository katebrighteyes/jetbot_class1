def splitLines(lines):
    left_x = []
    left_y = []
    right_x = []
    right_y = []
    for line in lines:
        x1 = line[0,0]
        y1 = line[0,1]
        x2 = line[0,2]
        y2 = line[0,3]
        slope = (float)(y2-y1)/(float)(x2-x1)
        if abs(slope) < 0.5:
            continue
        if slope <= 0:
            left_x.append([x1, x2])
            left_y.append([y1, y2])
        else:
            right_x.append([x1, x2])
            right_y.append([y1, y2])
    return left_x, left_y, right_x, right_y


def meanPoint(x):
    sum1 = 0
    sum2 = 0
    for x1, x2 in x:
        sum1 += x1
        sum2 += x2
    sum1 = int(float(sum1)/float(len(x)))
    sum2 = int(float(sum2)/float(len(x)))
    return [sum1, sum2]

def medianPoint(x):
    xx = sorted(x)
    return xx[(int)(len(xx)/2)]
    

def interpolate(list_x, list_y, y):
    x1 = list_x[0]
    x2 = list_x[1]
    y1 = list_y[0]
    y2 = list_y[1]
    return int(float(y - y1) * float(x2-x1) / float(y2-y1) + x1)

    
def lineFitting(image, left_x, left_y, right_x, right_y):
    result = imageCopy(image)
    height = image.shape[0]
    lx = meanPoint(left_x)
    ly = meanPoint(left_y)
    rx = meanPoint(right_x)
    ry = meanPoint(right_y)
    min_y = int(height*0.6)
    max_y = height
    min_x_left = interpolate(lx, ly, min_y)
    max_x_left = interpolate(lx, ly, max_y)
    min_x_right = interpolate(rx, ry, min_y)
    max_x_right = interpolate(rx, ry, max_y)
    cv2.line(result, (min_x_left, min_y), (max_x_left, max_y), (0, 0, 255), 3)
    cv2.line(result, (min_x_right, min_y), (max_x_right, max_y), (0, 0, 255), 3)
    return result

def imageProcessing(image):
    result = imageCopy(image)
    image_gray = convertColor(image, cv2.COLOR_BGR2GRAY)
    #image_edge = cannyEdge(image_gray, 100, 200)
    height, width = image.shape[:2]
    pt1 = (width*0.45, height*0.65)
    pt2 = (width*0.55, height*0.65)
    pt3 = (width, height*1.0)
    pt4 = (0, height*1.0)
    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    result = polyROI(result, roi_corners)

    result = cannyEdge(result, 100, 200)
    lines = houghLinesP(result, 1, np.pi/180, 10, 10)
    lx, ly, rx, ry = splitLines(lines)
    result = lineFitting(image, lx, ly, rx, ry)

    #result = lineFitting(image, lines, (0, 0, 255), 5, 5. * np.pi / 180.)
    '''
    height, width = result.shape[:2]
    result = convertColor(result, cv2.COLOR_BGR2GRAY)
    result = cannyEdge(result, 100, 200)
    
    pt1 = [int(width*0.45), int(height*0.65)]
    pt2 = [int(width*0.55), int(height*0.55)]
    pt3 = [width, height]
    pt4 = [0, height]
    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    result = polyROI(result, roi_corners)
    lines = houghLinesP(result, 1, np.pi/180, 100, 10, 50)
    #result = drawHoughLinesP(image, lines)
    result = lineFitting(image, lines, (0,0,255), 5, 5.*np.pi/180.)
    '''
    return result
