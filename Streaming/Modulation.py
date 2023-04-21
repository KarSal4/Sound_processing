import pyaudio 
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np


FORMAT = pyaudio.paInt16 # data type formate
CHANNELS = 1 # Adjust to your number of channels
RATE = 44100 # Sample Rate
CHUNK = 1024 # Block Size
STREAM_SECONDS = 5 # Record time


audio = pyaudio.PyAudio()

in_stream = audio.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, 
                    input=True,
                    input_device_index=1, #< ----- Input index device
                    frames_per_buffer=CHUNK)
out_stream = audio.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, 
                    output=True,
                    input_device_index=2, #< ----- Output index device
                    frames_per_buffer=CHUNK)
print("Stream started")



while(True):
    data = in_stream.read(CHUNK)
    signal = np.frombuffer(data, dtype=np.int16)

    length = signal.shape[0]
    yf = rfft(signal)
    xf = rfftfreq(length, 1/RATE)

    for i in range(len(yf)):
            if i > len(yf)-50:
                yf[i] = 0
            else:
                yf[i] =  yf[i+49]
    
    new_sig = irfft(yf)
    norm_new_sig = np.int16(new_sig * (3200 / new_sig.max()))
    out_stream.write(norm_new_sig.tobytes())
    
    

