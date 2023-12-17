libcamera-vid -t 0 --inline -o - --width 640 --height 480 | \
cvlc stream:///dev/stdin --sout='#rtp{sdp=rtsp://:8554/stream}' :demux=h264 

# libcamera-vid -t 0 --inline -o - --width 640 --height 480 --codec mjpeg | \
# cvlc stream:///dev/stdin --sout='#std{access=http, mux=ts, dst=:8080/stream.mjpg}' :demux=mjpeg

# libcamera-vid -t 0 --inline -o - --width 640 --height 480 | \
# cvlc stream:///dev/stdin --sout='#transcode{vcodec=h264,acodes=mpga,ab=128,channels=2,samplerate=4410,scodec=none}:http{mux=ffmpeg{mux=flv},dst=:8554/stream1}'