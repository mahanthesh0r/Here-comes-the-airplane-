import face_alignment
from skimage import io
import cv2
import numpy as np

# Load face alignment model
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False, device='cpu')

# Read the image
image_path = 'astra_capture.jpg'
input_image = io.imread(image_path)

# Get facial landmarks
preds = fa.get_landmarks(input_image)

# Convert image to BGR (since OpenCV uses BGR format)
image_bgr = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)

# Draw landmarks
if preds is not None:
    for landmarks in preds:
        for (x, y) in landmarks:
            cv2.circle(image_bgr, (int(x), int(y)), 2, (0, 255, 0), -1)  # Green dots

# Save the output image
output_path = 'aflw-test-landmarks.jpg'
cv2.imwrite(output_path, image_bgr)

print(f"Saved image with landmarks at {output_path}")
