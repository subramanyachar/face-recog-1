import cv2
import pandas as pd
from datetime import datetime

from train import label_map


def mark_attendance(name):
    """Marks attendance in an Excel or CSV file."""
    now = datetime.now()
    time_string = now.strftime('%H:%M:%S')
    date_string = now.strftime('%d-%m-%Y')

    # Load or create the attendance file
    try:
        df = pd.read_csv('attendance.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Date', 'Time'])

    # Check if the person has already been marked for the day
    if not ((df['Name'] == name) & (df['Date'] == date_string)).any():
        new_entry = pd.DataFrame([[name, date_string, time_string]], columns=['Name', 'Date', 'Time'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv('attendance.csv', index=False)


# Load the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_trainer.yml")

# Load the face cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]

        # Recognize the face
        label, confidence = recognizer.predict(face)
        name = label_map.get(label, "Unknown")

        # Mark attendance if confidence is above a certain threshold
        if confidence < 60:
            mark_attendance(name)
            cv2.putText(frame, f'{name} ({confidence:.2f})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Attendance System', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

