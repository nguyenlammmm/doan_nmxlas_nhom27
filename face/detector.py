import mediapipe as mp
import cv2

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

def detect_faces(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)
    locations = []

    if results.detections:
        for det in results.detections:
            box = det.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x1 = int(box.xmin * w)
            y1 = int(box.ymin * h)
            x2 = x1 + int(box.width * w)
            y2 = y1 + int(box.height * h)
            locations.append((y1, x2, y2, x1))

    return locations

