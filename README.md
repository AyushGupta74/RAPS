## Realtime Adaptive Pathfinding System (RAPS)

## Overview

The **Realtime Adaptive Pathfinding System (RAPS)** is an AI-driven urban routing system that dynamically adapts routes based on real-world traffic conditions. It integrates **computer vision**, **natural language processing**, and **graph-based shortest path algorithms** to demonstrate how live signals can influence routing decisions in real time.

The system is designed for **urban traffic scenarios** and is demonstrated using a **prebuilt San Francisco road network** derived from OpenStreetMap data.

---

## Problem Statement

Traditional navigation systems often rely on static edge weights or delayed traffic updates. They fail to demonstrate how **real-time, heterogeneous signals** (such as live traffic visuals or incident reports) can be fused and used to adapt routing decisions dynamically.

This project addresses the problem by answering:

> How can vision-based traffic density and text-based incident signals be fused to adaptively reroute paths on a city-scale road network?

---

## Objectives

* Build a real-time adaptive routing system using a city road graph
* Integrate computer vision to estimate traffic congestion from videos
* Integrate NLP to simulate incident severity signals
* Fuse multiple signals into a unified congestion model
* Demonstrate adaptive rerouting using graph cost manipulation
* Provide an interactive visualization interface for experimentation

---

## System Architecture

The system follows a **clean separation of concerns** with four major layers:

### 1. User Interface Layer (Streamlit)

* Handles user interaction
* Accepts start/end locations
* Accepts traffic video uploads
* Visualizes routes on an interactive map

### 2. Orchestration Layer

* Coordinates all subsystems
* Performs sensor fusion (vision + NLP)
* Decides when and how routing should adapt
* Executes a two-phase routing strategy

### 3. Routing Engine

* Owns and manages the road graph
* Applies dynamic edge cost updates
* Computes shortest paths using NetworkX

### 4. Sensor Services

* Vision Service: estimates congestion from traffic videos
* Text Service: simulates incident severity from NLP signals

---

## Key Design Insight

A critical design decision in RAPS is the use of **route-aware adaptive penalties** instead of static or global congestion penalties.

### Why route-aware penalties?

Uniformly scaling all edge weights does **not** change the shortest path. Penalizing edges that are **not part of the candidate route** also does not affect routing.

RAPS therefore uses a **two-phase adaptive routing strategy**:

1. Compute a baseline shortest route
2. Penalize edges along the candidate route based on congestion signals
3. Recompute an alternative route

This guarantees rerouting when viable alternatives exist and aligns with established adaptive routing literature.

---

## Adaptive Routing Workflow

1. User selects start and end locations
2. Baseline shortest route is computed
3. Vision model analyzes traffic video to estimate vehicle density
4. NLP service provides an incident severity factor
5. Signals are fused into a congestion severity score
6. Candidate route edges are penalized dynamically
7. Shortest path is recomputed using updated edge weights
8. Adaptive route is visualized on the map

---

## Technologies Used

### Core

* Python 3.10+
* NetworkX
* OpenStreetMap / OSMnx
* Pyrosm

### Computer Vision

* Ultralytics YOLO
* OpenCV
* PyTorch

### NLP

* Hugging Face Transformers

### Visualization & UI

* Streamlit
* Folium

---

## Project Structure

```
RAPS_final/
│
├── app.py                     # Streamlit application
├── core/
│   ├── orchestrator.py        # Adaptive decision logic
│   ├── routing_engine.py      # Graph & routing logic
│   └── logger.py              # Central logging
│
├── services/
│   ├── vision_service.py      # Traffic analysis from video
│   └── text_service.py        # Incident severity estimation
│
├── config/
│   └── settings.py            # Paths and constants
│
├── models/
│   └── best.pt                # YOLO traffic model
│
├── data/
│   └── sf_graph.graphml       # Cached OSM road graph
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Create environment

```bash
conda create -n raps python=3.10
conda activate raps
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## How to Use

1. Initialize the system
2. Select start and end locations
3. Optionally upload a traffic video (MP4)
4. Start optimization
5. Observe adaptive route changes on the map
6. Check terminal logs for congestion and routing details

---

## Demonstration Scenarios

### Low Traffic Video

* Low average vehicle count
* Minimal edge penalty
* Route remains close to baseline

### High Traffic Video

* High vehicle density detected
* Significant penalty applied to candidate route
* Alternative route selected

---

## Logging and Explainability

The system logs:

* Vision obstacle factor
* NLP incident factor
* Congestion multiplier
* Baseline vs adaptive route length
* Penalized edges

These logs provide transparency and help validate adaptive behavior.

---

## Assumptions and Limitations

* Traffic localization is simulated via route-based penalization
* Vision inference is limited to sampled frames for performance
* NLP incident signals are simulated for demonstration
* System demonstrates adaptivity rather than real-time deployment scale

---

## Academic Validity

The architecture aligns with:

* Adaptive shortest path theory
* Route replanning strategies in robotics
* Traffic-aware navigation systems

The design choices are mathematically sound and defensible in academic evaluation.

---

## Future Enhancements

* Integration with live traffic APIs
* Multi-sensor spatial congestion modeling
* Asynchronous vision inference
* Real-time GPS tracking
* REST API deployment

---

## Conclusion

RAPS demonstrates how heterogeneous AI signals can be fused to adapt routing decisions in real time. The system prioritizes **correct adaptive logic**, **architectural clarity**, and **explainability**, making it suitable for academic evaluation and further research extensions.

---
## Author
Naqshab Javed
Priyaansh Malik
Ayush Gupta
Sonu Kharayat
