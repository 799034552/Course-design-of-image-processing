#目的：建立阈值窗口调节滑动条改变canny的阈值大小，通过结果来决定阈值
#操作：按esc键退出
#参数：
#       img：读取图片名字
#日期： 2021.3.12
import cv2
import numpy as np
from numpy.core.fromnumeric import size

name = None


points = None
conts_num = None

img = None
img_shape = None

img_out = None
img_out2 = None

kernel = None

def initiate(nan):
    global name,points,conts_num,img,img_shape,img_out,img_out2,kernel
    name = nan
    points = []
    conts_num = []

    img = cv2.imread(name) 
    img_shape = (img.shape[1],img.shape[0])

    img_out = np.zeros((img.shape[0], img.shape[1], 1), dtype='uint8')
    img_out2 = np.zeros((img.shape[0], img.shape[1], 1))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))

# mouse_flag = 0
# def callback(event, x, y, flag, param):
#     global mouse_flag
#     global points
#     if(event == cv2.EVENT_LBUTTONDOWN):
#         mouse_flag = 0
#         points.append((x,y))
#         src = FindColor(name, points)
        
        
        
#     if(event == cv2.EVENT_LBUTTONUP and mouse_flag == 0):
#         mouse_flag = 1

 

# cv2.namedWindow('a')
# cv2.setMouseCallback('a', callback)

 


def FindColor(name, point, showcircle = True):
    global img_out,img_out2, points
    points.append(point)

    src = cv2.imread(name) 
    img = cv2.imread(name) 
    img_shape = (src.shape[1],src.shape[0])
    
    if showcircle:
        cv2.circle(img,points[-1], 16, (255,0,0), 2)

    for point in points:
        points.pop(0)
        
        src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        delta = 10
        color_box = src[point[1]][point[0]]
        RGB_H = np.array([color_box[0] + delta, color_box[1] + delta, color_box[2] + delta])
        RGB_L = np.array([color_box[0] - delta, color_box[1] - delta, color_box[2] - delta])
        img2 = cv2.inRange(src, RGB_L, RGB_H)
        # cv2.imshow("b",img2)
        # cv2.waitKey(1)
        # color_length = 15
        x = point[0]
        y = point[1]
        #print(img2[y][x])
        
        pos_list = []
        rubbish_list = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                x = point[0] + i
                y = point[1] + j
                pos_list.append((x, y))
        
        while pos_list != []:
            
            x = pos_list[0][0]
            y = pos_list[0][1]

            if img_out2[y][x] != 1:
                

                img_out2[y][x] = 1
                # img_color = img[y][x] 
                # length = np.linalg.norm(img_color - color_box)
                if img2[y][x] != 255:
                    pos_list.pop(0)
                    rubbish_list.append((x,y))
                else:

                    img_out[pos_list[0][1]][pos_list[0][0]][0] = 1
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            x = pos_list[0][0] + i
                            y = pos_list[0][1] + j
                            if x > img_shape[0] - 1 or x < 0 or y > img_shape[1] - 1 or y < 0:
                                continue

                            if img_out[y][x][0] == 0 and ((x,y) not in pos_list) and ((x,y) not in rubbish_list):
                                pos_list.append((x,y))
                
                    pos_list.pop(0)
            else:
                pos_list.pop(0)
    show =cv2.morphologyEx(img_out,cv2.MORPH_CLOSE,kernel)
    show = cv2.GaussianBlur(show,(3,3),0)
    contours, hierarchy = cv2.findContours(show,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img,contours,-1,(0,0,255),3) 
    return img

            


# cv2.imshow("a",img)
# cv2.waitKey(10)
# src = FindColor(name, [(150,150)])
# cv2.imshow("b",src)
# cv2.waitKey(10)

# while 1:
#     pass



#     cv2.waitKey(10)

#         # cv2.destroyAllWindows()
#         # break