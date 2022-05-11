from PIL import Image
import pytesseract
import numpy as np
import cv2

#---comparing OCR---
#Original Image

filename = 'tgl_test2.png'
img = np.array(Image.open(filename))
text1 = pytesseract.image_to_string(img, lang="tgl")

# print(pytesseract.image_to_data((img)))

#OpenCV Normalized
filename = 'tgl_test2.png'
img = np.array(Image.open(filename))

norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)

cv2.imwrite("normalized_img.png", img)

filename = 'normalized_img.png'
img = np.array(Image.open(filename))
text2 = pytesseract.image_to_string(img, lang="tgl")

#other test

# filename = 'tgl_test2.png'
# img = np.array(Image.open(filename))
# text3 = pytesseract.image_to_string(img)

# box_data = pytesseract.image_to_boxes((img))
# with open('boxes.txt', 'w') as f:
#     f.write(box_data)

#Comparison:

# print("Original:\n",text1)
# print("Edited:\n",text2)

with open('text1.txt', 'w') as f:
    f.write(text1)

with open('text2.txt', 'w') as f:
    f.write(text2)

# with open('text3.txt', 'w') as f:
#     f.write(text3)

print("done")