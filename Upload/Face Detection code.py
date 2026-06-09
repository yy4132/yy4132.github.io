import cv2

# Load pre-trained cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load pre-trained cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect faces and apply feature blurring with adjusted eye detection parameters
def detect_and_blur(image, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30), blurKernelSize=(51, 51), eyeParams=None):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)

    # Iterate over detected faces
    for (x, y, w, h) in faces:
        # Draw a red bounding box around detected face
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Extract region of interest (ROI) corresponding to face
        face_roi = image[y:y+h, x:x+w]
        gray_roi = gray[y:y+h, x:x+w]

        # Perform eye detection within face region
        if eyeParams is not None:
            eyes = eye_cascade.detectMultiScale(gray_roi, **eyeParams)
        else:
            eyes = eye_cascade.detectMultiScale(gray_roi)

        # Iterate over detected eyes
        for (ex, ey, ew, eh) in eyes:
            # Blur eye region
            blurred_eye = cv2.GaussianBlur(face_roi[ey:ey+eh, ex:ex+ew], blurKernelSize, 0)

            # Replace original eye region with blurred eye
            face_roi[ey:ey+eh, ex:ex+ew] = blurred_eye

        # Replace original face region with modified face ROI
        image[y:y+h, x:x+w] = face_roi

    return image

# Load three images
image1 = cv2.imread(r"C:\Users\leeyj\Downloads\humanSubjectsA.jpg")
image2 = cv2.imread(r"C:\Users\leeyj\Downloads\humanSubjectsB.jpg")
image3 = cv2.imread(r"C:\Users\leeyj\Downloads\nonHumanSubject(civet).jpg")

# Set detection parameters for each image
parameters_image1 = {
    'scaleFactor': 1.3,
    'minNeighbors': 4,
    'minSize': (30, 30),
    'blurKernelSize': (41, 41),
    'eyeParams': {
        'scaleFactor': 1.1,
        'minNeighbors': 7,
        'minSize': (20, 20),
        'maxSize': (40, 40)
    }
}

parameters_image2 = {
    'scaleFactor': 1.3,
    'minNeighbors': 6,
    'minSize': (30, 30),
    'blurKernelSize': (41, 41),
    'eyeParams': {
        'scaleFactor': 1.1,
        'minNeighbors': 1,
        'minSize': (1, 1),
        'maxSize': (5, 5)
    }
}

# Perform face detection and feature blurring on each image with custom parameters
result1 = detect_and_blur(image1.copy(), **parameters_image1)
result2 = detect_and_blur(image2.copy(), **parameters_image2)
result3 = detect_and_blur(image3.copy())  # Use default parameters

# Display modified images
cv2.imshow('Upfront', result1)
cv2.imshow('Distant', result2)
cv2.imshow('Nonhuman', result3)
cv2.waitKey(0)
cv2.destroyAllWindows()