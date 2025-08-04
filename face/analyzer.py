from deepface import DeepFace

def analyze_face(face_crop):
    try:
        result = DeepFace.analyze(face_crop, actions=['emotion', 'age', 'gender'], enforce_detection=False)
        print("DeepFace result:", result)

        if isinstance(result, dict):
            dominant_emotion = result.get('dominant_emotion', 'Unknown')
            age = result.get('age', '?')

            gender_info = result.get('gender', 'Unknown')
            if isinstance(gender_info, dict):  # nếu là dict các xác suất
                gender = max(gender_info, key=gender_info.get)
            else:
                gender = gender_info

        # Trường hợp là list (DeepFace cũ hơn)
        elif isinstance(result, list) and len(result) > 0:
            dominant_emotion = result[0].get('dominant_emotion', 'Unknown')
            age = result[0].get('age', '?')

            gender_info = result[0].get('gender', 'Unknown')
            if isinstance(gender_info, dict):
                gender = max(gender_info, key=gender_info.get)
            else:
                gender = gender_info

        else:
            dominant_emotion, age, gender = 'Unknown', '?', 'Unknown'

        print(f"Emotion: {dominant_emotion} | Age: {age} | Gender: {gender}")
        return dominant_emotion, age, gender

    except Exception as e:
        print("DeepFace Error:", e)
        return "Unknown", "?", "Unknown"
