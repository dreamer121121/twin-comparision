import os
import json
import numpy as np
import cv2
path = "../videos/uni/"

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
    return diff*100


if __name__ == "__main__":
    os.chdir(path)
    img = cv2.imread("0227.jpg", 0)
    img2 = cv2.imread("0228.jpg", 0)
    print(img)
    print(cal_diff(img, img2))

# tb = 43.3018337509066
# f = open("diff_normalized.txt", 'r')
# diff_list = json.loads(f.read())
# diff_array = np.array(diff_list)
# print(diff_list[199])
# print("---大于tb的diff值的索引---",np.where(diff_array>tb))
# print(diff_list[227])




