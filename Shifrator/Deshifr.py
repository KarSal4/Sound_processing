
# дешифровка

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

# playsound('Noise.wav')

noise_data = np.int16(noise_data*100)

plt.plot(noise_data)
plt.title("Шум")
plt.show()

# write("Shum.wav", samplerate, noise_data)
# playsound('Shum.wav') 

data = np.load('SecretSignal.npy')
length = noise_length

plt.plot(data)
plt.title("Зашифрованный сигнал")
plt.show()

received_signal = np.int16( data * (3000 / data.max()))

write("received.wav", samplerate, received_signal)
playsound('received.wav')

# Быстроое преобразование Фурье 

noise_yf = rfft(noise_data)
noise_xf = rfftfreq(noise_length, 1/samplerate)

plt.plot(noise_xf, np.abs(noise_yf))
plt.title("Спектр частот шума")
plt.show()

yf = rfft(data)
xf = rfftfreq(length, 1/samplerate)

plt.plot(xf, np.abs(yf))
plt.title("Спектр частот полезного сигнала")
plt.show()

print(len(noise_xf))
print(len(xf))

for i in range(len(xf)):
    yf[i] = yf[i] - noise_yf[i]
    
plt.plot(xf, np.abs(yf))
plt.title("Спектр частот очищенногй записи")
plt.show()

new_sig = irfft(yf)

plt.plot(new_sig)
plt.title("результат")
plt.show()

norm_new_sig = np.int16(new_sig * (3000 / new_sig.max()))

write("New.wav", samplerate, norm_new_sig)
playsound('New.wav')
