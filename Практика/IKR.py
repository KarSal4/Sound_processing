import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
from scipy.fft import *
from scipy.io.wavfile import write, read

samplerate, noise_data = read('Noise.wav')
noise_length = noise_data.shape[0]

plt.plot(noise_data)
plt.title("Шум")
plt.show()

playsound('Noise.wav')

samplerate, data = read('betkhoven-k-jelize.wav')
length = data.shape[0]

plt.plot(data)
plt.title("Запись с шумом")
plt.show()

playsound('betkhoven-k-jelize.wav')
print(data)

# Быстроое преобразование Фурье 

noise_yf = rfft(noise_data)
noise_xf = rfftfreq(noise_length, 1/samplerate)

plt.plot(noise_xf, np.abs(noise_yf))
plt.title("Спектр частот шума")
plt.show()

yf = rfft(data)
xf = rfftfreq(length, 1/samplerate)

plt.plot(xf, np.abs(yf))
plt.title("Спектр частот записи")
plt.show()

print(len(noise_xf))
print(len(xf))

for i in range(len(xf)):
    yf[i] = yf[i] - noise_yf[i]
    
plt.plot(xf, np.abs(yf))
plt.title("Спектр частот записи с вырезанными шумами")
plt.show()

new_sig = irfft(yf)

plt.plot(new_sig)
plt.title("результат")
plt.show()

norm_new_sig = np.int16(new_sig * (3000 / new_sig.max()))

write("clean.wav", samplerate, norm_new_sig)
playsound('clean.wav')
