#目的：建立阈值窗口调节滑动条改变canny的阈值大小，通过结果来决定阈值
#操作：按esc键退出
#参数：
#       img：读取图片名字
#日期： 2021.3.12
import cv2
import numpy as np
from numpy.core.fromnumeric import size

name = '1.jpg'

def FindEdge(name):

    lowThreshold1 = 60
    ratio = 3
    kernel_size = 3

    # points = []
    # conts_num = []

    # cv2.namedWindow('canny demo')
    # cv2.namedWindow('a')

    img = cv2.imread(name) 
    img2 = cv2.imread(name) 

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    detected_edges = cv2.GaussianBlur(gray,(7,7),0)

    for i in range(100):
        lowThreshold1 = i
        canny_img = cv2.Canny(detected_edges,
                                    lowThreshold1,
                                    lowThreshold1*ratio,
                                    apertureSize = kernel_size)
        contours, hierarchy = cv2.findContours(canny_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        if len(contours) < 5:
            break
    # print(i)
    detected_edges = canny_img

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    detected_edges =cv2.morphologyEx(detected_edges,cv2.MORPH_CLOSE,kernel)

    #cv2.imshow('canny demo',detected_edges)
    contours, hierarchy = cv2.findContours(detected_edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img2,contours,-1,(0,0,255),3) 

    return img2
    # cv2.imshow('a',img2)   
    # cv2.waitKey(10)  

# while 1:
#     pass
# cv2.waitKey(0)    
# # print((len(contours)))
# # for i in range(len(contours)):
# #     if cv2.contourArea(contours[i]) > 15:
# #         cv2.drawContours(img2,contours,i,(0,0,255),3) 
# #         cv2.waitKey(1000)
# #         cv2.imshow('a',img2)
# #cv2.drawContours(img2,contours,-1,(0,0,255),3) 
# while 1:
#     contours = np.array(contours)
#     print(contours[0].shape)
#     if len(points) != 0:
#         for point in points:

#             for i in range(len(contours)):
                
#                 print('true')
#                 conts_num.append(i)
                    

#     for i in conts_num:
#         cv2.drawContours(img2,contours,i,(0,0,255),3) 
#         #cv2.imshow('a',img2)
#     # cv2.pointPolygonTest 
#     # cv2.drawContours(img,contours,-1,(0,0,255),3) 
#     cv2.imshow('canny demo',detected_edges)
#     cv2.imshow('a',img2)
#     cv2.waitKey(10)

        # cv2.destroyAllWindows()
        # break