import streamlit as st
import cv2
import tempfile
from datetime import datetime

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

        if frame_count==5:
            st.error("⚠ 보호구역 내 위험 요소 감지 ⚠", icon="🚨")
        frame_count+=1

    cap.release()
