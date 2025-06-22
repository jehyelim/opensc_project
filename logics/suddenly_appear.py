from ultralytics import YOLO
import cv2
import numpy as np

def detect_suddenlyappear(video_path, model_path, output_path="output/result.mp4"):
    cap = cv2.VideoCapture(video_path)
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ★ TRACK 모드로 모델 로드 (detect→track)
    model = YOLO(model_path)
    model.conf = 0.4

    CLASS_NAMES = ['suddenlyappear']
    TARGET_ID   = 0  # 단일 클래스

    # 도로 폴리곤
    road_poly = np.array([
        [int(w*0.1), int(h*0.2)],
        [int(w*0.9), int(h*0.2)],
        [int(w*0.95),int(h*0.9)],
        [int(w*0.05),int(h*0.9)],
    ])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out    = cv2.VideoWriter(output_path, fourcc, 30, (w,h))

    # 이전 프레임에서 ROI 안에 있었는지 기록
    prev_inside = {} # {track_id: bool}
    detected=False

    while True:
        ret, frame = cap.read()
        if not ret: break

        results = model.track(source=[frame], persist=True, stream=True)
        for r in results:
            if not r.boxes or r.boxes.xyxy is None or r.boxes.cls is None or r.boxes.id is None:
                continue
            boxes   = r.boxes.xyxy.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy().astype(int)
            ids     = r.boxes.id.cpu().numpy().astype(int)

            for cls, box, tid in zip(classes, boxes, ids):
                if cls != TARGET_ID:
                    continue

                x1,y1,x2,y2 = map(int, box)
                cx, cy     = (x1+x2)//2, (y1+y2)//2
                inside = cv2.pointPolygonTest(road_poly, (cx,cy), False) >= 0

                # ★ 진입 이벤트: 이전엔 밖이었다가(또는 기록 없음) 지금 안에 들어온 경우
                if inside and not prev_inside.get(tid, False):
                    detected=True
                    cv2.putText(frame, "Detected!", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)
                    cv2.rectangle(frame, (x1,y1),(x2,y2),(0,0,255),3)
                else:
                    # ROI 밖이거나 이미 안에 있던 객체는 녹색
                    cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)

                # 상태 업데이트
                prev_inside[tid] = inside

        # 도로 폴리곤 그리기
        cv2.polylines(frame, [road_poly], True, (0,255,255),2)
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return detected  # 진입 감지는 화면에 표시로 대체


