# 🚦 Traffic Violation Detection System

An AI-powered computer vision project that detects and flags **traffic violations** including:
- 🚦 Red-Light Violation
- 🛑 Stop-Line Violation
- ↔️ Lane Violation

Built with **YOLOv8** and Python, this system processes traffic videos/images to automatically identify violations and log them for further analysis.

---

## 🚀 Features

### 🚦 Red-Light Violation Detection
- Detects vehicles moving past the signal during a red light  
- Logs timestamp, vehicle position, and violation type  
- Generates annotated video output with bounding boxes  

### 🛑 Stop-Line Violation Detection
- Identifies vehicles crossing beyond the stop line at traffic signals  
- Visualizes stop-line boundaries for easier monitoring  
- Stores violation evidence with video snapshots  

### ↔️ Lane Violation Detection
- Monitors vehicles deviating from their lane  
- Detects improper overtaking or crossing lane boundaries  
- Exports results with annotated frames  

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher  
- CUDA-enabled GPU (optional, for faster inference)  

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hemanth-1904/traffic-violation.git
   cd traffic-violation
