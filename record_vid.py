import cv2
import time

cap = cv2.VideoCapture("url")

io = cap.isOpened()
if not io:
    print('Could not open')
    exit()

fourcc = cv2.VideoWriter_fourcc(*'H264')
ost = cv2.VideoWriter("vid.mp4", fourcc, 30, (640, 480))

end = time.time() + 5
now = time.time()
while now < end:
    ret, frame = cap.read()
    ost.write(frame)
    now = time.time()

ost.release()
cap.release()