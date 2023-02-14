import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
from scipy.fft import *
from scipy.io.wavfile import write, read


samplerate, data = read('clean.wav')
length = data.shape[0]

plt.plot(data)
plt.title("Запись")
plt.show()

playsound('clean.wav')

# число точек в normalized_tone


yf = rfft(data)
xf = rfftfreq(length, 1/samplerate)

plt.plot(xf, np.abs(yf))
plt.show()


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

write("neclean.wav", samplerate, norm_new_sig)
playsound('neclean.wav')
