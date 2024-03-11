import pyaudio
import numpy as np
import wave
import datetime

def record_sound(filename_prefix, exam_duration, threshold=50):
    # Define the audio stream parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Initialize PyAudio object and open the microphone stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Flag to indicate whether recording is in progress or not
    recording = False
    frames = []

    # Get current timestamp
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=exam_duration)

    # Continuously read audio data from the microphone stream
    while datetime.datetime.now() < end_time:
        data = stream.read(CHUNK)
        frames.append(data)
        # Convert the audio data to a numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Calculate the root mean square (RMS) of the audio signal
        rms = np.sqrt(np.mean(np.square(audio_data)))
        # Check if the RMS exceeds the threshold
        if rms > threshold:
            if not recording:
                print("Recording started.")
                recording = True
        elif recording:
            print("Recording stopped.")
            recording = False
            frames = []  # Clear frames when silent

    # If there were frames recorded during the exam, save them to a WAV file
    if frames:
        # Construct the filename with timestamp
        timestamp = start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Audio saved to {filename}")

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Example usage:
record_sound("exam_recording", exam_duration=60, threshold=50)  # Record sound for 10 minutes (600 seconds) during the exam
