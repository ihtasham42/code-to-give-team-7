import cv2
import dlib
import numpy as np
import bz2

# Replace 'shape_predictor_68_face_landmarks.dat.bz2' with the actual file name.
input_file = r"C:\Users\Lenny\OneDrive - Nexus365\Documents\GitHub\code-to-give-team-7\image-detection-service\shape_predictor_68_face_landmarks.dat.bz2"
output_file = 'shape_predictor_68_face_landmarks.dat'  # Output file name

with bz2.BZ2File(input_file, 'rb') as source, open(output_file, 'wb') as dest:
    dest.write(source.read())

# Load the pre-trained face detection and facial landmark models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Open a video capture object
cap = cv2.VideoCapture("Head_tilt_test3.MOV")

#check if the video is opened
if not cap.isOpened():
    print("ERROR: Video couldn't be played")
else:
    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            # Extract the face region
            face_roi = frame[y:y + h, x:x + w]
            
            # Detect facial landmarks
            landmarks = predictor(gray, dlib.rectangle(x, y, x + w, y + h))
            
            if landmarks is not None:
                landmarks = landmarks.parts()
                
                # Define the key facial landmarks (e.g., eyes and nose)
                left_eye = landmarks[36:42]
                right_eye = landmarks[42:48]
                nose_bridge = landmarks[27:31]

                # Calculate the mean x and y coordinates separately for the left and right eye landmarks
                left_eye_mean_x = np.mean([point.x for point in left_eye])
                left_eye_mean_y = np.mean([point.y for point in left_eye])
                right_eye_mean_x = np.mean([point.x for point in right_eye])
                right_eye_mean_y = np.mean([point.y for point in right_eye])

                
                # Calculate the vertical distance between the eyes and nose
                d_y = nose_bridge[0].y - ((left_eye_mean_y + right_eye_mean_y) / 2)
                
                # Calculate the pitch angle using trigonometry
                angle = np.degrees(np.arctan2(d_y, w / 2))

                #If the calculated angle is less than -2, correlate that to up command
                # Display the pitch angle on the frame
                cv2.putText(frame, f'Input Command: {angle <= -2.00}', (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Display the frame with the pitch angle information
        cv2.imshow('Pitch Angle Estimation', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

#C:\Users\Lenny\OneDrive - Nexus365\Documents\GitHub\code-to-give-team-7\image-detection-service\main.py