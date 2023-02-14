import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.io.wavfile import write, read

# Создание сигнала
SAMPLE_RATE = 44100  # (Гц)(частота дискретизации) 
DURATION = 2  # (Секунды)длина сгенерированной выборки.

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x * freq
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Генерируем волны с частотой 400 Гц и 4000 Гц, длительностью 5 секунд

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)

noise_tone = noise_tone * 0.3
mixed_tone = nice_tone + noise_tone

# Сгенерированный сигнал с шумом
normalized_tone = np.int16((nice_tone / nice_tone.max()) * 32767)
plt.plot(normalized_tone[:1000])
plt.show()

write("mysinewave.wav", SAMPLE_RATE, normalized_tone)
playsound('mysinewave.wav')

# число точек в normalized_tone
N = SAMPLE_RATE * DURATION

yf = rfft(normalized_tone)
xf = rfftfreq(N, 1/SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()

# Максимальная частота составляет половину частоты дискретизации
points_per_freq = len(xf) / (SAMPLE_RATE / 2)

# Наша целевая частота - 4000 Гц
target_idx = int(points_per_freq * 4000)

for i in range(len(yf)):
    if i < len(yf)-1000:
        yf[-i-1] = yf[-i-1000]
    else:
        yf[-i-1] = 0



plt.plot(xf, np.abs(yf))
plt.show()

new_sig = irfft(yf)

plt.plot(new_sig[:1000])
plt.show()


norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

write("neclean.wav", SAMPLE_RATE, norm_new_sig)
playsound('neclean.wav')

