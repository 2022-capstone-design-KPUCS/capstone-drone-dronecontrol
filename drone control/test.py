import time, cv2
from threading import Thread
from djitellopy import Tello



tello = Tello()
tello.connect()
print(tello.get_battery())
keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    global keepRecording
    start_time = time.time()
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video2.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        if time.time() - start_time > 5000:
            keepRecording = False
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

recorder = Thread(target=videoRecorder)
recorder.start()

tello.takeoff()
tello.rotate_clockwise(180)
tello.land()
tello.end()

keepRecording = False
recorder.join()