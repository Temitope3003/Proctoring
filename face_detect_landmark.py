import cv2
import numpy as np
import dlib

# Function to convert dlib.full_object_detection to numpy array
def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

# Load the Dlib face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Users\PC\Desktop\Alusoft_proctoring\dlib\shape_predictor_68_face_landmarks.dat")

# Start capturing video from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to retrieve frame from the camera...")
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces using the Dlib face detector
    detected_boxes = detector(image_rgb)

    # Count the number of faces detected
    num_faces = len(detected_boxes)
    cv2.putText(frame, f"Number of Faces: {num_faces}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Loop through each detected face and draw rectangle around it
    for box in detected_boxes:
        cv2.rectangle(frame, (box.left(), box.top()), (box.right(), box.bottom()), (0, 255, 0), 3)

        # Predict facial landmarks
        landmarks = predictor(image_rgb, box)

        # Convert landmarks to numpy array
        points = shape_to_np(landmarks)

        # Loop through each landmark point and draw circle around it
        for (x, y) in points:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
