from djitellopy import Tello
import cv2
import json
from audio import AudioModule


class TelloController:

    def __init__(self) -> None:
        self.audio_module = AudioModule()
        self.tello = Tello()
        self.tello.connect()
        pass

    def read_json(self, json_data: str) -> dict:
        data = json.loads(json_data)
        return data

    def control_tello(self, json_data: str):

        commands = self.read_json(json_data)["commands"]

        for command in commands:
            if (command["function"] == "takeoff") :
                self.audio_module.play("takeoff")
                self.tello.takeoff()
            
            elif (command["function"] == "move"):
                amount = command["arguments"]["distance"]
                direction = command["arguments"]["direction"]

                self.audio_module.play_snippet(f"move_{direction}")
                self.tello.move(direction, amount)

            elif (command["function"] == "land"):
                self.audio_module.play_snippet("land")
                self.tello.land()

            elif (command["function"] == "rotate_clockwise"):
                self.audio_module.play_snippet("turn_left")
                degrees = command["arguments"]["degrees"]
                self.tello.rotate_clockwise(degrees)

            elif (command["function"] == "rotate_counter_clockwise"):
                degrees = command["arguments"]["degrees"]
                self.audio_module.play_snippet("turn_right")
                self.tello.rotate_counter_clockwise(degrees)

    def land(self):
        self.tello.land()

    def stop(self):
        self.tello.stop()

    def emergency(self):
        self.tello.emergency()

    
# me = self.tello.Tello()
# #cap = cv2.VideoCapture(0)
# me.connect()
# print(me.get_battery())
# me.streamon()


# while True:
#     img = me.get_frame_read().frame
#     img = cv2.resize(img, (360, 240))
#     cv2.imshow("results", img)
#     cv2.waitKey(1)