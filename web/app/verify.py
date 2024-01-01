from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, Conv2D, Dense, MaxPooling2D, Input, Flatten
import tensorflow as tf
import cv2
import os
import random
import numpy as np
from matplotlib import pyplot as plt


class L1Dist(Layer):
    
    # Init method - inheritance
    def __init__(self, **kwargs):
        super().__init__()
       
    # Magic happens here - similarity calculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)

siamese_model = tf.keras.models.load_model('siamesemodel.h5', 
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})


def preprocess(file_path):
    
    # Read in image from file path
    byte_img = tf.io.read_file(file_path)
    # Load in the image 
    img = tf.io.decode_png(byte_img, channels=1)
    
    # Preprocessing steps - resizing the image to be 100x100x3
    img = tf.image.resize(img, (100,100))
    # Scale image to be between 0 and 1 
    img = img / 255.0

    # Return image
    return img

def verify(valid_path, input_img_a, detection_threshold, verification_threshold):
    # Build results array
    results = []
    for image in os.listdir(valid_path):
        input_img = preprocess(input_img_a)
        validation_img = preprocess(os.path.join(valid_path, image))
        plt.subplot(1,2,1)
        plt.imshow(input_img, cmap='gray')

        # Set second subplot
        plt.subplot(1,2,2)
        plt.imshow(validation_img, cmap='gray')

        # Make Predictions 
        result = siamese_model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        results.append(result)
    
    # Detection Threshold: Metric above which a prediciton is considered positive 
    detection = np.sum(np.array(results) > detection_threshold)
    
    # Verification Threshold: Proportion of positive predictions / total positive samples 
    verification = detection / len(os.listdir(valid_path)) 
    verified = verification > verification_threshold
    
    return str(verified)