import cv2
import requests
from HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math
import time

# Server URL where the video feed is hosted
video_feed_url = 'http://127.0.0.1:8001/video_feed'

# URL of the server or site where you want to send the translated text
output_server_url = 'http://127.0.0.1:5001/output'

cap = cv2.VideoCapture(video_feed_url)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

labels = ["I'm Fine", "I Love You", "4", "Victory", "Why"]

# Initialize previous prediction to None
prev_prediction = None

# Set the delay time (in seconds) before accepting a new prediction
delay_time = 2.0
last_prediction_time = time.time()

while True:
    # Get video frame from the server
    success, img = cap.read()
    imgOutput = img.copy()

    hands, img = detector.findHands(img)
    
    # Rest of your code remains the same
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)


        # Check for changes in prediction
        current_time = time.time()
        if prediction != prev_prediction and current_time - last_prediction_time >= delay_time:
            print(f"Detected sign: {labels[index]}")

            # Send translated text to another server or site
            translated_text = labels[index]

            requests.post(output_server_url, data={'text': translated_text})

            prev_prediction = prediction
            last_prediction_time = current_time

    # Rest of your code remains the same
