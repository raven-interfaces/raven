from djitellopy import tello
import cv2

import json


class TelloController:

    def __init__(self) -> None:
        pass

    def read_json(self, json_data: str) -> dict:
        data = json.loads(json_data)
        return data

    def control_tello(self, json_data: str):

        commands = self.read_json(json_data)["commands"]

        for command in commands:
            if (command["function"] == "takeoff") :
                tello.takeoff()

            elif (command["function"] == "move"):
                amount = command["arguments"]["distance"]
                direction = command["arguments"]["direction"]
                tello.move(direction, amount)

            elif (command["function"] == "land"):
                tello.land()

            elif (command["function"] == "rotate_clockwise"):
                degrees = command["arguments"]["degrees"]
                tello.rotate_clockwise(degrees)

            elif (command["function"] == "rotate_counter_clockwise"):
                degrees = command["arguments"]["degrees"]
                tello.rotate_counter_clockwise(degrees)

    def land(self):
        tello.land()

    def stop(self):
        tello.stop()

    def emergency(self):
        tello.emergency()

    
# me = tello.Tello()
# #cap = cv2.VideoCapture(0)
# me.connect()
# print(me.get_battery())
# me.streamon()


# while True:
#     img = me.get_frame_read().frame
#     img = cv2.resize(img, (360, 240))
#     cv2.imshow("results", img)
#     cv2.waitKey(1)