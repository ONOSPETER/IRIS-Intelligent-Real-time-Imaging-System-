IRIS: Intelligent Real-time Imaging System

IRIS is a comprehensive, AI-driven surveillance system designed to track and analyze targets across multiple camera feeds in real-time. Using image processing and computer vision, IRIS enables security personnel to monitor targets, analyze behaviors, and anticipate movements across a network of cameras. The system is split into three core modules: EYE (image processing), FEED (camera feed handler), and GRAPH (geographic mapping and trajectory prediction).

Features

Target Marking & Tracking: Easily mark and track targets across multiple camera feeds.

Direction & Trajectory Analysis: Determine target movement relative to camera locations.

Action Recognition: Recognize target actions such as walking or running.

Facial Recognition: Capture and recognize faces when visible.

Camera Feed Management: Display live camera feeds and dynamically switch based on target movement.

Path Prediction: Identify the best camera for target observation based on geographic data.


Project Structure:
main.py: The primary entry point for the IRIS system, which provides a CLI to interact with all functionalities.

eye_module.py: The EYE module, handling image processing tasks like marking, tracking, and facial recognition.

feed_module.py: The FEED module, managing live camera feeds and retrieving data based on user input.

graph_module.py: The GRAPH module, which maps target trajectory to geographic coordinates and identifies the next-best camera for tracking.

config/camera_config.json: JSON file containing details of each camera, including positions and views.

config/graph_config.json: JSON file defining the graph structure, simulating camera network connections and spatial distances.

config/map.png: Geographical map of the monitored area for overlaying camera locations.


Setup & Installation

1. Clone the Repository:

git clone https://github.com/username/IRIS.git
cd IRIS


2. Install Required Packages: Ensure you have Python 3.8+ installed, then run:

pip install opencv-python-headless yolov5 deep_sort_realtime detectron2 face_recognition


3. Setup Configuration Files:

Modify config/camera_config.json and config/graph_config.json with the camera and graph data for your environment.

Place the geographical map in config/map.png.



4. Run the IRIS System:

python main.py



Module Details

EYE Module (eye_module.py)

Handles all image processing and target tracking. Functions include:

mark_and_track_targets: Marks targets, tracks movement, and maintains focus across frames.

track_direction_and_trajectory: Analyzes and outputs the direction and trajectory of the target.

analyze_action: Recognizes target actions (e.g., walking, running).

recognize_and_screengrab_face: Detects and screengrabs the target’s face when visible.


FEED Module (feed_module.py)

Manages camera feeds by:

get_camera_feed: Retrieves and displays live feeds from specified cameras.

switch_camera_feed: Switches camera feed based on tracking information.


GRAPH Module (graph_module.py)

Translates trajectory information into geographical context, using functions to:

map_target_location: Maps target movement to geographical coordinates.

calculate_next_camera: Determines the optimal camera for continued observation.



---

Usage

The system launches a CLI with options to display a camera feed, mark and track targets, disengage tracking, and exit. Each function supports seamless switching between feeds based on target movement and provides actionable insights for efficient monitoring.


---

IRIS combines deep learning and geospatial data, empowering users with a powerful, real-time surveillance tool for enhanced situational awareness and security management.

