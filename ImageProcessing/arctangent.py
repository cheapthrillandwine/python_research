'''
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
'''

import cv2
import numpy as np
#import paho.mqtt.client as mqtt
import time
import argparse
import math

def avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        #optional - average for multiple circles (can happen when a gauge is at a slight angle)
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

def dist_2_pts(x1, y1, x2, y2):
    #print np.sqrt((x2-x1)^2+(y2-y1)^2)
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calibrate_gauge(gauge_number, file_type):
    '''
        This function should be run using a test image in order to calibrate the range available to the dial as well as the
        units.  It works by first finding the center point and radius of the gauge.  Then it draws lines at hard coded intervals
        (separation) in degrees.  It then prompts the user to enter position in degrees of the lowest possible value of the gauge,
        as well as the starting value (which is probably zero in most cases but it won't assume that).  It will then ask for the
        position in degrees of the largest possible value of the gauge. Finally, it will ask for the units.  This assumes that
        the gauge is linear (as most probably are).
        It will return the min value with angle in degrees (as a tuple), the max value with angle in degrees (as a tuple),
        and the units (as a string).
    '''

    img = cv2.imread('images/gauge-%s.%s' %(gauge_number, file_type))
    img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    img = cv2.resize(img,(300,300))
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to gray
    edges = cv2.Canny(gray,100,200)
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.medianBlur(gray, 5)

    #for testing, output gray image
    #cv2.imwrite('gauge-%s-bw.%s' %(gauge_number, file_type),gray)

    #detect circles
    #restricting the search from 35-48% of the possible radii gives fairly good results across different samples.  Remember that
    #these are pixel values which correspond to the possible radii search range.

    lines = cv2.HoughLinesP(edges, rho = 1, theta = 1*np.pi/180, threshold = 100, minLineLength = 100,maxLineGap = 50)

    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height*0.35), int(height*0.48))
    #
    # # average found circles, found it to be more accurate than trying to tune HoughCircles parameters to get just the right one
    a, b, c = lines.shape
    x,y,r = avg_circles(lines, b)

    # a, b, c = circles.shape
    # x,y,r = avg_circles(circles, b)
    #

    r = r+140
    print(x, y, r)
    # #draw center and circle
    # cv2.circle(img, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA)  # draw circle
    # cv2.circle(img, (x, y), 3, (0, 255, 0), 3, cv2.LINE_AA)  # draw center of circle

    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]

        arg = math.degrees(math.atan2((y2-y1), (x2-x1)))

        print(arg)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

    #for testing, output circles on image
    #cv2.imwrite('gauge-%s-circles.%s' % (gauge_number, file_type), img)


    #for calibration, plot lines from center going out at every 10 degrees and add marker
    #for i from 0 to 36 (every 10 deg)

    '''
    goes through the motion of a circle and sets x and y values based on the set separation spacing.  Also adds text to each
    line.  These lines and text labels serve as the reference point for the user to enter
    NOTE: by default this approach sets 0/360 to be the +x axis (if the image has a cartesian grid in the middle), the addition
    (i+9) in the text offset rotates the labels by 90 degrees so 0/360 is at the bottom (-y in cartesian).  So this assumes the
    gauge is aligned in the image, but it can be adjusted by changing the value of 9 to something else.
    '''
    # separation = 10.0 #in degrees
    # interval = int(60 / separation)
    # p1 = np.zeros((interval,2))  #set empty arrays
    # p2 = np.zeros((interval,2))
    # p_text = np.zeros((interval,2))
    # for i in range(0,interval):
    #     for j in range(0,2):
    #         if (j%2==0):
    #             p1[i][j] = x + 0.9 * r * np.cos(separation * i * 3.14 / 77) #point for lines
    #         else:
    #             p1[i][j] = y + 0.9 * r * np.sin(separation * i * 3.14 / 77)
    # text_offset_x = -120
    # text_offset_y = -100
    # for i in range(0, interval):
    #     for j in range(0, 2):
    #         if (j % 2 == 0):
    #             p2[i][j] = x + r * np.cos(separation * i * 3.14 / 77)
    #             p_text[i][j] = x - text_offset_x + 0.7 * r * np.cos((separation) * (i+9) * 3.14 / 77) #point for text labels, i+9 rotates the labels by 90 degrees
    #         else:
    #             p2[i][j] = y + r * np.sin(separation * i * 3.14 / 77)
    #             p_text[i][j] = y + text_offset_y + 0.7* r * np.sin((separation) * (i+9) * 3.14 / 77)  # point for text labels, i+9 rotates the labels by 90 degrees

    # #add the lines and labels to the image
    # for i in range(0,interval):
    #     cv2.line(img, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
    #     cv2.putText(img, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,255),1,cv2.LINE_AA)

    #cv2.imwrite('gauge-%s-calibration.%s' % (gauge_number, file_type), img)
    cv2.imshow('gauge-%s-calibration.%s' % (gauge_number, file_type), img)
    #get user input on min, max, values, and units
    print('gauge number: %s' %gauge_number)
    # min_angle = input('Min angle (lowest possible angle of dial) - in degrees: ') #the lowest possible angle
    # max_angle = input('Max angle (highest possible angle) - in degrees: ') #highest possible angle
    # min_value = input('Min value: ') #usually zero
    # max_value = input('Max value: ') #maximum reading of the gauge
    # units = input('Enter units: ')

    #for testing purposes: hardcode and comment out raw_inputs above
    # ここから自動で取得したい！！
    if(gauge_number == 1):
        min_angle = 50
        max_angle = 320
        min_value = 0
        max_value = 200
    elif(gauge_number == 2):
        min_angle = 45
        max_angle = 325
        min_value = 0
        max_value = 200
    elif(gauge_number == 3):
        min_angle = 40
        max_angle = 260
        min_value = 0
        max_value = 8
    elif(gauge_number == 4):
        min_angle = 0
        max_angle = 265
        min_value = 0
        max_value = 9
    elif(gauge_number == 5):
        min_angle = 40
        max_angle = 315
        min_value = 0
        max_value = 190
    elif(gauge_number == 6):
        min_angle = 0
        max_angle = 270
        min_value = -1
        max_value = 2
    elif(gauge_number == 7):
        min_angle = 45
        max_angle = 315
        min_value = 0
        max_value = 160
    elif(gauge_number == 8):
        min_angle = 60
        max_angle = 330
        min_value = 0
        max_value = 60
    elif(gauge_number == 9):
        min_angle = 40
        max_angle = 258
        min_value = 0
        max_value = 9
    elif(gauge_number == 10):
        min_angle = 0
        max_angle = 265
        min_value = 0
        max_value = 11
    elif(gauge_number == 11):
        min_angle = 43
        max_angle = 318
        min_value = 0
        max_value = 100
    elif(gauge_number == 12):
        min_angle = 45
        max_angle = 315
        min_value = 0
        max_value = 160
    elif(gauge_number == 13):
        min_angle = 45
        max_angle = 315
        min_value = 0
        max_value = 160
    elif(gauge_number == 14):
        min_angle = 45
        max_angle = 315
        min_value = 0
        max_value = 160
    elif(gauge_number == 15):
        min_angle = 0
        max_angle = 90
        min_value = 3
        max_value = 20
    elif(gauge_number == 22):
        min_angle = 0
        max_angle = 90
        min_value = 3
        max_value = 20
    units = "PSI"

    return min_angle, max_angle, min_value, max_value, units, x, y, r

