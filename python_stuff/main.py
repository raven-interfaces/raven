from voice import VoiceModule
from gesture import GestureModule
from tello_controller import TelloController
import sys
import cv2
import base64 

tello_controller = TelloController()

def main():
    modality_type = input("Enter modality type: ")
    if modality_type == "voice":
        voice = VoiceModule()

        while True:
            commands_json = voice.run_voice_step()
            print(commands_json)
            run_commands(commands_json)
    
    elif modality_type == "gesture":
        gesture = GestureModule()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        while True:
            ret, frame = cap.read()
            cv2.imshow('Webcam Feed', frame)
            img_base64 = encode_img_base64(frame)
            commands_str = gesture.process_frame(img_base64)
            print(commands_str)
            run_commands_str(commands_str)

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