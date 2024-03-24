import base64
import openai
from config import OPENAI_KEY
import requests


class GestureModule:
    def __init__(self):
        self.gesture = None
        self.client = openai.OpenAI(api_key=OPENAI_KEY)


    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    def process_frame(self, base64_image):
        

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_KEY}"}

        prompt = f'''
        You are a controller for a gesture-controlled drone. Your job is to interpret images of gestures from the user and translate the text to commands that can be run on the drone.


        You can run the following commands on the done:

        def flip( direction: str = "f"):
                """Flips the drone in the given direction.
                
                Args:
                    direction (str): Direction to flip. Options: "l" (left), "r" (right), 
                                    "f" (forward, default), "b" (backward).
                """

            def move(direction: str = "forward", distance: int = 50):
                """
                Moves the drone in the specified direction by a certain distance.
                
                Args:
                    direction (str): Direction to move. Options: "left", "right", "forward" (default), "backward", "up", "down".
                    distance (int): Distance to move in centimeters. Range: 20 to 500 (default 50).
                """

            def land():
                """Lands the drone automatically."""

            def rotate_clockwise(degrees: int = 90):
                """
                Rotates the drone clockwise by a specified number of degrees.
                
                Args:
                    degrees (int): Degrees to rotate. Range: 0 to 360 (default 90).
                """

            def rotate_counter_clockwise(degrees: int = 90):
                """
                Rotates the drone counter-clockwise by a specified number of degrees.
                
                Args:
                    degrees (int): Degrees to rotate. Range: 0 to 360 (default 90).
                """


        Please a function call (and associated arguments) in JSON that you would make for the drone to satisfy following gesture commands:

        If the user is holding their palm facing towards you, it means you should terminate the flight and land using the land() method.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

        If the user is pointing with one finger, it means you should use the move() function to move in the direction the user is pointing.
        If the user is pointing up with one finger, the direction should be up.
        If the user is pointing down with one finger, the direction should be down.
        If the user is pointing left with one finger, the direction should be left.
        If the user is pointing right with one finger, the direction should be right.
        If the user is pointing towards the camera with one finger, the direction should be backward.
        If the user is pointing directly away (towards themselves) with one finger, the direction should be forward.

        
        If the user is pointing with with three fingers, it means you should turn in the direction the user is pointing.
        If the user is pointing with three fingers to the right, the direction should be clockwise.
        If the user is pointing with three fingers to the left, the direction should be counter-clockwise.
        
        If the user is making a dab dance move motion, it means you should do a forward flip.
        
        Please also ensure that the JSON is structured in the following form:

        "commands": [
            {{
            "function": "move",
            "arguments": {{
                "direction": "forward",
                "distance": 50
            }}
            }}, ... ]

        Don't include anything in your response except for the json object.
        '''

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"{prompt}"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 300
        }


        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()

    
    def run_gesture_step(self, filename):
        base64_image = self.encode_image(filename)
        response = self.process_frame(base64_image)
        print(response)
