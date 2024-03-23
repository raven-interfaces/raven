from voice import VoiceModule
from gesture import GestureModule


def main():

    gesture = GestureModule()
    gesture.run_gesture_step("test_files/test.jpeg")


    # voice = VoiceModule()
    # response = voice.run_voice_step()
    # print(response)




if __name__ == "__main__":
    main()