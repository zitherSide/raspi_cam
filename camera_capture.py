import cv2
from picamera2 import Picamera2

camera = Picamera2()
camera.start()
img = camera.capture_array()
cv2.imwrite('test.jpg', img)
