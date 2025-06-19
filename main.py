


import streamlit as st
import os
import tempfile
import concurrent.futures
import shutil
from logics.jay_walk_test import detect_jaywalking
from logics.fall_down_test import detect_fall_down
from logics.suddenly_appear_test import detect_suddenly_appear
from email import send_alert
from playsound import playsound

st.title("도로상에서의 어린이 위험 행동 감지 시스템")
st.write("영상에서 jay_walk, suddenly appear, fall down을 자동으로 감지합니다.")

uploaded_video=st.file_uploader("영상을 업로드하세요 (mp4)", type=["mp4"])

if uploaded_video is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(uploaded_video.read())
        video_path=temp_video_file.name

    jay_model_path="models/jay_walk.pt"
    fall_model_path="models/fall_down.pt"
    sudden_model_path="models.suddenly_appear.pt"

    st.info("분석 중입니다.")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures={
            executor.submit(detect_jaywalking, video_path, jay_model_path):"jay", 
            executor.submit(detect_fall_down, video_path, fall_model_path):"fall",
            executor.submit(detect_suddenly_appear, video_path, sudden_model_path):"sudden"
        }
        results={}
        for future in concurrent.futures.as_completed(futures):
            name=futures[future]
            try:
                results[name]=future.result()
            except Exception as e:
                results[name]=False
                st.warning(f"{name} 로직 실행 중 오류 발생: {e} ")
    if any(results.values()):
        st.error("🚨 위험 행동이 감지되었습니다!")
        playsound("alert.mp3")
        send_alert()
    else:
        st.success("위험 행동이 감지되지 않았습니다.")

    jay_alert=detect_jaywalking(video_path, jay_model_path)
    fall_alert=detect_fall_down(video_path, fall_model_path)
    sudden_alert=detect_suddenly_appear(video_path,sudden_model_path)
    
    if jay_alert or fall_alert or sudden_alert:
        st.error("🚨 위험 행동이 감지되었습니다!")
        playsound("alert.mp3")
        send_alert()
    else:
        st.success("위험 행동이 감지되지 않았습니다.")
        

    output_video_path="output/result.mp4"
    if os.path.exists(output_video_path):
        with open(output_video_path, "rb") as f:
            st.download_button("⬇️ 결과 영상 다운로드", f, file_name="result.mp4")

