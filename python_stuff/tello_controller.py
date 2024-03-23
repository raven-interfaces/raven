from djitellopy import Tello
import cv2
import json
import base64


class TelloController:

    def __init__(self) -> None:
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()
        pass

    def read_json(self, json_data: str) -> dict:
        data = json.loads(json_data)
        return data

    def control_tello(self, json_data: str):

        commands = self.read_json(json_data)["commands"]

        for command in commands:
            if (command["function"] == "takeoff") :
                self.tello.takeoff()

            elif (command["function"] == "move"):
                amount = command["arguments"]["distance"]
                direction = command["arguments"]["direction"]
                self.tello.move(direction, amount)

            elif (command["function"] == "land"):
                self.tello.land()

            elif (command["function"] == "rotate_clockwise"):
                degrees = command["arguments"]["degrees"]
                self.tello.rotate_clockwise(degrees)

            elif (command["function"] == "rotate_counter_clockwise"):
                degrees = command["arguments"]["degrees"]
                self.tello.rotate_counter_clockwise(degrees)

    def get_camera_frame(self):
        img = self.tello.get_frame_read().frame
        cv2.imshow("results", img)
        return img
        

    def get_camer_frame_base64(self):
        img = self.get_camera_frame()
        _, img_encoded = cv2.imencode('.jpg', img)
        return base64.b64encode(img_encoded).decode('utf-8')
        
        

    
# me = self.tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamon()

# while True:
#     img = me.get_frame_read().frame
#     img = cv2.resize(img, (360, 240))
#     cv2.imshow("results", img)
#     cv2.waitKey(1)