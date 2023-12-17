import threading
import time
import datetime
import cv2

class serveillance:
    def __init__(self):
        self.imgMutex = threading.Lock()
        self.img = None

        self.streamUrl = "url"
        self.fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.fps = 30
        self.size = (640, 480)

        print(f'{datetime.datetime.now()}')
        self.cap = cv2.VideoCapture(self.streamUrl)

    def capture_thread(self):
        while True:
            self.imgMutex.acquire()
            ret, self.img = self.cap.read()
            self.imgMutex.release()

    def detect_thread(self):
        lastFrame = None
        endTime = time.time()
        while True:
            time.sleep(0.5)
            self.imgMutex.acquire()
            frame = self.img
            self.imgMutex.release()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if lastFrame is None:
                lastFrame = gray.astype("float")
            
            try:
                cv2.accumulateWeighted(gray, lastFrame, 0.7)
            except Exception as e:
                print(e)
                lastFrame = gray.astype("float")

            diff = cv2.absdiff(gray.astype("float"), lastFrame)
            thresh = cv2.threshold(diff.astype("uint8"), 4, 255, cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detected = False
            for c in contours:
                if cv2.contourArea(c) > 600:
                    detected = True
                    print(f'ContureArea: ${cv2.contourArea(c)}')
                    break
            
            if detected:
                endTime = time.time() + 10
            
                stillPath = f'./img/{datetime.datetime.now()}.jpg'
                vidPath = f'./vid/{datetime.datetime.now()}.mp4'
                
                self.imgMutex.acquire()
                cv2.imwrite(stillPath, self.img)
                ost = cv2.VideoWriter(vidPath, self.fourcc, self.fps, self.size)
                while time.time() < endTime:
                    ost.write(self.img)
                    ret, self.img = self.cap.read()

                self.imgMutex.release()
                
                ost.release()
                lastFrame = gray.astype("float")
            else:
                try:
                    cv2.accumulateWeighted(gray, lastFrame, 0.7)
                except Exception as e:
                    print(e)
                    lastFrame = gray.astype("float")

    def run(self):
        t1 = threading.Thread(target=self.capture_thread)
        t2 = threading.Thread(target=self.detect_thread)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

s = serveillance()
s.run()