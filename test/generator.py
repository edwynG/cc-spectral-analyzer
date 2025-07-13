import numpy as np
from scipy.io.wavfile import write

# Frecuencias DTMF (Hz)
fr = np.array([697, 770, 852, 941])
fc = np.array([1209, 1336, 1477])

# Mapeo de dígitos a sus frecuencias (fila, columna)
dtmf_map = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

# Parámetros de la señal
T = 0.25      # Duración del tono (segundos)
Fs = 32768    # Tasa de muestreo (Hz)

def generate_tone_for_wav(digit: str, duration: float, Fs: int) -> np.ndarray:
    if digit not in dtmf_map:
        raise ValueError(f"Dígito DTMF inválido: {digit}")

    f1, f2 = dtmf_map[digit]
    t = np.arange(0, duration, 1/Fs)  # paso fijo 1/Fs
    tone1 = np.sin(2 * np.pi * f1 * t)
    tone2 = np.sin(2 * np.pi * f2 * t)
    distance = 0.5 
    return distance * (tone1 + tone2)

def generateWav(phone_number: str, filename="tono.wav"):

    partsSignal = []
    # intervalo 
    timeSilence = 0.15
    # array de silencio 
    samplesS = int(np.ceil(timeSilence * Fs))
    segment = np.zeros(samplesS, dtype=float)

    for digit in phone_number:
        tones = generate_tone_for_wav(digit, T, Fs)
        partsSignal.append(tones)
        # silencio entre tonos
        partsSignal.append(segment)

    # tono y silencio final arreglo de tono de digito final
    final_signal = np.concatenate(partsSignal)

    # normalizamos y ponemos conversión a 16 bits
    scaled = final_signal / np.max(np.abs(final_signal))
    signalScaled = np.int16(scaled * 32767)

    write(f"{filename}", Fs, signalScaled)

if __name__ == '__main__':
    number = "04241543777"
    generateWav(number)