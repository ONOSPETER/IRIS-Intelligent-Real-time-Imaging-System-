import cv2
import torch
import face_recognition
import random
from deep_sort_realtime.deepsort_tracker import DeepSort
from yolov5 import YOLOv5
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

class EYE:
    def __init__(self, yolo_model_path="yolov5s.pt"):
        # Initialize YOLOv5 for target detection
        self.yolo_model = YOLOv5(yolo_model_path)
        
        # Initialize DeepSORT for tracking
        self.tracker = DeepSort()
        
        # Initialize Detectron2 for action recognition
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.action_predictor = DefaultPredictor(self.cfg)
        
        # Variables for manually marked target
        self.marked_target = None
        self.previous_position = None

    def set_target(self, frame):
        # User-drawn bounding box to mark the target
        r = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Frame")
        if r:
            self.marked_target = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))

    def mark_and_track_targets(self, frame):
        # Detect and track targets
        detections = self.yolo_model.predict(frame).xyxy[0]
        if self.marked_target:
            tracked_targets = self.tracker.update_tracks(detections, frame=frame)
            for track in tracked_targets:
                if track.is_confirmed() and track.to_ltwh()[:2] == self.marked_target[:2]:
                    self.marked_target = track.to_ltwh()  # Update to new position
                    return self.marked_target
        return None

    def track_direction_and_trajectory(self, current_position):
        # Determine target movement direction
        if self.previous_position is None:
            self.previous_position = current_position
            return "Stationary"

        direction = ""
        x_diff = current_position[0] - self.previous_position[0]
        y_diff = current_position[1] - self.previous_position[1]
        if abs(x_diff) > abs(y_diff):
            direction = "right" if x_diff > 0 else "left"
        else:
            direction = "down" if y_diff > 0 else "up"
        
        self.previous_position = current_position
        return direction

    def analyze_action(self, frame, bounding_box):
        # Detect action within bounding box using Detectron2
        x, y, w, h = bounding_box
        target_area = frame[y:y+h, x:x+w]

        # Run Detectron2 prediction
        outputs = self.action_predictor(target_area)
        instances = outputs["instances"]

        actions = []
        if instances.has("pred_classes"):
            classes = instances.pred_classes
            scores = instances.scores
            for cls, score in zip(classes, scores):
                if score > 0.5:
                    action_label = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes[cls]
                    actions.append(action_label)
        
        return actions  # List of recognized actions

    def recognize_and_screengrab_face(self, frame, bounding_box):
        # Detect faces within bounding box and screengrab if detected
        x, y, w, h = bounding_box
        target_face = frame[y:y+h, x:x+w]
        face_locations = face_recognition.face_locations(target_face)
        if face_locations:
            face_image = target_face[face_locations[0][0]:face_locations[0][2], face_locations[0][3]:face_locations[0][1]]
            cv2.imwrite("target_face_screengrab.jpg", face_image)
            return "Face screengrab saved."
        return None

    def process_frame(self, frame):
        # Main function to process a single frame and return relevant data
        if self.marked_target:
            tracked_position = self.mark_and_track_targets(frame)
            if tracked_position:
                direction = self.track_direction_and_trajectory(tracked_position[:2])
                actions = self.analyze_action(frame, tracked_position)
                face_result = self.recognize_and_screengrab_face(frame, tracked_position)

                return {
                    "position": tracked_position,
                    "direction": direction,
                    "actions": actions,
                    "face_recognition": face_result
                }
        return None

# Example usage
eye_module = EYE()
frame = cv2.imread("input_frame.jpg")

# User marks the target
eye_module.set_target(frame)

# Process the frame with all functionalities integrated
data = eye_module.process_frame(frame)
print("Processed frame data:", data)
