import csv, os
from datetime import datetime

def log_detection(name, emotion, age, gender, path="app/data/detections.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ['timestamp', 'name', 'emotion', 'age', 'gender']
    write_header = not os.path.exists(path)

    with open(path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(header)
        writer.writerow([now, name, emotion, age, gender])
    print(f"[LOG] {now} | {name} | {emotion} | {age}, {gender}")
