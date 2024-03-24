import base64
import openai
from config import OPENAI_KEY
import requests
import json


class GestureModule:
    def __init__(self):
        self.gesture = None
        self.client = openai.OpenAI(api_key=OPENAI_KEY)


    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    def process_frame(self, img_base64):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_KEY}"}

        prompt = f'''
        You are a controller for a gesture-controlled drone. Your job is to interpret images of gestures from the user and translate the text to commands that can be run on the drone.
                
        Please output the function that would make for the drone to satisfy the gesture command:

        your output should be only one string, with the function name, and arguments comma separated. For example, if you want to move the drone forward by 50 cm, you should output "move,forward,50"

        If the user is making an X with their arms, it means you should return "land"
        If the user has both hands up, it means you should return "takeoff"

        If the user is pointing up with one finger, you should return "move,forward,200".
        If the user is pointing down with one finger, you should return "move,back,200".

        If only the user's arm on the left side of the screen is held up, you should return rotate_counter_clockwise, 90.
        If only the user's arm on the right side of the screen is held up(from the perspective of the camera) is held up, you should return rotate_clockwise, 90.

        If there is no gesture recognized, you should output "null"

        please only output the one string, and nothing else
        '''
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"{prompt}"
                    },
                ]
            }
        ]
        response = self.client.chat.completions.create(
            model = "gpt-4-vision-preview",
            messages = messages,
        )
        str_response = response.choices[0].message.content
        print(str_response)
        print("-----------------")
        return str_response


    def run_gesture_step(self, filename):
        base64_image = self.encode_image(filename)
        response = self.process_frame(base64_image)
        print(response)
