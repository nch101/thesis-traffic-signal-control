import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

import cv2

cap = cv2.VideoCapture('rtsp://admin:test12345@192.168.0.30:554/onvif1', cv2.CAP_FFMPEG)
ret, frame = cap.read()

while ret:
    cv2.imshow('test', frame)
    ret, frame = cap.read()
    key = cv2.waitKey(20)

    if key == 27:
        cv2.imwrite('raw-image6.png', frame)
        break

cap.release()
cv2.destroyAllWindows()