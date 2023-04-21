import numpy as np
import soundfile as sf
import librosa
from matplotlib import pyplot as plt
from scipy.io.wavfile import write, read
import librosa.display
from playsound import playsound

# загрузка аудиозаписи и ее преобразование в спектрограмму
audio, sr = librosa.load('betkhoven-k-jelize.wav')

playsound('betkhoven-k-jelize.wav')

samplerate, data = read('betkhoven-k-jelize.wav')
length = data.shape[0]

plt.plot(data)
plt.title("Запись с шумом")
plt.show()

# вычисление спектрограммы записи
spec_audio = librosa.stft(audio)

# визуализация спектрограммы записи
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(spec_audio), ref=np.max), y_axis='log', x_axis='time', sr=sr)
plt.title('Спектрограмма исходной аудиозаписи')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

# Загрузка аудиофайла шума
audio_file, sr = librosa.load('Long_noise.wav')



# вычисление спектрограммы записи
spec_noise = librosa.stft(audio_file)

# визуализация спектрограммы записи
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(spec_noise), ref=np.max), y_axis='log', x_axis='time', sr=sr)
plt.title('Спектрограмма шума')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

# Вычисление спектрограммы шума
stft = librosa.stft(audio_file)
# spectrogram = np.abs(stft) # **2

# спектральный профиль шума
# noise_spec = np.mean(spectrogram, axis=1)

for i in range(10):
    spec = librosa.stft(audio)
    # вычисление маски на основе спектрального профиля шума
    mask = (np.abs(spec) > np.abs(stft))

    # удаление шума путем умножения спектрограммы на маску
    spec = spec * mask

    # обратное преобразование спектрограммы в аудио
    audio = librosa.istft(spec)

# сохранение очищенной аудиозаписи
sf.write('clean_audio_file.wav', audio, sr)

samplerate, data = read('clean_audio_file.wav')
length = data.shape[0]

plt.plot(data)
plt.title("итог")
plt.show()

playsound('clean_audio_file.wav')



# вычисление спектрограммы записи
spec_audio = librosa.stft(audio)

# визуализация спектрограммы записи
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(spec_audio), ref=np.max), y_axis='log', x_axis='time', sr=sr)
plt.title('Спектрограмма итоговой аудиозаписи')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

