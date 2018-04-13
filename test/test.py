import cv2 as cv

cvNet = cv.dnn.readNetFromTensorflow('mobile-car.pb', 'mobile-car.pbtxt')
#cvNet = cv.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

img = cv.imread('example.jpg')
rows = img.shape[0]
cols = img.shape[1]
cvNet.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (128, 128), (127.5, 127.5, 127.5), swapRB=True, crop=False))
cvOut = cvNet.forward()

for detection in cvOut[0,0,:,:]:
    score = float(detection[2])
    if score > 0.3:
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)

cv.imshow('img', img)
cv.waitKey()

# python .\tf_text_graph_ssd.py --input .\mobile-car.pb --output mobile-car.pbtxt --num_classes 4 --image_width 128 --image_height 128