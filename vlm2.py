import cv2
import openai
import base64
import os
import subprocess
import time
import pyautogui

# Set your OpenAI API key


def start_kobuki_keyop():
    """Starts the kobuki-simple-keyop process in a new terminal."""
    process = subprocess.Popen(["gnome-terminal", "--", "kobuki-simple-keyop"])
    time.sleep(2)  # Wait for the process to initialize
    return process

def capture_image_from_astra():
    """Captures an image from Astra Pro camera using OpenCV and saves it."""
    cap = cv2.VideoCapture(0)  # Astra Pro should be detected as a webcam

    if not cap.isOpened():
        raise RuntimeError("Error: Could not open Astra Pro camera!")

    # Allow camera to warm up
    for _ in range(10):
        ret, frame = cap.read()

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to capture a frame from Astra Pro.")

    # Save the captured image
    image_path = "astra_capture.jpg"
    cv2.imwrite(image_path, frame)
    print(f"Image captured and saved as {image_path}")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

    return image_path

def encode_image(image_path):
    """Encodes an image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chatgpt_with_image(image_path, prompt):
    """Sends an image and a prompt to OpenAI's GPT-4 Turbo Vision model."""
    base64_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Latest model supporting vision
        messages=[
            {"role": "system", "content": "You are an AI that analyzes images."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=300
    )
    
    return response["choices"][0]["message"]["content"]
    

def send_keystroke(action):
    """Simulates a key press based on the action provided by ChatGPT."""
    key_map = {
        "forward": "up",
        "left": "left",
        "right": "right",
        "reverse": "down",
        "stop": "space"
    }

    if action in key_map:
        print(f"Simulating key press: {key_map[action]}")
        pyautogui.press(key_map[action])
    else:
        print("Invalid action received.")

if __name__ == "__main__":
    prompt = "Given the following image, provide a clear and concise action for the robot. The action should be one of the following: 'forward', 'stop', 'left', 'right', 'reverse', or 'continue'. The image will show the robot's current environment, and I need the most appropriate action to move the robot safely and correctly. If the image contains a man with glasses, blonde hair, and his mouth open, return 'stop'.  If the image contains a man with glasses, blonde hair, but his mouth is not open, return 'continue'. Only return the action as output without any explanation."
    
    try:
        # Start the Kobuki keyop process
        kobuki_process = start_kobuki_keyop()
        
        while True:
            # Capture image from Astra Pro
            image_path = capture_image_from_astra()

            if image_path:  # Proceed only if image capture was successful
                result = chatgpt_with_image(image_path, prompt)
                print("\nResponse from OpenAI:")
                print(result)

                # Simulate keystroke based on the response
                send_keystroke(result)
            else:
                print("Image capture failed. Skipping this iteration.")

            time.sleep(2)  # Wait for 2 seconds before repeating the loop
    
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
