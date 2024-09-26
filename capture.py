import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import cv2
from datetime import datetime, timedelta


# Function to capture face images
def capture_face_images(name):
    # Open video capture
    cap = cv2.VideoCapture(0)

    # Create directory for storing images
    os.makedirs(f'dataset/{name}', exist_ok=True)

    start_time = datetime.now()

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

        current_time = datetime.now()
        elapsed_time = current_time - start_time

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

            if not capturing:
                if elapsed_time > timedelta(seconds=10):
                    capturing = True
                else:
                    print(elapsed_time)

        # Capture images if in capturing mode
        if capturing:
            # Capture image
            count += 1
            cv2.imwrite(f'dataset/{name}/{name}_{count}.jpg', roi_gray)
            print(f'Image {count} captured!')

            # Stop capturing after 30 images
            if count >= 30:
                break

        # Show frame
        cv2.imshow('Capturing Faces', frame)

        # Break on 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Function to open a new window for capturing images
def open_capture_window():
    # Create a new window for capturing images
    capture_window = tk.Toplevel(root)
    capture_window.title("Capture Images")
    capture_window.geometry("300x150")

    # Label and entry for the name
    name_label = tk.Label(capture_window, text="Enter Name:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(capture_window, width=30)
    name_entry.pack(pady=5)

    # Function to capture images when button is clicked
    def capture_images():
        name = name_entry.get().strip()  # Get the name from the entry widget

        if not name:  # Check if the name is empty
            messagebox.showwarning("Input Error", "Please enter a name.")
            return

        try:
            # Call the function to capture images with the entered name
            capture_face_images(name)
            messagebox.showinfo("Success", f"Images captured successfully for {name}!")
            capture_window.destroy()  # Close the capture window after success
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture images: {e}")

    # Create and place the capture button in the new window
    capture_button = tk.Button(capture_window, text="Capture", command=capture_images)
    capture_button.pack(pady=20)


# Function to train the model
def train_model():
    try:
        # This will execute the training script using subprocess
        subprocess.run(['python', 'train.py'])
        messagebox.showinfo("Success", "Model trained successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to train the model: {e}")


# Function to mark attendance
def take_attendance():
    try:
        # This will execute the take_attendance script using subprocess
        subprocess.run(['python', 'take_attendance.py'])
        messagebox.showinfo("Success", "Attendance marked successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to mark attendance: {e}")


# Function to view the attendance CSV
def view_attendance():
    if os.path.exists('attendance.csv'):
        os.system('start excel attendance.csv')  # For Windows to open CSV in Excel
    else:
        messagebox.showinfo("Error", "Attendance file not found!")


root = tk.Tk()
root.title("Face Recognition Attendance System")

root.geometry("400x300")

capture_button = tk.Button(root, text="Capture Images", width=25, command=open_capture_window)
capture_button.pack(pady=20)

train_button = tk.Button(root, text="Train Model", width=25, command=train_model)
train_button.pack(pady=20)

attendance_button = tk.Button(root, text="Mark Attendance", width=25, command=take_attendance)
attendance_button.pack(pady=20)

view_button = tk.Button(root, text="View Attendance", width=25, command=view_attendance)
view_button.pack(pady=20)

root.mainloop()
