# 오픈소스프로그래밍 기말 프로젝트

## Introduction
  It is a system that automatically detects and warns children's dangerous behavior that may occur on the road in a child protection zone to    reduce traffic accidents among children.
  The main function is to detect a child's dangerous behavior (jay walk, suddenly appear, and fall down) in real time, float a warning          message notification with a warning sound. Images of detecting each dangerous behavior are also stored to check which behavior is detected.

## 
## usage dataset
  어린이 보호구역 내 어린이 도로보행 위험 행동 영상 데이터(https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=169)
  - Fall_down, jay_walk, suddenlyappear


## Features
- Real-time detection of dangerous Child behavior using YOLOv8
- Supports detection of:
  - Jay walk
  - Sudden appear
  - Fall down
- Displays on-screen warning messages
- Plays waring sounds('alert.mp3')
- Saves detection results as a vidio ('output/result.mp4')
  

## Project Structure
opensc_project/
    logics/ # Core detection logic (e.g., fall_down.py)
    models/ # YOLO trained model files (e.g., fall_down.pt)
    output/ # Output derectory for result videos
    alert.mp3 # Warning sound file
    main.py # Main entry point (Streanlit app)
    requirements.txt # Python dependencies
    README.md


## Example output
Below is an example of the system detecting a dangerous behavior in a child protection zone.
![Detection]
![Detection]
When dangerous behavior is detected:
- A red bounding box appears on the person
- A warning message is displayed
  


## Installation
#### 1. Clone the repository:
```
  git clone https://github.com/jehyelim/opensc_project.git
  cd opencd_project
```
#### 2. Install required dependencies:
```
pip install -r requirements.txt
```  
#### 3. Run the main:
``` 
streamlit run main.py
```





