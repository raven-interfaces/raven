import numpy as np
import torch
import pyaudio
import wave
import io
import time


# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4000  # Samples per frame

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Load Silero VAD model
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=False)

(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

# Initialize buffer and timing
audio_buffer = io.BytesIO()
last_speech_time = time.time()
streaming = True  # Flag to control the streaming

class VADModule():

    def __init__(self):
        pass

    def save_buffer_to_file(self, buffer, filename="output.wav"):
        """Saves the content of the buffer to a file."""
        buffer.seek(0)
        with wave.open(filename, "wb") as wave_file:
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(audio.get_sample_size(FORMAT))
            wave_file.setframerate(RATE)
            wave_file.writeframes(buffer.getvalue())
        print(f"Saved: {filename}")


    def process_audio(self, in_data, frame_count, time_info, status):
        global audio_buffer, last_speech_time, streaming
        signal = np.frombuffer(in_data, dtype=np.int16)
        speech_prob = model(torch.tensor(signal).float(), RATE).item()

        if speech_prob > 0.9:  # Adjust threshold as needed
            audio_buffer.write(in_data)
            last_speech_time = time.time()
        else:
            current_time = time.time()
            if current_time - last_speech_time >= 1.5 and audio_buffer.getbuffer().nbytes > 0:
                # Save buffer to file and stop streaming after the first silence period is detected
                filename = f"output.wav"
                self.save_buffer_to_file(audio_buffer, filename)
                streaming = False  # Set flag to false to stop streaming
                return (None, pyaudio.paComplete)  # Stop processing audio
        return (in_data, pyaudio.paContinue)


    def run(self):
        # Open the stream with the callback
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=self.process_audio)

        print("Recording... Press Ctrl+C to stop.")
        stream.start_stream()

        # Keep the stream open until you want to stop recording or until streaming flag is False
        try:
            while stream.is_active() and streaming:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            # Terminate the PyAudio session
            audio.terminate()
            print("Recording stopped.")




vad_module = VADModule()
vad_module.run()