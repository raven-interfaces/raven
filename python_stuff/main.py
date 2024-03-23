from voice import VoiceModule
# from gesture import GestureModule

from tello_controller import TelloController


def main():

    tello_controller = TelloController()

    gesture = GestureModule()
    # gesture.run_gesture_step("test_files/test.jpeg")


    # voice = VoiceModule()
    # response = voice.run_voice_step()
    # print(response) 

    # tello_controller.control_tello(response)

    tello_controller.get_camer_frame_base64()
    
    tello_controller.tello.stop()
    tello_controller.tello.land()


if __name__ == "__main__":
    main()