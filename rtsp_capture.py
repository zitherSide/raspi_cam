import cv2

cap = cv2.VideoCapture("url")
io = cap.isOpened()
ret, frame = cap.read()

cv2.imwrite('test.jpg', frame)

cv2.destroyAllWindows()
