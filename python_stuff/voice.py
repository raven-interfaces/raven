import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from config import *
import os
import tempfile
import pygame
import threading
from trip_writer import write_to_trip, add_to_trip

client = OpenAI(api_key=OPENAI_KEY)

class VoiceModule:
    def __init__(self):
        self.recording = None
        self.fs = 44100  # Sample rate
        self.is_recording = False
        self.record_thread = None

    def start_recording(self):
        print("Recording started... Press any key to stop.")
        self.recording = sd.rec(int(10 * self.fs), samplerate=self.fs, channels=1, dtype='float64', blocking=False)
        self.is_recording = True

    def stop_recording(self):
        self.is_recording = False
        sd.stop()
        pygame.quit()
        print("Recording finished")

    def record_audio(self):
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption("Press any key to start recording")

        print("Waiting for keypress to start recording...")
        waiting_for_start = True  # Initialize the variable before the loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if waiting_for_start:
                        self.start_recording()
                        waiting_for_start = False  # Change its value after starting the recording
                    else:
                        self.stop_recording()
                        running = False
                elif event.type == pygame.QUIT:
                    running = False
                    if not waiting_for_start:  # Ensure recording is stopped only if it has started
                        self.stop_recording()
        pygame.quit()


    def monitor_pygame_events(self):
        while self.is_recording:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.stop_recording()
                    return
            sd.sleep(100)  # Check for events periodically


    def save_recording(self, filename='recording.wav'):
        if self.recording is not None:
            write(filename, self.fs, self.recording)


    def record_and_transcribe(self):
        self.record_audio()
        with tempfile.NamedTemporaryFile(suffix='.wav') as tmpfile:
            self.save_recording(filename=tmpfile.name)
            with open(tmpfile.name, 'rb') as audio_file:
                # Ensure you have a way to define or import `client`
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )

        write_to_trip(f"## Voice Mode")
        add_to_trip(f"```{transcription.text}```")

        return transcription
               

            # Assume transcription logic here



    # # Adjusted to record mono audio
    # def record_audio(self, duration=3, fs=44100):
    #     print("Recording...")
    #     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    #     sd.wait()  # Wait until recording is finished
    #     print("Recording finished")
    #     return recording, fs

    # # Save recording to a WAV file
    # def save_recording(self, recording, fs, filename='recording.wav'):
    #     write(filename, fs, recording)  # Save as WAV file

    # Main function to record and transcribe
    # def record_and_transcribe(self):
    #         # Record audio
    #         self.record_audio()
            
    #         # Use a temporary file to avoid manual cleanup
    #         with tempfile.NamedTemporaryFile(suffix='.wav') as tmpfile:
    #             self.save_recording(filename=tmpfile.name)
    

    # def transcribe(self):
    #     with open('output.wav', 'rb') as f:
    #         transcription = client.audio.transcriptions.create(
    #             model="whisper-1", 
    #             file=f
    #         )
    #     return transcription
        
        # # Use a temporary file to avoid manual cleanup
        # with tempfile.NamedTemporaryFile(suffix='.wav') as tmpfile:
        #     self.save_recording(recording, fs, filename=tmpfile.name)


        #     # Open the temporary file in 'rb' mode for transcription
        #     with open(tmpfile.name, 'rb') as audio_file:
        #         transcription = client.audio.transcriptions.create(
        #             model="whisper-1", 
        #             file=audio_file
        #         )
        #         return transcription
    


    def run_voice_step(self):

        # fetch audio from stream
        # self.vad_module.run()

        # Ensure you have configured your OpenAI client before calling this
        # transcription = self.record_and_transcribe(10)
        transcription = self.record_and_transcribe()

        print(transcription)
        speech_commands = transcription.text

        prompt = f'''
        You are a controller for a voice-controlled drone. Your job is to interpret transcriptions of speech from the user and translate the text to commands that can be run on the drone.

        You can run the following commands on the done:

        def flip(self, direction: str = "f"):
                """Flips the drone in the given direction.
                
                Args:
                    direction (str): Direction to flip. Options: "l" (left), "r" (right), 
                                    "f" (forward, default), "b" (back).
                """

            def move(self, direction: str = "forward", distance: int = 50):
                """
                Moves the drone in the specified direction by a certain distance.
                
                Args:
                    direction (str): Direction to move. Options: "left", "right", "forward" (default), "back", "up", "down".
                    distance (int): Distance to move in centimeters. Range: 20 to 500 (default 50).
                """

            def land(self):
                """Lands the drone automatically."""


            def takeoff(self):
                """Takes off the drone automatically."""

                
            def rotate_clockwise(self, degrees: int = 90):
                """
                Rotates the drone clockwise by a specified number of degrees.
                
                Args:
                    degrees (int): Degrees to rotate. Range: 0 to 360 (default 90).
                """

            def rotate_counter_clockwise(self, degrees: int = 90):
                """
                Rotates the drone counter-clockwise by a specified number of degrees.
                
                Args:
                    degrees (int): Degrees to rotate. Range: 0 to 360 (default 90).
                """


        Please return a list of function calls (and associated arguments) in JSON that you would make for the drone to satisfy following speech commands:
        
        To turn left, use rotate_counter_clockwise()
        
        To turn right, use rotate_clockwise().
        
        {speech_commands}

        Please also ensure that the JSON is structured in the following form:

        
    "commands": [
        {{
        "function": "move",
        "arguments": {{
            "direction": "forward",
            "distance": 50
        }}
        }}, ... ]

        '''

        response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={ "type": "json_object" },
        messages=[
            # {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"{prompt}"}
        ]
        )


        return response.choices[0].message.content
