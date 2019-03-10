import cv2
import os
import numpy as np
import os.path
import json
import matplotlib.pyplot as plt
path = r"../videos/uni/"
os.chdir(path)
img_list = os.listdir("./")
print("----total_img_nm----", len(img_list))


def cal_hj(img, j):
    # j代表灰度等级
    shpae = img.shape
    mn = shpae[0] * shpae[1]
    num_j = np.sum(img == j)
    hj = num_j/mn
    return hj


def cal_diff(fst, sec):
    diff = 0
    for intensity in range(256):
        h0 = cal_hj(fst, intensity)
        h1 = cal_hj(sec, intensity)
        diff += abs(h0 - h1)
    return diff


def twin_comparision():
    diff = []
    for i in range(len(img_list)):
        if i == len(img_list) - 1:
            break
        img = cv2.imread(img_list[i], 0)
        img2 = cv2.imread(img_list[i + 1], 0)
        diff.append(cal_diff(img, img2) * 100)  # E.4计算两张图像间的不同,*100是将diff规范化到0,100
    print(diff)
    tb = cal_tb(diff)
    write_diffto_file(diff)
    find_camera_breaks(tb)


def write_diffto_file(diff):
    os.chdir(r"C:\Users\dreamer\Desktop\twin-omparision\code")
    if not os.path.exists("./diff_value.txt"):
        f = open('diff_value.txt', 'w')
        f.close()
    f = open("diff_value.txt", 'w')
    f.write(json.dumps(diff))
    f.close()


def find_camera_breaks(tb):
    f = open("diff_value.txt", 'r')
    diff_array = np.array(json.loads(f.read()))
    index = np.where(diff_array > tb)
    print('----camera_breaks_index---', index)
    f.close()


def cal_tb(diff):
    alaph = 6
    diff_array = np.array(diff)
    mean = diff_array.mean()
    std = diff_array.std()  # 注意numpy中计算方差和标准差时分母为N而并非概率论中样本方差定义的N-1
    tb = mean + alaph * std
    return tb


if __name__ == "__main__":
    twin_comparision()
