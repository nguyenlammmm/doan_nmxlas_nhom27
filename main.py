
import cv2
import time
from camera.stream import get_frame
from face.detector import detect_faces
from face.analyzer import analyze_face
from face.recognizer import load_known_faces, recognize_face, save_new_face
from face.storage import load_names
from utils.logger import log_detection
from utils.overlay import draw_overlay
from utils.popup import ask_name_popup
import time
from utils.speaker import speak
from utils.speaker import speak_async

video = cv2.VideoCapture(0)
known_db = load_names()
known_encodings, known_names = load_known_faces()

frame_count = 0
analyzed_cache = {}
last_speak_time = {}

while True:
    frame = get_frame(video)
    locations = detect_faces(frame)
    frame_count += 1

    for i, loc in enumerate(locations):
        y1, x2, y2, x1 = loc
        face_crop = frame[y1:y2, x1:x2]
        face_crop_resized = cv2.resize(face_crop, (256, 256))

        # Nhận diện khuôn mặt
        name = recognize_face(face_crop_resized, known_encodings, known_names)
        label_id = name if name != "Unknown" else f"Person{i+1}"

        # Dùng cache hoặc phân tích lại mỗi 15 frame
        if label_id not in analyzed_cache or frame_count % 60 == 0:
            emotion, age, gender = analyze_face(face_crop_resized)
            analyzed_cache[label_id] = (emotion, age)
            if name != "Unknown":
                if name != "Unknown":
                    now = time.time()
                    last_time = last_speak_time.get(label_id, 0)
                    if now - last_time > 10:
                        speak_async(f"Hello {label_id}, you look {emotion} and about {age} years old.")
                        last_speak_time[label_id] = now
        else:
            emotion, age = analyzed_cache[label_id]

        label = f"{label_id} | {emotion} | {gender} | {age} Age"
        log_detection(label_id, emotion, age, gender)

        # Gợi ý lưu người mới
        key = cv2.waitKey(1)
        if name == "Unknown":
            cv2.putText(frame, "Press 'a' to save as new", (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if key & 0xFF == ord('a'):
                user_name = ask_name_popup()
                if not user_name:
                    user_name = f"new_{int(time.time())}"
                save_new_face(face_crop, user_name)
                print(f"Đã lưu khuôn mặt mới: {user_name}")
                known_encodings, known_names = load_known_faces()
                continue

        draw_overlay(frame, name, label, loc, emotion, name != "Unknown")

    instruction_text = "Press 'q' to exit"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(instruction_text, font, font_scale, thickness)
    text_x = 10
    text_y = frame.shape[0] - 10
    cv2.rectangle(frame, (text_x - 5, text_y - text_height - 5), (text_x + text_width + 5, text_y + 5), (0, 0, 0), -1)
    cv2.putText(frame, instruction_text, (text_x, text_y), font, font_scale, (0, 255, 255), thickness, cv2.LINE_AA)
    cv2.imshow("Mediapipe Face System", frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

