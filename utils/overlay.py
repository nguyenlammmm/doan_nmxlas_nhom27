import cv2
import os

AVATAR_DIR = "data/avatars"

def draw_overlay(frame, name, label, bbox, emotion, is_known):
    y1, x2, y2, x1 = bbox

    # Xác định màu khung
    if not is_known:
        box_color = (0, 0, 255)
    elif emotion.lower() == "angry":
        box_color = (0, 165, 255)  # cam
    else:
        box_color = (0, 255, 0)  

    # Vẽ khung quanh mặt
    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, box_color, 2)

    # Vẽ avatar nếu có
    avatar_path = os.path.join(AVATAR_DIR, f"{name}.jpg")
    if is_known and os.path.exists(avatar_path):
        avatar = cv2.imread(avatar_path)
        if avatar is not None:
            avatar = cv2.resize(avatar, (60, 60))
            x_avatar = max(x1 - 65, 0)
            y_avatar = max(y1, 0)
            frame[y_avatar:y_avatar+60, x_avatar:x_avatar+60] = avatar
