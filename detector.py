import cv2
import time

cap = cv2.VideoCapture("url")
lastFrame = None

while cap.isOpened():
    try:
        ret, frame = cap.read()
        if not ret:
            print("Could not read frame.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if lastFrame is None:
            # lastFrame = gray
            lastFrame = gray.astype("float")
            continue

        # cv2.imwrite("f.jpg", gray)
        # cv2.imwrite("l.jpg", lastFrame)

        cv2.accumulateWeighted(gray, lastFrame, 0.4)
        frame_diff = cv2.absdiff(gray.astype("float"), lastFrame)
        # frame_diff = cv2.absdiff(gray, cv2.convertScaleAbs(lastFrame))
        cv2.imwrite("diff.jpg", frame_diff)
        # cv2.imshow('diff.jpg', frame)
        thresh = cv2.threshold(frame_diff.astype("uint8"), 4, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)

        print(f'contour: ${cv2.contourArea(sortedContours[0])}')
        if cv2.contourArea(sortedContours[0]) > 100:
            cv2.imwrite("detected.jpg", frame)
        else:
            cv2.imwrite("detected.jpg", frame)

    except Exception as e:
        # lastFrame = gray
        print(f'Error: ${e}')

    time.sleep(1)

