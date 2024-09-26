import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Function to capture images
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
        name = name_entry.get()  # Get the name from the entry widget
        if not name.strip():  # Check if the name is empty
            messagebox.showwarning("Input Error", "Please enter a name.")
            return

        try:
            # This will execute the capture script with the name argument using subprocess
            subprocess.run(['python', 'capture.py', name])
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

# Initialize the main window
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Set the window size
root.geometry("400x300")

# Create and place buttons
capture_button = tk.Button(root, text="Capture Images", width=25, command=open_capture_window)
capture_button.pack(pady=20)

train_button = tk.Button(root, text="Train Model", width=25, command=train_model)
train_button.pack(pady=20)

attendance_button = tk.Button(root, text="Mark Attendance", width=25, command=take_attendance)
attendance_button.pack(pady=20)

view_button = tk.Button(root, text="View Attendance", width=25, command=view_attendance)
view_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
