import streamlit as st
import cv2
import tempfile
from datetime import datetime
from detector import detect_objects

st.title("어린이 보호구역 위험 감지 시스템")

video_file=st.file_uploader("영상을 업로드하세요", type=["mp4", "avi", "mov"])

if video_file:
    tfile=tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    st.video(video_file)
    cap=cv2.VideoCapture(tfile.name)

    frame_count=0
    while cap.isOpened():
        ret, frame=cap.read()
        if not ret or frame_count>10:
            break

        for det in detections:
            if det["class-id"]==2:
                st.error("⚠ 보호구역 내 차량 감지됨! 위험합니다 ⚠", icon="🚨")
                break
        frame_count+=1

    cap.release()