def remove_small_noise(img, fg_mask, color = (255,0,0), index=1):
    countersRemovedNoize = []
    # fg_mask, contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fg_mask, contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # fg_mask, contours, hierarchy = cv2.findContours(
    #         fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    for counter in contours:
        (x, y, w, h) = cv2.boundingRect(counter)
        # # cv2.rectangle(img, (x, y), (x + w - 1, y + h - 1),
        # #                  color, 2)
        # if index == 3:
        #     cv2.putText(img, "w:" + str(w) + " h:" + str(h), (x + 5, y+ 15), cv2.FONT_HERSHEY_SIMPLEX,
        #                     0.5, (255, 0, 255), 1)
        #print("h=",h,"---w=",w)
        if (h <= 50 or w < 50):
            print("height:",h, "-width=",w)
            countersRemovedNoize.append(counter)
    # Fill Noise
    return cv2.drawContours(fg_mask, countersRemovedNoize, -1, (0, 0, 0), -1)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, gauge_number, file_type):

    #for testing purposes
    #img = cv2.imread('gauge-%s.%s' % (gauge_number, file_type))

    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Set threshold and maxValue
    thresh = 128
    maxValue = 255
    new_value = 0
    # for testing purposes, found cv2.THRESH_BINARY_INV to perform the best
    # th, dst1 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY);
    # th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV);
    # th, dst3 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TRUNC);
    # th, dst4 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO);
    # th, dst5 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO_INV);
    # cv2.imshow('THRESH_BINARY',dst2)
    # cv2.imshow('THRESH_BINARY_INV',dst2)
    # cv2.imshow('THRESH_TRUNC',dst2)
    # cv2.imshow('THRESH_TOZERO',dst2)
    # cv2.imshow('THRESH_TOZERO_INV',dst2)

    # cv2.imwrite('gauge-%s-dst1.%s' % (gauge_number, file_type), dst1)
    # cv2.imwrite('gauge-%s-dst2.%s' % (gauge_number, file_type), dst2)
    # cv2.imwrite('gauge-%s-dst3.%s' % (gauge_number, file_type), dst3)
    # cv2.imwrite('gauge-%s-dst4.%s' % (gauge_number, file_type), dst4)
    # cv2.imwrite('gauge-%s-dst5.%s' % (gauge_number, file_type), dst5)

    # apply thresholding which helps for finding lines
    th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV);

    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))

    # # Fill any small holes
    # closing = cv2.morphologyEx(dst2, cv2.MORPH_CLOSE, kernel)
    # # Remove noise
    # opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    # # Dilate to merge adjacent blobs
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # # dst2 = cv2.erode(opening, kernel)
    # dst2 = cv2.dilate(opening, kernel)
    # dst2 = remove_small_noise(img, dst2)
    #cv2.imshow('dilation',dst2)

    # fg_mask, contours, hierarchy = cv2.findContours(dst2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # fg_mask, contours, hierarchy = cv2.findContours(
    #         fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    # for counter in contours:
    #     (x, y, w, h) = cv2.boundingRect(counter)
    #     cv2.rectangle(img, (x, y), (x + w - 1, y + h - 1),
    #                      (255,0,0), 2)

    # dst2 = remove_small_noise(img, dst2,color = (255,255,0))
    # cv2.imshow('dilation2',dst2)
    # dst2 = remove_small_noise(img, dst2,color = (255,255,255), index = 3)
    # cv2.imshow('dilation3',dst2)
    #th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY);

    # found Hough Lines generally performs better without Canny / blurring, though there were a couple exceptions where it would only work with Canny / blurring
    #dst2 = cv2.medianBlur(dst2, 1)

    # blurred = cv2.GaussianBlur(dst2, (3, 3), 0)
    # test = auto_canny(blurred,sigma=0.1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closing = cv2.morphologyEx(gray2, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    test = cv2.dilate(opening, kernel)
    #cv2.imshow('dilate',test)
    test = cv2.erode(test, None,iterations = 1)
    #cv2.imshow('erode',test)
    test = cv2.Canny(test, 50, 200,apertureSize = 3)
    #test = cv2.medianBlur(test, 3)
    #cv2.imshow('dilation',test)
    try:
        linesTest = cv2.HoughLinesP(image=test, rho=1, theta=np.pi / 360, threshold=30,minLineLength=60, maxLineGap=10)

        # if(linesTest is not None):
        #     for coords in linesTest:
        #         coords = coords[0]
        #         try:
        #             cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), (0,0,255), 3)
        #         except Exception as e:
        #             print(str(e))

        #cv2.imshow('img',img)
    except Exception as ex:
        print("error", ex)
    # dst2 = cv2.Canny(gray2, 175, 255)
    # dst2 = cv2.GaussianBlur(dst2, (5, 5), 0)

    # for testing, show image after thresholding
    #cv2.imwrite('gauge-%s-tempdst2.%s' % (gauge_number, file_type), dst2)
    #cv2.imshow('gauge-%s-tempdst2.%s' % (gauge_number, file_type),dst2)
    # find lines
    minLineLength = 40
    maxLineGap = 10
