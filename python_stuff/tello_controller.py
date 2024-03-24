# from djitellopy import Tello
# import cv2
# import json
# from audio import AudioModule
# import base64


# class TelloController:

#     def __init__(self) -> None:
#         self.audio_module = AudioModule()
#         self.tello = Tello()
#         self.tello.connect()
#         self.tello.streamon()
#         pass

#     def read_json(self, json_data: str) -> dict:
#         data = json.loads(json_data)
#         return data

#     def control_tello(self, json_data: str) -> str:

#         commands = self.read_json(json_data)["commands"]

#         for command in commands:
#             if (command["function"] == "takeoff") :
#                 self.audio_module.play("takeoff")
#                 self.tello.takeoff()
            
#             elif (command["function"] == "move"):
#                 amount = command["arguments"]["distance"]
#                 direction = command["arguments"]["direction"]

#                 self.audio_module.play_snippet(f"move_{direction}")
#                 self.tello.move(direction, amount)

#             elif (command["function"] == "land"):
#                 self.audio_module.play_snippet("land")
#                 self.tello.land()
#                 return "done"

#             elif (command["function"] == "rotate_clockwise"):
#                 self.audio_module.play_snippet("turn_left")
#                 degrees = command["arguments"]["degrees"]
#                 self.tello.rotate_clockwise(degrees)

#             elif (command["function"] == "rotate_counter_clockwise"):
#                 degrees = command["arguments"]["degrees"]
#                 self.audio_module.play_snippet("turn_right")
#                 self.tello.rotate_counter_clockwise(degrees)
            
#         return "continue"


#     def get_camera_frame(self):
#         img = self.tello.get_frame_read().frame
#         cv2.imshow("results", img)
#         return img
        

#     def get_camera_frame_base64(self):
#         img = self.get_camera_frame()
#         _, img_encoded = cv2.imencode('.jpg', img)
#         return base64.b64encode(img_encoded).decode('utf-8')
        
        

    
from djitellopy import tello
import cv2

me = tello.Tello()
#cap = cv2.VideoCapture(0)
me.connect()
print(me.get_battery())
me.streamon()


# while True:

for x in range(1000):
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    
    b, g, r = cv2.split(img)
    temp = b
    b = r
    r = temp
    img = cv2.merge((b, g, r))

    cv2.imshow("results", img)

cv2.imwrite("picture.png", img)


cv2.waitKey(1)
