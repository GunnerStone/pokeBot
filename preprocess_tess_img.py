import numpy as np
import matplotlib.pyplot as pp
import math
import cv2
import pytesseract

def preprocess_img(img):
        "TO GET preprocess.png"
        """ THIS HAS THICCER LETTERS NEAR THE VERTICAL LINE (GOOD THING)"""
        #convert pyautogui/PIL to opencv format (numpy array)
        img = np.array(img,dtype=np.uint8) 
        savImg = img

        #make image black/white
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY ) 

        #threshold to isolate black/white color
        #_,img = cv2.threshold(img,105,255,cv2.THRESH_BINARY)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,7))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite('preprocess.png',img)

        "TO GET preprocess2.png"
        """ THIS HEAVILY THINS THE VERTICAL LINE BUT ALSO ALL LETTERS (BAD)"""
        #remove vertical
        vertical_kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(1,2))
        detected_lines = cv2.morphologyEx(img,cv2.MORPH_OPEN,vertical_kernal,iterations=2)

        cnts = cv2.findContours(detected_lines,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img,[c],-1,(255,255,255),2)

        #repair image
        repair_kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(3,1))
        results = 255 - cv2.morphologyEx(255-img,cv2.MORPH_CLOSE,repair_kernal,iterations=1)

        img = results
        

        #remove vertical
        vertical_kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(1,5))
        detected_lines = cv2.morphologyEx(img,cv2.MORPH_OPEN,vertical_kernal,iterations=2)

        cnts = cv2.findContours(detected_lines,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img,[c],-1,(255,255,255),2)

        

        

        #repair image
        repair_kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(3,1))
        results = 255 - cv2.morphologyEx(255-img,cv2.MORPH_CLOSE,repair_kernal,iterations=1)

        img = results

        cv2.imwrite('preprocess2.png',img)

        """ To get preprocess3.png""" 
        """ TRIES TO RESTORE THICKNESS IN LETTERS """

        img =  cv2.medianBlur(img,3)

        #erosion
        kernal = np.ones((1,1),np.uint8)
        img = cv2.erode(img,kernel,iterations =1)
        cv2.imwrite('preprocess3.png',img)


        

        

        

        

        # image = img
        # blur = cv2.GaussianBlur(image, (5,5), 0)
        # thresh = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY_INV)[1]

        # vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        # horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        # remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)
        # remove_vertical = cv2.morphologyEx(remove_horizontal, cv2.MORPH_OPEN, horizontal_kernel)

        # cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # mask = np.ones(image.shape, dtype=np.uint8)
        # for c in cnts:
        #     area = cv2.contourArea(c)
        #     if area > 50:
        #         cv2.drawContours(mask, [c], -1, (255,255,255), -1)

        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        # mask = cv2.dilate(mask, kernel, iterations=1)
        # image = 255 - image
        # result = 255 - cv2.bitwise_and(mask, image)

        # img = result

        # img = cv2.blur(img,(3,3))
        # _,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
        
        # img = cv2.blur(img,(3,3))
        # _,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)

        #img = cv2.blur(img,(2,2))
        #_, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    # #img = savImg
    #     dst = cv2.Canny(img, 50, 200, None, 3)
    #     img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
    #     # Copy edges to the images that will display the results in BGR
    #     cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    #     cdstP = np.copy(cdst)
        
    #     lines = cv2.HoughLines(dst, 2, np.pi / 180, 150, None, 0, 0)
        
    #     if lines is not None:
    #         for i in range(0, len(lines)):
    #             rho = lines[i][0][0]
    #             theta = lines[i][0][1]
    #             a = math.cos(theta)
    #             b = math.sin(theta)
    #             x0 = a * rho
    #             y0 = b * rho
    #             pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #             pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #             cv2.line(img, pt1, pt2, (255,255,255), 7, cv2.LINE_AA)
        
        
    #     linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
        
    #     if linesP is not None:
    #         for i in range(0, len(linesP)):
    #             l = linesP[i][0]
    #             cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

        # cv2.imwrite('blog.png',img)
        # # img =  cv2.medianBlur(img,5)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,7))
        # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # cv2.imwrite('preprocess3.png',img)

img = cv2.imread('captcha_sample.png')
preprocess_img(img)