import os
import json
import numpy as np
import cv2
# path = "../videos/uni/"
#
# def cal_hj(img, j):
#     # j代表灰度等级
#     shpae = img.shape
#     mn = shpae[0] * shpae[1]
#     num_j = np.sum(img == j)
#     hj = num_j/mn
#     return hj
#
#
# def cal_diff(fst, sec):
#     diff = 0
#     for intensity in range(256):
#         h0 = cal_hj(fst, intensity)
#         h1 = cal_hj(sec, intensity)
#         diff += abs(h0 - h1)
#     return diff*100
#

# if __name__ == "__main__":
#     os.chdir(path)
#     img = cv2.imread("0227.jpg", 0)
#     img2 = cv2.imread("0228.jpg", 0)
#     print(img)
#     print(cal_diff(img, img2))

# tb = 43.3018337509066
# f = open("diff_normalized.txt", 'r')
# diff_list = json.loads(f.read())
# diff_array = np.array(diff_list)
# print(diff_list[199])
# print("---大于tb的diff值的索引---",np.where(diff_array>tb))
# print(diff_list[227])

# f = open("diff_value.txt", 'r')
# data = json.loads(f.read())
# print(type(data))
# print(data.index(12.389520202020215))
# f = open("transition.txt", "w")
# f.write(json.dumps(data[130:160]))
# f.close()





#-----------------------------------------------------------------
"""第二次扫描，检测gradual transition"""
def cal_hj(img, j):
    # j代表灰度等级
    """
    计算图像中灰度级为j的直方图值。
    :param img:
    :param j:
    :return:
    """
    shpae = img.shape
    mn = shpae[0] * shpae[1]
    num_j = np.sum(img == j)
    hj = num_j / mn
    return hj


def cal_diff(fst, sec):
    """
    此函数用于计算相邻两帧图像间的差异
    使用文中方程4所定义的SDi，并最终规范到0-100之间。
    :param fst:
    :param sec:
    :return:
    """
    diff = 0
    for intensity in range(256):
        h0 = cal_hj(fst, intensity)
        h1 = cal_hj(sec, intensity)
        diff += abs(h0 - h1)
    return diff*100


# 计算accumulated difference
imglist = os.listdir(path)
Ts = 17
Tb = 48.60732894720321

potential_start_point = -1
flag = 0 #潜在gradual transition 起始点标志位
accumulated = 0 #累积误差清零
for i in range(130, 160):
    img = cv2.imread(imglist[i], 0)  # 一定注意要用灰度值读入
    img2 = cv2.imread(imglist[i + 1], 0)
    consecutive_diff = cal_diff(img, img2)  # 计算相邻两帧的diff值规范化到100以内。
    print(str(i)+"----consecutive_diff----", consecutive_diff)

    if consecutive_diff >= Ts:
        if flag == 0: #没有考察的gradual transition 起始点，则新建一个点
            accumulated = 0
            flag = 1 #标志位置1
            potential_start_point = i  # 潜在的过渡起始帧
            print("潜在起始点：", potential_start_point)
            start_img = cv2.imread(imglist[potential_start_point], 0)


        elif flag == 1: #有正在考察的起始点，故继续累加累积误差
            current_img = img
            accumulated += cal_diff(start_img, current_img)  # 计算累积不同度
            print("起始点"+str(potential_start_point)+"的累计值"+str(accumulated))

    else:  # 此时相邻两帧的不同度降低到了Ts以下
        if flag == 0:  # 此时没有正在评估的gradual_transition的起始点
            continue
        if flag == 1:
            if accumulated < Tb:
                print("误差累计值："+str(accumulated)+"<Tb")
                accumulated = 0  # 累积差异值清零。
                print("丢弃当前潜在过渡点" + str(potential_start_point))
                flag = 0
            else:
                print("----找到了gradual_transition---")
                print((potential_start_point, i))
                accumulated = 0  # 累积差异值清零。
                flag = 0


