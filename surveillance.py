import threading
import time
import datetime
import cv2
import video_context as vc

def getFilenames():
    stem = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    stillPath = f'./rec/{stem}.jpg'
    vidPath = f'./rec/{stem}.mp4'
    return (stillPath, vidPath)

def copyLockValue(lock, value):
    lock.acquire()
    ret = value
    lock.release()
    return ret

class surveillance:
    streamUrl = "url"
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    fps = 30
    size = (640, 480)
    extendInterval = 3 # seconds
    
    def __init__(self):
        self.imgMutex = threading.Lock()
        self.img = None
        self.endTimeMutex = threading.Lock()
        self.endTime = time.time()

        print(f'program started: {datetime.datetime.now()}')

    def capture_thread(self):
        cap = cv2.VideoCapture(self.streamUrl)

        while True:
            self.imgMutex.acquire()
            ret, self.img = cap.read()
            self.imgMutex.release()
            time.sleep(0)

            et = copyLockValue(self.endTimeMutex, self.endTime)

            if time.time() < et:
                _, vidPath = getFilenames()
                with vc.VideoContext(vidPath, self.fourcc, self.fps, self.size) as ost:
                    while time.time() < et:
                        self.imgMutex.acquire()
                        ost.write(self.img)
                        ret, self.img = cap.read()
                        self.imgMutex.release()

                        et = copyLockValue(self.endTimeMutex, self.endTime)
                        # print(f'ref et: {et}')
                        time.sleep(0)

    def detect_thread(self):
        lastFrame = None
        lastSavedTime = 0
        while True:
            time.sleep(0.5)
            self.imgMutex.acquire()
            frame = self.img
            self.imgMutex.release()

            gray = None
            detected = False
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if lastFrame is None:
                    lastFrame = gray.astype("float")

                cv2.accumulateWeighted(gray, lastFrame, 0.7)
                diff = cv2.absdiff(gray.astype("float"), lastFrame)
                thresh = cv2.threshold(diff.astype("uint8"), 4, 255, cv2.THRESH_BINARY)[1]
                contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contours:
                    if cv2.contourArea(c) > 600:
                        detected = True
                        print(f'ContourArea: ${cv2.contourArea(c)}')
                        break
            except Exception as e:
                print(e)
                if gray is not None:
                    lastFrame = gray.astype("float")

            if detected:
                stillPath, _ = getFilenames()

                self.imgMutex.acquire()
                if (self.img is not None ) and (time.time() - lastSavedTime > self.extendInterval):
                    cv2.imwrite(stillPath, self.img)
                    lastSavedTime = time.time()
                self.imgMutex.release()
                
                self.endTimeMutex.acquire()
                self.endTime = time.time() + self.extendInterval
                # print(f'new et: {self.endTime}')
                self.endTimeMutex.release()

            else:
                self.endTimeMutex.acquire()
                self.endTime = time.time() - 1
                self.endTimeMutex.release()
                try:
                    cv2.accumulateWeighted(gray, lastFrame, 0.7)
                except Exception as e:
                    print(e)
                    if gray is not None:
                        lastFrame = gray.astype("float")

    def run(self):
        t1 = threading.Thread(target=self.capture_thread)
        t2 = threading.Thread(target=self.detect_thread)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

s = surveillance()
s.run()