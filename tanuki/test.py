import cv2
filename = 'sample_image.png'

read_image = cv2.imread(filename,1)
print(read_image)