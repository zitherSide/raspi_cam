import cv2

class VideoContext:
    def __init__(self, filename, fourcc, fps, size):
        self.ost = cv2.VideoWriter(filename, fourcc, fps, size)
    
    def __enter__(self):
        return self.ost

    def __exit__(self, exc_type, exc_value, traceback):
        self.ost.release()

if __name__ == '__main__':
    import time
    cap = cv2.VideoCapture("url")

    io = cap.isOpened()
    if not io:
        print('Could not open')
        exit()

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    with VideoContext("vid.mp4", fourcc, 30, (640, 480)) as ost:
        end = time.time() + 5
        now = time.time()
        while now < end:
            ret, frame = cap.read()
            ost.write(frame)
            now = time.time()
    cap.release()