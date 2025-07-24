import numpy as np
from scipy.fft import ifft    # importamos ifft
from scipy.io.wavfile import write
import sys

# frecuencias DTMF (Hz)
fr = np.array([697, 770, 852, 941])
fc = np.array([1209, 1336, 1477])

# digitos con sus frecuencias
dtmfFreqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

#tiempo de tono
T = 0.25 
# hz
Fs = 32768

def generateToneWav(digit: str, duration: float, Fs: int) -> np.ndarray:
    if digit not in dtmfFreqs:
        raise ValueError(f"Dígito DTMF inválido: {digit}")

    f1, f2 = dtmfFreqs[digit]
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
    tone = ifft(Y).real # type: ignore
    return tone

def generateWav(phone_number: str, filename="generado.wav"):
    partsSignal = []
    timeSilence = 0.15
    samplesS = int(np.ceil(timeSilence * Fs))
    segment = np.zeros(samplesS, dtype=float)

    for digit in phone_number:
        tones = generateToneWav(digit, T, Fs)
        partsSignal.append(tones)
        partsSignal.append(segment)

    final_signal = np.concatenate(partsSignal)
    scaled = final_signal / np.max(np.abs(final_signal))
    signalScaled = np.int16(scaled * 32767)
    write(f"{filename}", Fs, signalScaled)
    
if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 2 or args[0] not in ("--num", "-n"):
        print("Uso: python generator.py --num <número de 11 dígitos>")
        sys.exit(1)

    number = args[1]
    if not (number.isdigit() and len(number) == 11):
        print("Error: El número debe tener exactamente 11 dígitos numéricos.")
        sys.exit(1)

    generateWav(number)