#     image – ảnh input nhị phân (ảnh có thể bị thay đổi khi tính toán)
# lines – Output là vector chứa các đường thẳng. Mỗi đường thẳng chứa 2 giá trị (ρ, θ)
# rho – Khoảng cách của các đường thẳng tính bằng pixels
# theta – Khoảng cách góc của các đường thẳng tính bằng radians
# threshold – Đường thẳng nào có số pixel lớn hơn threshold mới lấy
# srn – Dùng cho multi-scale
# stn – Cũng dùng cho multi-scale
    lines = cv2.HoughLinesP(image=test, rho=1, theta=np.pi / 360, threshold=30,minLineLength=minLineLength, maxLineGap=maxLineGap)  # rho is set to 3 to detect more lines, easier to get more then filter them out later

    # lines = cv2.HoughLines(image=dst2, rho=1, theta=np.pi / 180, threshold=180,minLineLength=minLineLength, maxLineGap=0)  # rho is set to 3 to detect more lines, easier to get more then filter them out later

    # for coords in lines:
    #     coords = coords[0]
    #     try:
    #         cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
    #     except Exception as e:
    #         print(str(e))
    # cv2.imshow('img',img)

    #for testing purposes, show all found lines
    # for i in range(0, len(lines)):
    #   for x1, y1, x2, y2 in lines[i]:
    #      cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #      cv2.imwrite('gauge-%s-lines-test.%s' %(gauge_number, file_type), img)

    # remove all lines outside a given radius
    final_line_list = []
    #print "radius: %s" %r

    diff1LowerBound = 0.15 #diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.25
    diff2LowerBound = 0.5 #diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
    diff2UpperBound = 1.0
    tmp =[]
    tmp2 =[]
    line_width = 0
    if lines is not None:
        for i in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                diff1 = dist_2_pts(x, y, x1, y1)  # x, y is center of circle
                diff2 = dist_2_pts(x, y, x2, y2)  # x, y is center of circle
                #print("diff1=", diff1, "--diff2",diff2)
                #set diff1 to be the smaller (closest to the center) of the two), makes the math easier
                if (diff1 > diff2):
                    temp = diff1
                    diff1 = diff2
                    diff2 = temp

                #cv2.line(img, (x1, y1), (x2, x2), (0,0,255), 3)

                diffLine = dist_2_pts(x1, y1, x2, y2)
                if(diffLine > line_width):
                    line_width = diffLine
                    diff1 = dist_2_pts(x, y, x1, y1)  # x, y is center of circle
                    diff2 = dist_2_pts(x, y, x2, y2)  # x, y is center of circle
                    if diff1 <= (r*1.25) and diff2 <= (r*1.25):
                        #tmp.append([x1, y1, x2, y2])
                        tmp = [x1, y1, x2, y2]

                # check if line is within an acceptable range
                if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                    line_length = dist_2_pts(x1, y1, x2, y2)
                    # add to final list
                    #final_line_list.append([x1, y1, x2, y2])
        # print("rrr=",r)
        # for i in tmp:
        #     coords = tmp[0]
        #     #print("coords=",coords)
        #     #print("coords=",coords[0])
        #     #print("coords=",coords[1])
        #     diff1 = dist_2_pts(x, y, coords[0], coords[1])  # x, y is center of circle
        #     diff2 = dist_2_pts(x, y, coords[2], coords[3])  # x, y is center of circle
        #     print("diff1=", diff1, "--diff2",diff2)
        #     if(diff1 < r and diff2 < r):
        #         tmp2 = [coords[0], coords[1], coords[2], coords[3]]

        final_line_list.append(tmp)
    #testing only, show all lines after filtering
    if(len(final_line_list) > 0):
        x1 = final_line_list[0][0]
        y1 = final_line_list[0][1]
        x2 = final_line_list[0][2]
        y2 = final_line_list[0][3]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # for i in range(0,len(final_line_list)):
        #     x1 = final_line_list[i][0]
        #     y1 = final_line_list[i][1]
        #     x2 = final_line_list[i][2]
        #     y2 = final_line_list[i][3]
        #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # assumes the first line is the best one


        #for testing purposes, show the line overlayed on the original image
        #cv2.imwrite('gauge-1-test.jpg', img)
        #cv2.imwrite('gauge-%s-lines-2.%s' % (gauge_number, file_type), img)
        #cv2.imshow('gauge-%s-lines-2.%s' % (gauge_number, file_type), img)
        #find the farthest point from the center to be what is used to determine the angle
        # cv2.circle(img, (x1, y1), 2, (255, 0, 0), 3, cv2.LINE_AA)
        # cv2.putText(img, "(" + str(x1) + "," + str(y1) + ")", (x1 + 10, y1+ 10), cv2.FONT_HERSHEY_SIMPLEX,
        #                         0.5, (255, 0, 0), 1)

        # cv2.circle(img, (x2, y2), 2, (255, 0, 255), 3, cv2.LINE_AA)
        # cv2.putText(img, "(" + str(x2) + "," + str(y2) + ")", (x2 + 10, y2+ 10), cv2.FONT_HERSHEY_SIMPLEX,
        #                         0.5, (255, 0, 255), 1)


        dist_pt_0 = dist_2_pts(x, y, x1, y1)
        dist_pt_1 = dist_2_pts(x, y, x2, y2)
        if (dist_pt_0 > dist_pt_1):
            x_angle = x1 - x
            y_angle = y - y1
        else:
            x_angle = x2 - x
            y_angle = y - y2
        # take the arc tan of y/x to find the angle
        res = np.arctan(np.divide(float(y_angle), float(x_angle)))
        #np.rad2deg(res) #coverts to degrees

        # print x_angle
        # print y_angle
        # print res
        #print("rad2deg=", np.rad2deg(res))

        #these were determined by trial and error
        res = np.rad2deg(res)
        if x_angle > 0 and y_angle > 0:  #in quadrant I
            final_angle = 270 - res
        if x_angle < 0 and y_angle > 0:  #in quadrant II
            final_angle = 90 - res
        if x_angle < 0 and y_angle < 0:  #in quadrant III
            final_angle = 90 - res
        if x_angle > 0 and y_angle < 0:  #in quadrant IV
            final_angle = 270 - res

        #print final_angle

        old_min = float(min_angle)
        old_max = float(max_angle)

        new_min = float(min_value)
        new_max = float(max_value)

        old_value = final_angle

        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min

    cv2.rectangle(img, (0, 0), (120, 20), (255, 255, 255), cv2.FILLED)

    cv2.putText(img, ("value: {total} ".format(total=round(new_value))), (5, 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    cv2.imshow('TEST', img)
    return new_value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', '--file', dest='file',
                        default="1")

    args = parser.parse_args()

    gauge_number = int(args.file)
    file_type='jpg'
    # name the calibration image of your gauge 'gauge-#.jpg', for example 'gauge-5.jpg'.  It's written this way so you can easily try multiple images
    min_angle, max_angle, min_value, max_value, units, x, y, r = calibrate_gauge(gauge_number, file_type)

    #feed an image (or frame) to get the current value, based on the calibration, by default uses same image as calibration
    img = cv2.imread('images/gauge-%s.%s' % (gauge_number, file_type))
    img = cv2.resize(img,(300,300))
    # val = get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, gauge_number, file_type)
    # print("Current reading: %s %s" %(val, units))
    cv2.waitKey(0)
if __name__=='__main__':
    main()
