import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq, irfft
from scipy.io.wavfile import write

# параметры захвата звука с микрофона
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# создание объекта PyAudio для захвата звука
p = pyaudio.PyAudio()

# открытие потока захвата звука
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# создание фильтра для изменения тональности
def pitch_shift(signal, semitones):
    length = signal.shape[0]
    yf = rfft(signal)
    xf = rfftfreq(length, 1/RATE)

    if semitones > 0:
        for i in range(len(yf)):
            if i < len(yf)-int(2**(semitones/12)*1000):
                yf[-i-1] = yf[-i-int(2**(semitones/12)*1000)]
            else:
                yf[-i-1] = 0

    elif semitones < 0:
        for i in range(len(yf)):
            if i > int(2**(-semitones/12)*500):
                yf[i] = 0
            else:
                yf[i] = yf[i+int(2**(-semitones/12)*500)]

    new_sig = irfft(yf)
    norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
    return norm_new_sig

# запись измененного звука в файл
def write_to_file(data):
    write("modified.wav", RATE, data)

# запуск потока захвата звука и изменения тональности
while True:
    try:
        # чтение данных из потока захвата звука
        data = stream.read(CHUNK, exception_on_overflow=False)
        # преобразование байтовых данных в массив NumPy
        signal = np.frombuffer(data, dtype=np.int16)
        # изменение тональности звука на 2 полутона вверх
        shifted_signal = pitch_shift(signal, 2)
        # вывод измененного звука на колонки
        stream.write(shifted_signal.tobytes())
    except KeyboardInterrupt:
        break

# остановка потока захвата звука
stream.stop_stream