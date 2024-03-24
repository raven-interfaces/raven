from djitellopy import Tello
import cv2
import json
from audio import AudioModule
import base64
import time


class TelloController:

    def __init__(self) -> None:
        self.audio_module = AudioModule()
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()
        self.img_count = 0
        pass

    def read_json(self, json_data: str) -> dict:
        data = json.loads(json_data)
        return data

    def control_tello(self, json_data: str) -> str:

        commands = self.read_json(json_data)["commands"]

        for command in commands:
            if (command["function"] == "takeoff") :
                self.audio_module.play_snippet("takeoff")
                self.tello.takeoff()
            
            elif (command["function"] == "move"):
                amount = command["arguments"]["distance"]
                direction = command["arguments"]["direction"]

                self.audio_module.play_snippet(f"move_{direction}")
                self.tello.move(direction, amount)

            elif (command["function"] == "land"):
                self.audio_module.play_snippet("land")
                self.tello.land()
                return "done"
            
            elif (command["function"] == "flip"):
                direction = command["arguments"]["direction"]

                if direction == "f":
                    self.audio_module.play_snippet("flip_forward")
                elif direction == "b":
                    self.audio_module.play_snippet("flip_backward")
                elif direction == "l":
                    self.audio_module.play_snippet("flip_left")
                elif direction == "r":
                    self.audio_module.play_snippet("flip_right")
                self.tello.flip(direction)

            elif (command["function"] == "rotate_clockwise"):
                self.audio_module.play_snippet("turn_left")
                degrees = command["arguments"]["degrees"]
                self.tello.rotate_clockwise(degrees)

            elif (command["function"] == "rotate_counter_clockwise"):
                degrees = command["arguments"]["degrees"]
                self.audio_module.play_snippet("turn_right")
                self.tello.rotate_counter_clockwise(degrees)


            time.sleep(1)
            
        return "continue"



    def control_tello_string(self, command_str: str) -> str:
        command_str = command_str.strip()
        command_list = [item.strip() for item in command_str.split(',')]

        if command_list[0] == "takeoff":
            self.audio_module.play_snippet("takeoff")
            self.tello.takeoff()

        elif command_list[0] == "move":
            amount = command_list[1]
            direction = command_list[2]
            self.audio_module.play_snippet(f"move_{direction}")
            self.tello.move(direction, amount)

        elif command_list[0] == "land":
            self.audio_module.play_snippet("land")
            self.tello.land()
            return "done"

        elif command_list[0] == "rotate_clockwise":
            degrees = command_list[1]
            self.audio_module.play_snippet("turn_right")
            self.tello.rotate_counter_clockwise(degrees)

        elif command_list[0] == "rotate_counter_clockwise":
            degrees = command_list[1]
            self.audio_module.play_snippet("turn_right")
            self.tello.rotate_counter_clockwise(degrees)

        time.sleep(1)
            
        return "continue"
    


    def run_camera_buffer(self):
        for i in range(1000):
            self.tello.get_frame_read().frame


    def get_camera_frame(self):
        img = self.tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        b, g, r = cv2.split(img)
        temp = b
        b = r
        r = temp
        img = cv2.merge((b, g, r))
        file_name = "images/picture" + str(self.img_count) + ".png"
        self.img_count += 1
        cv2.imwrite("file_name", img)
        return img

    
    def encode_img_base64(self, img):
        _, img_encoded = cv2.imencode('.jpg', img)
        return base64.b64encode(img_encoded).decode('utf-8')

        

    # def get_camera_frame_base64(self):
    #     img = self.get_camera_frame()
    #     _, img_encoded = cv2.imencode('.jpg', img)
    #     return base64.b64encode(img_encoded).decode('utf-8')
        
        

    
# from djitellopy import tello
# import cv2

# me = tello.Tello()
# #cap = cv2.VideoCapture(0)
# me.connect()
# print(me.get_battery())
# me.streamon()


# # while True:

# for x in range(1000):
#     img = me.get_frame_read().frame
#     img = cv2.resize(img, (360, 240))
    
#     b, g, r = cv2.split(img)
#     temp = b
#     b = r
#     r = temp
#     img = cv2.merge((b, g, r))

#     cv2.imshow("results", img)

# cv2.imwrite("picture.png", img)


# cv2.waitKey(1)
