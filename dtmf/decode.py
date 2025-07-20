import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
from playsound import playsound
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from tkinter import filedialog, messagebox
from . import dtmf_map, fc, fr

def signalDecode(signal, fs):
    """
    Decodifica una señal DTMF en dígitos usando segmentación por energía.
    """
    digits = ''
    
    # --- Segmentación por Energía ---
    window_size = int(fs * 0.02)
    # Umbral dinámico: 20% de la energía media de la señal
    energy_threshold = np.mean(signal**2) * 0.2 

    toneIn = False
    startIndex = 0
    
    for i in range(0, len(signal) - window_size, window_size):
        window_energy = np.mean(signal[i:i+window_size]**2)
        
        # Detección del inicio de un tono
        if not toneIn and window_energy > energy_threshold:
            toneIn = True
            startIndex = i
            
        # Detección del final de un tono
        elif toneIn and window_energy < energy_threshold:
            toneIn = False
            endIndex = i
            
            # Procesar el segmento encontrado
            segment = signal[startIndex:endIndex]
            
            # Ignorar ruidos o segmentos muy cortos
            if len(segment) < int(fs * 0.1):
                continue

            # --- Lógica de FFT y decodificación ---
            Y = fft(segment)
            freqs = fftfreq(len(segment), 1 / fs)
            
            pos_mask = freqs > 0
            freqs_pos = freqs[pos_mask]
            mags = np.abs(Y[pos_mask])
            
            # Filtrar para buscar picos solo en el rango de interés DTMF
            relevant_mask = (freqs_pos > 600) & (freqs_pos < 1550)
            if not np.any(relevant_mask): continue

            mags_relevant = mags[relevant_mask]
            freqs_relevant = freqs_pos[relevant_mask]
            
            if len(mags_relevant) < 2: continue
            
            # Encontrar los dos picos de mayor magnitud
            peak_indices = np.argsort(mags_relevant)[-2:]
            detected_peaks = freqs_relevant[peak_indices]
            
            if len(detected_peaks) < 2: continue
            
            f_low, f_high = sorted(detected_peaks)
            
            # Encontrar la frecuencia de fila y columna más cercana
            row = fr[np.argmin(np.abs(fr - f_low))]
            col = fc[np.argmin(np.abs(fc - f_high))]
            
            # Mapeo inverso para encontrar el dígito
            found_digit = '?'
            for digit, (r, c) in dtmf_map.items():
                if r == row and c == col:
                    found_digit = digit
                    break
            
            digits += found_digit
            
            # Detenerse si ya encontramos 11 dígitos
            if len(digits) >= 11:
                break
    
    return digits

def signalLoad():
        """Maneja la carga y decodificación de una señal de archivo WAV."""
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if not path:
            return
        
        try:
            loadFs, data = wavfile.read(path)
            
            # Convertir a mono si es estéreo
            if data.ndim > 1:
                data = data[:, 0]
            
            # Normalizar la señal a un rango de -1.0 a 1.0
            signal = data.astype(np.float32) / np.max(np.abs(data))

            # Reproducir la señal cargada
            relativePath = os.path.relpath(path, os.getcwd())
            playsound(relativePath)

            # Graficar la señal cargada
            t = np.linspace(0, len(signal) / loadFs, num=len(signal))
            plt.figure("Señal Cargada")
            plt.clf()
            plt.plot(t, signal, color='#FF9500') # Color naranja estilo iOS
            plt.title("Señal cargada del archivo", fontsize=14, fontweight='bold')
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud Normalizada')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.show(block=False)

            # Decodificar la señal
            digitsDecode = signalDecode(signal, loadFs)
            return digitsDecode
            
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")