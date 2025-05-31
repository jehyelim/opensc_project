from ultralytics import YOLO
import cv2

model=YOLO("best.pt")

def detect_objects(frame):
    results=model(frame)
    detections=[]
    for result in results:
        for box in result.boxes:
            cls_id=int(box.cls[0])
            conf=float(box.conf[0])
            x1, y1, x2, y2=map(int,box.xyxy[0] )
            detections.append( {
                "class_id": cls_id, "confidence": conf, "box":[x1, y1, x2, y2]
            })
    return detections 
    