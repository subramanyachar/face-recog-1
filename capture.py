import cv2
import os


def capture_face_images(name):
    # Open video capture
    cap = cv2.VideoCapture(0)

    # Create directory for storing images
    os.makedirs(f'dataset/{name}', exist_ok=True)

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Save the detected face images
        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y + h, x:x + w]
            cv2.imwrite(f'dataset/{name}/{name}_{count}.jpg', face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Show frame
        cv2.imshow('Capturing Faces', frame)

        # Break on 'q' or after capturing 10 images
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 10:
            break

    cap.release()
    cv2.destroyAllWindows()


name = input("Enter the user Name")
# Capture images for a person
capture_face_images(name)
