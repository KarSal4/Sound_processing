import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
import scipy.interpolate
from scipy.fft import *
from scipy.io.wavfile import write, read

samplerate, noise_data = read('Little_noise.wav')
# samplerate, noise_data = read('Long_noise.wav')
noise_length = noise_data.shape[0]

plt.plot(noise_data)
plt.title("Шум")
plt.show()

# playsound('Little_noise.wav')

# playsound('Long_noise.wav')

samplerate, data = read('betkhoven-k-jelize.wav')
length = data.shape[0]

plt.plot(data)
plt.title("Запись с шумом")
plt.show()

# playsound('betkhoven-k-jelize.wav')
# print(data)

# Быстроое преобразование Фурье 

noise_yf = fft(noise_data)
noise_xf = fftfreq(noise_length, 1/samplerate)

plt.plot(noise_xf, np.abs(noise_yf))
plt.title("Спектр частот шума")
plt.ioff()
plt.show(block=True)

yf = fft(data)
xf = fftfreq(length, 1/samplerate)

plt.plot(xf, np.abs(yf))
plt.title("Спектр частот записи")
plt.show(block=True)

print(noise_xf)
print(xf)
print(noise_yf)

new_noise = np.interp(fftshift(xf), fftshift(noise_xf) , fftshift(noise_yf))
noise_yf = fftshift(new_noise)
print(noise_yf)


plt.plot(xf, np.abs(noise_yf))
plt.title("Спектр частот шума 2")
plt.show(block=True)

# Максимальная частота составляет половину частоты дискретизации
points_per_freq = len(xf) / (samplerate / 2)

print(len(noise_xf))
print(len(xf))

for i in range(len(xf)):
    yf[i] = yf[i] - noise_yf[i]
    
plt.plot(xf, np.abs(yf))
plt.title("Спектр частот записи с вырезанными шумами")
plt.show(block=True)

new_sig = ifft(yf)

plt.plot(new_sig)
plt.title("результат")
plt.show()

norm_new_sig = np.int16(new_sig * (3500 / new_sig.max()))

write("clean.wav", samplerate, norm_new_sig)
playsound('clean.wav')

