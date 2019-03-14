import cv2
import os
import numpy as np
import os.path
import json
import matplotlib.pyplot as plt


def cal_hj(img, j):
    # j代表灰度等级
    """
    计算图像中灰度级为j的直方图值。
    :param img:
    :param j:
    :return:
    """
    shape = img.shape
    mn = shape[0] * shape[1]
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


def write_to_file(content,filename):
    os.chdir(r"C:\Users\dreamer\Desktop\twin-omparision\code")
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.close()
    f = open(filename, 'w')
    f.write(json.dumps(content))
    f.close()

def find_camera_breaks(tb):
    """
    此函数用于寻找camera breaks所对应的图片的索引
    :param tb:
    :return:
    """
    f = open("diff_value.txt", 'r')
    diff_array = np.array(json.loads(f.read()))
    f.close()
    index = list(np.where(diff_array > tb))
    write_to_file(index[0].tolist(),"cam_breaks.txt")




def cal_tb(diff):
    """
    此函数用于计算Tb的值
    :param diff:
    :return:
    """
    params = {}
    alaph = 6
    diff_array = np.array(diff)
    mean = diff_array.mean()  # numpy计算均值。
    std = diff_array.std()  # 注意numpy中计算方差和标准差时分母为N而并非概率论中样本方差定义的N-1
    tb = mean + alaph * std
    params["alaph"] = alaph
    params["mean"] = mean
    params["Tb"] = tb
    write_to_file(params,"params.txt")
    return tb

def second_scan():
    """
    第二次扫描视频发现gradual transition
    :return:
    """
    imglist = os.listdir(path)
    Ts = 17
    Tb = 48.60732894720321

    os.chdir(path)
    potential_start_point = -1
    flag = 0  # 潜在gradual transition 起始点标志位
    accumulated = 0  # 累积误差清零
    for i in range(130, 160):
        img = cv2.imread(imglist[i], 0)  # 一定注意要用灰度值读入
        img2 = cv2.imread(imglist[i + 1], 0)
        consecutive_diff = cal_diff(img, img2)  # 计算相邻两帧的diff值规范化到100以内。

        if consecutive_diff >= Ts:
            if flag == 0:  # 没有考察的gradual transition 起始点，则新建一个点
                accumulated = 0
                flag = 1  # 标志位置1
                potential_start_point = i  # 潜在的过渡起始帧
                start_img = cv2.imread(imglist[potential_start_point], 0)


            elif flag == 1:  # 有正在考察的起始点，故继续累加累积误差
                current_img = img
                accumulated += cal_diff(start_img, current_img)  # 计算累积不同度

        else:  # 此时相邻两帧的不同度降低到了Ts以下
            if flag == 0:  # 此时没有正在评估的gradual_transition的起始点
                continue
            if flag == 1:
                if accumulated < Tb:
                    accumulated = 0  # 累积差异值清零。
                    flag = 0
                else:
                    write_to_file([potential_start_point,i],"gradual_transistion.txt")
                    os.chdir(path)
                    accumulated = 0  # 累积差异值清零。
                    flag = 0


def first_sacn():
    """
    第一次扫描
    :param img_lsit:
    :return:
    """
    diff = []
    for i in range(len(img_list)):
        if i == len(img_list) - 1:
            break
        img = cv2.imread(img_list[i], 0)
        img2 = cv2.imread(img_list[i + 1], 0)
        diff.append(cal_diff(img, img2))  # E.4计算两张图像间的不同,*100是将diff规范化到0,100
    tb = cal_tb(diff)
    write_to_file(diff,"diff_value.txt")
    find_camera_breaks(tb)


def twin_comparision(img_list):
    #第一次扫描
    first_sacn()
    print("----第一次扫描结束----")
    #第二次扫描
    second_scan()
    print("----第二次扫描结束----")


def read_img():
    img_list = os.listdir("./")
    print("----total_img_nm----", len(img_list))
    return img_list


if __name__ == "__main__":
    path = r"../videos/uni/"
    os.chdir(path)
    img_list = read_img()
    twin_comparision(img_list)
