import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
from scipy.fft import *
from scipy.io.wavfile import write, read


samplerate, data = read('record.wav')
length = data.shape[0]

plt.plot(data)
plt.title("Запись")
plt.show()

playsound('record.wav')

yf = rfft(data)
xf = rfftfreq(length, 1/samplerate)

plt.plot(xf, np.abs(yf))
plt.show()

print('Вверх или вниз?')

a = input()

if a == 'вверх':
    for i in range(len(yf)):
        if i < len(yf)-1000:
            yf[-i-1] = yf[-i-1000]
        else:
            yf[-i-1] = 0

if a == 'вниз':
    for i in range(len(yf)):
        if i > len(yf)-500:
            yf[i] = 0
        else:
            yf[i] =  yf[i+499]


plt.plot(xf, np.abs(yf))
plt.show()

new_sig = irfft(yf)

plt.plot(new_sig)
plt.show()


norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

write("Modified.wav", samplerate, norm_new_sig)
playsound('Modified.wav')
