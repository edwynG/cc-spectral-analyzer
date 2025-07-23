import numpy as np
from scipy.fft import ifft    # importamos ifft
from scipy.io.wavfile import write

# frecuencias DTMF (Hz)
fr = np.array([697, 770, 852, 941])
fc = np.array([1209, 1336, 1477])

# digitos con sus frecuencias
dtmf_map = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}
#tiempo de tono
T = 0.25 
# hz
Fs = 32768

def generate_tone_for_wav(digit: str, duration: float, Fs: int) -> np.ndarray:
    if digit not in dtmf_map:
        raise ValueError(f"Dígito DTMF inválido: {digit}")

    f1, f2 = dtmf_map[digit]
    N = int(duration * Fs)

    # Creamos el espectro con dos picos para f1 y f2
    Y = np.zeros(N, dtype=complex)
    k1 = int(f1 * N / Fs)
    k2 = int(f2 * N / Fs)
    Y[k1]  = N * 0.25
    Y[-k1] = N * 0.25
    Y[k2]  = N * 0.25
    Y[-k2] = N * 0.25
    
    # Aquí aplicamos la iFFT para generar directamente la señal de audio
    tone = ifft(Y).real
    return tone

def generateWav(phone_number: str, filename="generado.wav"):
    partsSignal = []
    timeSilence = 0.15
    samplesS = int(np.ceil(timeSilence * Fs))
    segment = np.zeros(samplesS, dtype=float)

    for digit in phone_number:
        tones = generate_tone_for_wav(digit, T, Fs)
        partsSignal.append(tones)
        partsSignal.append(segment)

    final_signal = np.concatenate(partsSignal)
    scaled = final_signal / np.max(np.abs(final_signal))
    signalScaled = np.int16(scaled * 32767)
    write(f"{filename}", Fs, signalScaled)
    
if __name__ == '__main__':
    number = "04143386275"
    generateWav(number)