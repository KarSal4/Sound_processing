import pyaudio 

FORMAT = pyaudio.paInt16 # data type formate
CHANNELS = 1 # Adjust to your number of channels
RATE = 22010 # Sample Rate
CHUNK = 256 # Block Size
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

    out_stream.write(data)