import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def process_image(image_path, destination_path):
    image = cv2.imread(image_path, 0)
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=3, minSize=(100, 100))

    if len(faces) > 0:
        x, y, w, h = faces[0]  # Consider only the first detected face
        face_img = image[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (128, 128))
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        cv2.imwrite(destination_path, face_resized)
    else:
        # Handle cases where no face is detected if needed
        pass


