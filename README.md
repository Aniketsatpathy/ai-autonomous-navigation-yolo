# 🚗 AI-Based Autonomous Navigation System (YOLO + OpenCV)

## 🔍 Overview

This project implements a real-time AI-based autonomous navigation system using computer vision and deep learning. It processes real-world driving videos to detect obstacles, understand lane structure, plan safe paths, and make driving decisions.

---

## ❗ Problem Statement

Autonomous systems must perceive dynamic environments and make real-time decisions. Traditional rule-based systems fail in complex scenarios.

This project solves:

* obstacle detection
* lane understanding
* safe path planning
* navigation decisions

---

## 🏭 Industry Relevance

Used in:

* self-driving cars (Tesla, Waymo)
* warehouse robots
* delivery bots
* smart mobility systems

---

## 🧠 System Workflow

1. Input video frame
2. Lane detection (OpenCV)
3. Object detection (YOLOv8)
4. Path planning (A*)
5. Decision making
6. Visualization

---

## 🛠️ Tech Stack

* Python
* OpenCV
* NumPy
* YOLOv8 (Ultralytics)
* A* Algorithm

---

## 📂 Dataset

* Real-world driving video (YouTube dashcam footage)

---

## 🏗️ Architecture

```
Video → Detection → Planning → Decision → Visualization
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/ai-autonomous-navigation-yolo.git
cd ai-autonomous-navigation-yolo

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python run.py
```

---

## 📊 Results

* Real-time object detection
* Lane tracking
* Dynamic path planning
* Intelligent navigation decisions

---

## 🖼️ Screenshots

### Navigation Output - Detection & Lane Understanding
![Navigation Output 1](https://raw.githubusercontent.com/Aniketsatpathy/ai-autonomous-navigation-yolo/main/images/screenshots/Navigation_output1.png)

### Real-time Path Planning & Obstacle Avoidance
![Navigation Output 2](https://raw.githubusercontent.com/Aniketsatpathy/ai-autonomous-navigation-yolo/main/images/screenshots/Navigation_output2.png)

### System Terminal Output & Logs
![Terminal Log Output](https://raw.githubusercontent.com/Aniketsatpathy/ai-autonomous-navigation-yolo/main/images/screenshots/Terminal_log_output.png)

---

## 🎥 Demo Video

Experience the autonomous navigation system in action:

https://github.com/Aniketsatpathy/ai-autonomous-navigation-yolo/raw/main/outputs/result_videos/demo_output.avi

## 📚 Learning Outcomes

* End-to-end AI pipeline development
* Computer vision + deep learning integration
* Real-time system optimization
* Modular system design

---

## 🚀 Future Improvements

* Object tracking
* Collision prediction
* CARLA integration
* Reinforcement learning

---

## 👨‍💻 Author
Aniket Satpathy

## Project Timeline

Day 1 — Setup
create repo
folder structure

Commit:

Initial project setup

Day 2 — Data
add video
test OpenCV reading

Commit:

Added video input pipeline

Day 3 — Preprocessing
lane detection

Commit:

Implemented lane detection

Day 4 — Model
YOLO integration

Commit:

Integrated YOLOv8 detection

Day 5 — Planning
A* path

Commit:

Added path planning module

Day 6 — Evaluation
optimize speed
UI improvements

Commit:

Optimized performance and visualization

Day 7 — Upload
README
assets

Commit:
Finalized project with documentation and demo
