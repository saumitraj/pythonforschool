import cv2
import numpy as np

# Load the cascade for hand detection
hand_cascade = cv2.CascadeClassifier('hand.xml')

# Access the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from video capture
    ret, frame = cap.read()

    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands in the frame
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in hands:
        # Draw a rectangle around the detected hand
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the region of interest
        roi = frame[y:y + h, x:x + w]

        # Convert to grayscale for better processing
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to create a binary image
        _, binary = cv2.threshold(gray_roi, 100, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the binary image
        cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Count the number of fingers (assumes each contour represents a finger)
        count = len(cnts)

        # Draw the count on the frame
        cv2.putText(frame, str(count), (x + w - 50, y + h + 10),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2)

    # Display the frame with hand and finger count
    cv2.imshow('Finger Counter', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
