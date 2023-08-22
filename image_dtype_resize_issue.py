import cv2
import numpy as np

# below image default reads to BGR
img = cv2.imread("/home/devil/dataset/heart.png") 

# we will print the image dimensions
print("image dimensions: ", img.shape)
#print(range(216))

def print_img_values(img):
    rows,cols,ch = img.shape
    rows = rows -1
    cols = cols -1
    for r in range(rows):
        for c in range(cols):
            print(img[r,c])
        print("\n")
    print("\n\n")
# we will print the image data

print_img_values(img)
# now we will resize the image to half the dimensions

res_img = cv2.resize(img, (int(img.shape[0]/2), int(img.shape[1]/2)), interpolation =cv2.INTER_AREA)
print_img_values(res_img)

# after converting to float and then resize
flt_img_arr = img.astype('float')
res_flt_img = cv2.resize(flt_img_arr, (int(flt_img_arr.shape[0]/2), int(flt_img_arr.shape[1]/2)), interpolation =cv2.INTER_AREA)
print_img_values(res_flt_img)
