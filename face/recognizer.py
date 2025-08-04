import face_recognition
import numpy as np
import os
import cv2

KNOWN_DIR = "data/known_faces"

def load_known_faces():
    known_encodings = []
    known_names = []
    if not os.path.exists(KNOWN_DIR):
        os.makedirs(KNOWN_DIR)
    for fn in os.listdir(KNOWN_DIR):
        if fn.lower().endswith((".jpg", ".png", ".jpeg")):
            img = face_recognition.load_image_file(os.path.join(KNOWN_DIR, fn))
            encs = face_recognition.face_encodings(img)
            if len(encs) > 0:
                known_encodings.append(encs[0])
                known_names.append(os.path.splitext(fn)[0])
    return known_encodings, known_names

def recognize_face(face_img, known_encodings, known_names):
    try:
        rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        encs = face_recognition.face_encodings(rgb)
        if len(encs) == 0:
            return "Unknown"
        face_enc = encs[0]
        if known_encodings:
            distances = face_recognition.face_distance(known_encodings, face_enc)
            min_idx = np.argmin(distances)
            if distances[min_idx] < 0.45:
                return known_names[min_idx]
        return "Unknown"
    except Exception as e:
        return "Unknown"

def save_new_face(face_img, name):
    filename = os.path.join(KNOWN_DIR, f"{name}.jpg")
    cv2.imwrite(filename, face_img)
