import cv2
import os
src = r"C:\Users\dreamer\Desktop\twin-comparision\videos\777"
os.chdir(src)
img = cv2.imread('0000.jpg', 0)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
