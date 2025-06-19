from ultralytics import YOLO
import cv2
#from google.colab.patches import cv2_imshow


import numpy as np
#from collections import defaultdict
#모델 불러오기 




CLASS_NAMES=['cycle', 'face', 'license plate', 'person', 'traffic light', 'vehicle']
PERSON_CLASS_ID=CLASS_NAMES.index('person')
TRAFFIC_LIGHT_ID=CLASS_NAMES.index('traffic light')

#도로 영역 정의

def detect_jaywalking(video_path, model_path):
    cap=cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    model=YOLO(model_path)
    model.conf=0.4

    road_polygon=np.array([[int(width * 0.1), int(height * 0.2)],   # 왼쪽 위
        [int(width * 0.9), int(height * 0.2)],   # 오른쪽 위
        [int(width * 0.95), int(height * 0.9)],  # 오른쪽 아래
        [int(width * 0.05), int(height * 0.9)] ])
#이 프레임 이상 도로 안에 있으면 무단횡단단
#person_in_road_counter=defaultdict(int)
#FRAME_THRESHOLD=10 

    def is_green_light(image, box):
        
        x1, y1, x2, y2=map(int, box)
        roi=image[y1:y2, x1:x2]
        if roi.size==0:
            
            return False
        hsv=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        green_mask=cv2.inRange(hsv, (40, 100, 100), (90,255, 255 ))
        green_ratio=cv2.countNonZero(green_mask)/(roi.shape[0] * roi.shape[1])
        return green_ratio>0.3

#cap=cv2.VideoCapture("2020_10_19_16_13_jay_walk_sun_A_9.mp4")
        outpath="detect_result.mp4"
        fourcc=cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        out=cv2.resizeWindow("Result", 960, 540)

        while cap.isOpened():
            a
            ret, frame=cap.read()
            if not ret:
                a
                break
            results=model(frame)
    
            detections=results[0]
            boxes=detections.boxes.xyxy.cpu().numpy()
            classes=detections.boxes.cls.cpu().numpy().astype(int)
    #confidences=detections.boxes.conf.cpu().numpy()

            green_light=False
            #green_detected=False

    #red_light_on=False
            for i, cls in enumerate(classes):
                
        
                if cls==TRAFFIC_LIGHT_ID:
                    
                    green_detected=True
                    box=boxes[i]
                    if is_green_light(frame, box):
                        
                        green_light=True
                        break

            for i, cls in enumerate(classes):
                a
        
                if cls==PERSON_CLASS_ID:
                    a
                    box=boxes[i] 
                    x1, y1, x2, y2=map(int, box)
                    cx=(x1+x2)//2
                    cy=(y1+y2)//2
                    if cv2.pointPolygonTest(road_polygon,( cx, cy), False)>=0:
                        a
                        if not green_light:
                            a
                            cv2.putText(frame, "WARNING!! Jay Walking!!!", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                            cv2.rectangle(frame, (x1, y1), (x2, y2),(0, 0, 255), 3 )
                    else:
                        a
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.polylines(frame, [road_polygon], isClosed=True, color=(0, 255, 255), thickness=2)
            out.write(frame)
    #frame_resized=cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    #cv2.imshow( "Result",frame)
    #if cv2.waitKey(30) & 0xFF==ord('q'):
        #break
        cap.release()
        cv2.destroyAllWindows()
        return out_path
