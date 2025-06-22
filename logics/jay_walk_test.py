from ultralytics import YOLO
import cv2
#from google.colab.patches import cv2_imshow


import numpy as np

#모델 불러오기 



#도로 영역 정의

def detect_jaywalking(video_path, model_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    model = YOLO(model_path)
    model.conf = 0.4

    detected=False 

    CLASS_NAMES = ['cycle', 'face', 'license plate', 'person', 'traffic light', 'vehicle']
    PERSON_CLASS_ID = CLASS_NAMES.index('person')
    TRAFFIC_LIGHT_ID = CLASS_NAMES.index('traffic light')

    road_polygon = np.array([
        [int(width * 0.1), int(height * 0.2)],
        [int(width * 0.9), int(height * 0.2)],
        [int(width * 0.95), int(height * 0.9)],
        [int(width * 0.05), int(height * 0.9)]
    ])

    def is_green_light(image, box):
        x1, y1, x2, y2 = map(int, box)
        roi = image[y1:y2, x1:x2]
        if roi.size == 0:
            return False
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, (40, 100, 100), (90, 255, 255))
        green_ratio = cv2.countNonZero(green_mask) / (roi.shape[0] * roi.shape[1])
        return green_ratio > 0.3

    out_path = "output/jay_walk_result.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 30.0, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results[0]
        boxes = detections.boxes.xyxy.cpu().numpy()
        classes = detections.boxes.cls.cpu().numpy().astype(int)

        green_light = False

        for i, cls in enumerate(classes):
            if cls == TRAFFIC_LIGHT_ID:
                box = boxes[i]
                if is_green_light(frame, box):
                    green_light = True
                    break

        for i, cls in enumerate(classes):
            if cls == PERSON_CLASS_ID:
                box = boxes[i]
                x1, y1, x2, y2 = map(int, box)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                if cv2.pointPolygonTest(road_polygon, (cx, cy), False) >= 0:
                    if not green_light:
                        detected=True
                        cv2.putText(frame, "WARNING!! ", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.polylines(frame, [road_polygon], isClosed=True, color=(0, 255, 255), thickness=2)
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return detected
