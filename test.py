import torch
import numpy as np
import cv2
from threading import Thread
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import Annotator



from djitellopy import Tello

MODEL_PATH = 'runs/train/exp4/weights/e50b32.pt'

img_size = 416
conf_thres = 0.5  # confidence threshold
iou_thres = 0.45  # NMS IOU threshold
max_det = 1000  # maximum detections per image
classes = None  # filter by class
agnostic_nms = False  # class-agnostic NMS

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

ckpt = torch.load(MODEL_PATH, map_location=device)
model = ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval()
class_names = ['fire'] # model.names
stride = int(model.stride.max())
colors = ((0, 255, 0)) # (gray, red, green)

me = Tello()
me.connect()
print(me.get_battery())

# Initiate video stream
me.streamon()
cap = me.get_frame_read()
# cap = cv2.VideoCapture('data/testVideo.mp4')
#cap = cv2.VideoCapture(0)

# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# out = cv2.VideoWriter('data/output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

def video_with_yolo():
    while True:
        #ret, img = cap.read()
        img = cap.frame
        # if not ret:
        #     break

        # preprocess
        img_input = letterbox(img, img_size, stride=stride)[0]
        img_input = img_input.transpose((2, 0, 1))[::-1]
        img_input = np.ascontiguousarray(img_input)
        img_input = torch.from_numpy(img_input).to(device)
        img_input = img_input.float()
        img_input /= 255.
        img_input = img_input.unsqueeze(0)

        # inference
        pred = model(img_input, augment=False, visualize=False)[0]

        # postprocess
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)[0]

        pred = pred.cpu().numpy()

        pred[:, :4] = scale_coords(img_input.shape[2:], pred[:, :4], img.shape).round()

        annotator = Annotator(img.copy(), line_width=3, example=str(class_names), font='data/malgun.ttf')

        for p in pred:
            class_name = class_names[int(p[5])]

            x1, y1, x2, y2 = p[:4]
            print(p)
            annotator.box_label([x1, y1, x2, y2], '%s %d' % (class_name, float(p[4]) * 100), color=colors[int(p[5])])

        result_img = annotator.result()

        cv2.imshow('result', result_img)
        # out.write(result_img)
        if cv2.waitKey(1) == ord('q'):
            break


# Thread video_with_yolo start
video = Thread(target=video_with_yolo)
video.start()

# tello control part
def drone_control():
    f= open('./command.txt', 'r')
    command=f.readlines()
    for i in command:
        if i == "takeoff\n":
            me.takeoff()

        elif i[:5] =="speed":
            speed=int(i[6:])
            me.set_speed(speed)
        elif i[:3] =="ccw":
            angle=int(i[4:])
            me.rotate_counter_clockwise(angle)

        elif i[:2] =="cw":
            angle=int(i[3:])
            me.rotate_clockwise(angle)

        elif i[:7] == "forward":
            distance=int(i[8:])
            me.move_forward(distance)

        elif i == "land\n":
            me.land()
drone_control()
me.end()

cap.release()
video.join()
