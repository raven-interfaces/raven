from voice import VoiceModule
from gesture import GestureModule
from tello_controller import TelloController
import sys
import cv2
import base64 
from trip_writer import write_to_trip, add_to_trip
import os
import time

# tello_controller = TelloController()

def main():
    # delete notes.txt and picture.png from trip folder
    if os.path.exists("trip/notes.txt"):
        os.remove("trip/notes.txt")

    if os.path.exists("trip/picture.jpg"):
        os.remove("trip/picture.jpg")


    modality_type = input("Enter modality type: ")
    if modality_type == "voice":
        voice = VoiceModule()

        while True:
            commands_json = voice.run_voice_step()
            print(commands_json)
            
            add_to_trip(f"```\n{commands_json}\n```")
            # run_commands(commands_json)
    
    elif modality_type == "gesture":
        gesture = GestureModule()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        
        past_time = 0
        while True:

            print("capturing frame")
            ret, frame = cap.read()
            # cv2.imshow('Webcam Feed', frame)

            current_time = time.time()

            file_name = "trip/picture.jpg"
            cv2.imwrite(file_name, frame)

            if current_time - past_time > 5:
                img_base64 = encode_img_base64(frame)
                commands_str = gesture.process_frame(img_base64)

                file_name_copy = "trip/picture_copy.jpg"
                cv2.imwrite(file_name_copy, frame)

                past_time = current_time

                commands_arr = commands_str.split(",")
                if "null" in commands_arr:
                    add_to_trip("```\nnull\n```")
                else:
                    method_name = commands_arr[0]
                    arguments = ",".join(commands_arr[1:])


                    add_to_trip(f"```\n{method_name}({arguments})\n```")

                print(commands_str)



            # time.sleep(5)

            cv2.waitKey(1)


            # run_commands_str(commands_str)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    

def run_commands(commands_json):
    status = tello_controller.control_tello(commands_json)
    if status == "done":
        print("Done")
        sys.exit(0)


def run_commands_str(commands_str):
    status = tello_controller.control_tello_string(commands_str)
    if status == "done":
        print("Done")
        sys.exit(0)


def encode_img_base64(img):
    _, img_encoded = cv2.imencode('.jpg', img)
    return base64.b64encode(img_encoded).decode('utf-8')


if __name__ == "__main__":
    main()