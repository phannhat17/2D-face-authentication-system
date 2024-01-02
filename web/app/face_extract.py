import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def process_image(image_path):
    image = cv2.imread(image_path, 0)
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=3, minSize=(100, 100))

    if len(faces) > 0:
        x, y, w, h = faces[0]  # Consider only the first detected face
        face_img = image[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (128, 128))
        cv2.imwrite(image_path, face_resized)  # Overwrite the original image


