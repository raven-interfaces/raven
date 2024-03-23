import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from openai import OpenAI
from config import *

client = OpenAI(api_key=OPENAI_KEY)

class VoiceModule:
    def __init__(self):
        pass

    # Adjusted to record mono audio
    def record_audio(self, duration=3, fs=44100):
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()  # Wait until recording is finished
        print("Recording finished")
        return recording, fs

    # Save recording to a WAV file
    def save_recording(self, recording, fs, filename='recording.wav'):
        write(filename, fs, recording)  # Save as WAV file

    # Main function to record and transcribe
    def record_and_transcribe(self, duration=3):
        # Record audio
        recording, fs = self.record_audio(duration=duration)
        
        # Use a temporary file to avoid manual cleanup
        with tempfile.NamedTemporaryFile(suffix='.wav') as tmpfile:
            self.save_recording(recording, fs, filename=tmpfile.name)


            # Open the temporary file in 'rb' mode for transcription
            with open(tmpfile.name, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                return transcription
    
    
    def run_voice_step(self):
        # Ensure you have configured your OpenAI client before calling this
        transcription = self.record_and_transcribe(10)

        speech_commands = transcription.text

        prompt = f'''
        You are a controller for a voice-controlled drone. Your job is to interpret transcriptions of speech from the user and translate the text to commands that can be run on the drone.

        You can run the following commands on the done:

        def flip(self, direction: str = "f"):
                """Flips the drone in the given direction.
                
                Args:
                    direction (str): Direction to flip. Options: "l" (left), "r" (right), 
                                    "f" (forward, default), "b" (backward).
                """

            def move(self, direction: str = "forward", distance: int = 50):
                """
                Moves the drone in the specified direction by a certain distance.
                
                Args:
                    direction (str): Direction to move. Options: "left", "right", "forward" (default), "backward", "up", "down".
                    distance (int): Distance to move in centimeters. Range: 20 to 500 (default 50).
                """

            def land(self):
                """Lands the drone automatically."""

                
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
        
        Note: To turn left, use rotate_counter_clockwise() and to turn right, use rotate_clockwise().
        
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
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            # {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"{prompt}"}
        ]
        )


        return response.choices[0].message.content



# print(transcription)
# print(transcription.text)