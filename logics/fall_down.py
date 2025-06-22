from ultralytics import YOLO
import cv2
import numpy as np

def find_nearest_key(fall_status, x1, y1, threshold=30):
    for kx, ky in fall_status.keys():
        if abs(kx - x1) < threshold and abs(ky - y1) < threshold:
            return (kx, ky)
    return None

def detect_fall(video_path, model_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    model = YOLO(model_path)
    model.conf = 0.4

    output_path = "output/fall_result.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    fall_status = {}
    fall_display_counter = 0
    fall_position = None

    detected=False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results[0]
        boxes = detections.boxes.xyxy.cpu().numpy()
        classes = detections.boxes.cls.cpu().numpy().astype(int)

        for i, cls in enumerate(classes):
            if cls == 0:  # person
                x1, y1, x2, y2 = map(int, boxes[i])
                w = x2 - x1
                h = y2 - y1
                ar = w / h if h != 0 else 0

                if h < 120 and ar > 0.82:
                    key = find_nearest_key(fall_status, x1, y1)
                    if key:
                        fall_status[key] += 1
                    else:
                        key = (x1, y1)
                        fall_status[key] = 1

                    if fall_status[key] >= 3:
                        detected=True
                        fall_display_counter = 30
                        if fall_position is None:
                            fall_position = (x1, max(50, y1 - 10))

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if fall_display_counter > 0 and fall_position is not None:
            fx, fy = fall_position
            cv2.putText(frame, "FALL DETECTED!", (fx, fy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
            fall_display_counter -= 1

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return detected

