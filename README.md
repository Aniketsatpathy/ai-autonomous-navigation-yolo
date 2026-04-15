# 🚗 AI-Based Autonomous Navigation System (YOLO + OpenCV)

## 🔍 Overview

This project implements a real-time AI-based autonomous navigation system using computer vision and deep learning. It processes real-world driving videos to detect obstacles, understand lane structure, and plan safe navigation paths.

---

## ❗ Problem Statement

Autonomous systems must perceive dynamic environments and make real-time decisions. Traditional rule-based systems fail in complex, unpredictable scenarios.

This project addresses four critical challenges:

- **Obstacle Detection**: Identifying objects and hazards in the environment
- **Lane Understanding**: Recognizing and tracking road lanes
- **Safe Path Planning**: Computing collision-free navigation routes
- **Intelligent Decision Making**: Selecting optimal navigation strategies

---

## 🏭 Industry Relevance

This technology is deployed across multiple autonomous systems:

- **Self-Driving Vehicles**: Tesla, Waymo, and other autonomous car manufacturers
- **Warehouse Automation**: Autonomous robots for inventory management
- **Last-Mile Delivery**: Autonomous delivery bots and drones
- **Smart Mobility Systems**: Connected autonomous transportation networks

---

## 🧠 System Workflow

The autonomous navigation pipeline operates in the following sequence:

1. **Input**: Capture video frame from camera feed
2. **Lane Detection**: Process frame using OpenCV for lane identification
3. **Object Detection**: Detect obstacles using YOLOv8
4. **Path Planning**: Compute safe navigation route using A* algorithm
5. **Decision Making**: Evaluate and select optimal action
6. **Visualization**: Display results with annotations

---

## 🛠️ Tech Stack

- **Python**: Core programming language
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computations
- **YOLOv8** (Ultralytics): State-of-the-art object detection
- **A* Algorithm**: Pathfinding and route optimization

---

## 📂 Dataset

- **Source**: Real-world driving video footage from YouTube dashcam
- **Format**: MP4 video file
- **Content**: Urban driving scenarios with varied traffic and environmental conditions

---

## 🏗️ Architecture

```
Video Input
    ↓
Lane Detection (OpenCV)
    ↓
Object Detection (YOLOv8)
    ↓
Path Planning (A*)
    ↓
Decision Making
    ↓
Visualization & Output
```

---

## ⚙️ Installation

Follow these steps to set up the project:

```bash
# Clone the repository
git clone https://github.com/Aniketsatpathy/ai-autonomous-navigation-yolo.git
cd ai-autonomous-navigation-yolo

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

Execute the autonomous navigation system:

```bash
python run.py
```

The system will process the video, perform real-time detection and planning, and generate annotated output.

---

## 📊 Results

The system achieves the following capabilities:

- ✅ Real-time object detection with high accuracy
- ✅ Robust lane tracking and identification
- ✅ Dynamic path planning with obstacle avoidance
- ✅ Intelligent decision making for navigation

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

[View Demo Video](https://github.com/Aniketsatpathy/ai-autonomous-navigation-yolo/raw/main/outputs/result_videos/demo_output.avi)

---

## 📚 Learning Outcomes

This project demonstrates key competencies:

- **End-to-End AI Pipeline Development**: Building complete autonomous systems
- **Computer Vision + Deep Learning Integration**: Combining multiple ML techniques
- **Real-Time System Optimization**: Achieving high performance under constraints
- **Modular System Design**: Creating reusable and scalable components

---

## 🚀 Future Improvements

Planned enhancements for the project:

- **Object Tracking**: Multi-object tracking across frames
- **Collision Prediction**: Anticipatory hazard detection
- **CARLA Integration**: Simulation environment testing
- **Reinforcement Learning**: Learning-based decision optimization

---

## 📝 Project Timeline

| Day | Phase | Activities | Outcome |
|-----|-------|-----------|---------|
| 1 | Setup | Repository initialization, folder structure | Initial project setup |
| 2 | Data | Video ingestion, OpenCV pipeline testing | Video input pipeline |
| 3 | Preprocessing | Lane detection implementation | Lane detection module |
| 4 | Model | YOLOv8 integration | Object detection integration |
| 5 | Planning | A* pathfinding algorithm | Path planning module |
| 6 | Evaluation | Performance optimization, UI improvements | Optimized visualization |
| 7 | Documentation | README, assets, final packaging | Complete documentation |

---

## 👨‍💻 Author

**Aniket Satpathy**

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project.

---

**Last Updated**: April 2026
