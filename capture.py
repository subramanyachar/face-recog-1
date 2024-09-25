import cv2
import os

def capture_face_images(name):
    # Open video capture
    cap = cv2.VideoCapture(0)

    # Create directory for storing images
    os.makedirs(f'dataset/{name}', exist_ok=True)

    count = 0
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    last_eye_state = False  # Track the last state of the eyes (open/closed)
    blink_threshold = 5  # Number of frames to consider as a blink
    blink_count = 0
    capturing = False  # Flag to indicate if we are in capturing mode

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Process each detected face
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Get the region of interest for eye detection
            roi_gray = gray[y:y + h, x:x + w]

            # Detect eyes within the face region
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 0:  # Eyes are closed
                blink_count += 1
                if blink_count >= blink_threshold and not last_eye_state:
                    # Start capturing images after a blink
                    capturing = True
                    last_eye_state = True  # Update last eye state
            else:  # Eyes are open
                if last_eye_state:  # Reset if eyes were last closed
                    last_eye_state = False
                    blink_count = 0  # Reset blink count

        # Capture images if in capturing mode
        if capturing:
            # Capture image
            count += 1
            cv2.imwrite(f'dataset/{name}/{name}_{count}.jpg', roi_gray)
            print(f'Image {count} captured!')

            # Stop capturing after 10 images
            if count >= 10:
                break

        # Show frame
        cv2.imshow('Capturing Faces', frame)

        # Break on 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

name = input("Enter the user Name: ")
# Capture images for a person
capture_face_images(name)
