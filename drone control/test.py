import time, cv2
from threading import Thread
from djitellopy import Tello

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

def drone_control():
    f= open('./command.txt', 'r')
    command=f.readlines()
    for i in command:
        if i == "takeoff\n":
            tello.takeoff()

        elif i[:5] =="speed":
            speed=int(i[6:])
            tello.set_speed(speed)
        elif i[:3] =="ccw":
            angle=int(i[4:])
            tello.rotate_counter_clockwise(angle)

        elif i[:2] =="cw":
            angle=int(i[3:])
            tello.rotate_clockwise(angle)

        elif i[:7] == "forward":
            distance=int(i[8:])
            tello.move_forward(distance)

        elif i == "land\n":
            tello.land()
            

# tello = Tello()
# tello.connect()
# print(tello.get_battery())
# keepRecording = True
# tello.streamon()
# frame_read = tello.get_frame_read()
#
#
# recorder = Thread(target=videoRecorder)
# recorder.start()
#
# tello.takeoff()
# tello.rotate_clockwise(180)
# tello.land()
# tello.end()
#
# keepRecording = False
# recorder.join()

drone_control()