import pyaudio
import webrtcvad
import numpy as np
import collections

# Инициализация PyAudio и WebRTC VAD
audio = pyaudio.PyAudio()
vad = webrtcvad.Vad()

# Конфигурация параметров
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)  # 480
SILENCE_THRESHOLD = 500
BUFFER_SIZE = FRAME_SIZE * 10

# Создание буфера истории сэмплов для эхо-фильтра
history_buffer = collections.deque(maxlen=int(RATE / 100))

# Инициализация фильтров
echo_filter = None
noise_filter = None

# Установка чувствительности VAD
vad.set_mode(3)

# Функция подавления эха
def echo_cancellation(sample):
    global history_buffer
    filtered_samples = np.zeros_like(sample)
    for i in range(len(sample)):
        echo_filter = np.zeros_like(sample)
        if i >= len(history_buffer):
            prev_samples = np.array(history_buffer)
            echo_filter[i-len(history_buffer):i] = prev_samples
            filtered_samples[i] = sample[i] - 0.1 * echo_filter[i]
        else:
            filtered_samples[i] = sample[i]
        history_buffer.append(filtered_samples[i])
    return filtered_samples

# Функция обработки аудио-потока
def process_audio(in_data, frame_count, time_info, status):
    global echo_filter, noise_filter, history_buffer

    # Конвертирование входных данных в массив NumPy
    samples = np.frombuffer(in_data, dtype=np.int16)

    # Определение типа блока звука
    is_speech = vad.is_speech(samples.tobytes(), RATE)

    if is_speech:
        # Применение фильтров при наличии речи
        if echo_filter:
            samples = echo_cancellation(samples)
        if noise_filter:
            samples = noise_filter(samples)
    else:
        # Создание фильтра эхо при отсутствии речи
        if echo_filter is None:
            echo_filter = np.zeros(BUFFER_SIZE, dtype=np.int16)
        # Создание фильтра шума при отсутствии речи
        if noise_filter is None:
            noise_filter = np.zeros(BUFFER_SIZE, dtype=np.int16)

    # Конвертирование обратно в байтовый формат
    out_data = samples.tobytes()

    return (out_data, pyaudio.paContinue)

# Инициализация PyAudio Stream
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    stream_callback=process_audio
)

# Запуск потока PyAudio
stream.start_stream()

# Ожидание завершения работы

while stream.is_active():
    try:
        continue
    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()
audio.terminate()