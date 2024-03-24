from voice import VoiceModule
from gesture import GestureModule
from tello_controller import TelloController
import sys

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
        # gesture.run_gesture_step("test_files/test.jpeg")
        tello_controller.run_camera_buffer()
        while True:
            img = tello_controller.get_camera_frame()
            img_base64 = tello_controller.encode_img_base64(img)
            commands_str = gesture.process_frame(img_base64)
            print(commands_str)
            status = tello_controller.control_tello_string(commands_str)
            if status == "done":
                print("Done")
                sys.exit(0)


def run_commands(commands_json):
    status = tello_controller.control_tello(commands_json)
    if status == "done":
        print("Done")
        sys.exit(0)
        

    

if __name__ == "__main__":
    main()