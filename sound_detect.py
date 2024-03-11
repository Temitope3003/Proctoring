import pyaudio
import numpy as np
import keyboard

def detect_sound(threshold=50):
    # Define the audio stream parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Initialize PyAudio object and open the microphone stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Flag to indicate whether recording is in progress or not
    recording = True

    # Continuously read audio data from the microphone stream
    while recording:
        data = stream.read(CHUNK)
        # Convert the audio data to a numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Calculate the root mean square (RMS) of the audio signal
        rms = np.sqrt(np.mean(np.square(audio_data)))
        # Check if the RMS exceeds the threshold
        if rms > threshold:
            print(f"Sound detected {rms}")
        else:
            print("no sound detected")
        # Check for keypress to stop recording
        if keyboard.is_pressed('q'):
            recording = False

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Example usage
detect_sound()
