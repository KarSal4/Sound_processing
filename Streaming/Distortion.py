import pyaudio 
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np


FORMAT = pyaudio.paInt16 # data type formate
CHANNELS = 1 # Adjust to your number of channels
RATE = 44100 # Sample Rate
CHUNK = 512 # Block Size
STREAM_SECONDS = 5 # Record time


audio = pyaudio.PyAudio()


in_stream = audio.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, 
                    input=True,
                    input_device_index=4, #< ----- Input index device
                    frames_per_buffer=CHUNK)
out_stream = audio.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, 
                    output=True,
                    input_device_index=1, #< ----- Output index device
                    frames_per_buffer=CHUNK)
print("Stream started")

def apply_distortion(input_signal, gain, threshold):


    distorted_signal = np.tanh(input_signal / threshold)
    return distorted_signal

def process_audio(input_data):

    input_signal = np.frombuffer(input_data, dtype=np.float32)

    distorted_signal = apply_distortion(input_signal, 1, 0.5)
    output_data = distorted_signal.tobytes()



    return (output_data, pyaudio.paContinue)

while(True):
    data = in_stream.read(CHUNK)
    signal = np.frombuffer(data, dtype=np.int16)

    distorted, a = process_audio(data)


    out_stream.write( distorted)
    
    

