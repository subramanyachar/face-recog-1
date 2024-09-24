import cv2
import numpy as np
import os


# Function to load images and labels for training
def load_training_data():
    faces = []
    labels = []
    label_id = 0
    label_map = {}

    dataset_dir = 'dataset'
    for person in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, person)
        for image_file in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_file)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            labels.append(label_id)

        label_map[label_id] = person
        label_id += 1

    return faces, labels, label_map


# Load training data
faces, labels, label_map = load_training_data()

# Train the LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

# Save the trained model
recognizer.save("face_trainer.yml")
