from scipy.fft import fft, fftfreq
import tkinter as tk
from tkinter import ttk
from dtmf.decode import signalLoad
from dtmf.encode import play_and_plot

class Interface:
    def __init__(self, master):
        self.master = master
        master.title("Teclado DTMF")
        master.geometry("500x500")
        master.resizable(False, False)
        master.configure(bg="#070707")

        # estilos
        style = ttk.Style()
        # tema
        style.theme_use('clam')
        
        # estilos de botones
        style.configure('TButton', 
                        font=('SF Pro Display', 18, 'bold'),
                        foreground='white',
                        background="#313138",
                        relief='flat',
                        padding=[5, 5],
                        borderwidth=0,
                        focuscolor="#0A0A7E")
        style.map('TButton', 
                  background=[('active', "#0C0C92")])

        # carga senal
        style.configure('Load.TButton',
                        font=('SF Pro Display', 14),
                        foreground='white',
                        background="#2C78C5",
                        relief='flat',
                        padding=[10, 10],
                        borderwidth=0,
                        focuscolor='#0A84FF')
        style.map('Load.TButton',
                  background=[('active', '#007AFF')])

        # estilo resultado
        style.configure('TLabel',
                        font=('SF Pro Display', 14),
                        background='#1C1C1E',
                        foreground='white')

        # frame de botones
        btn_frame = tk.Frame(master, bg='#1C1C1E')
        btn_frame.pack(pady=20)

        # teclas
        digit_keys = ['1','2','3','4','5','6','7','8','9','*','0','#']
        
        # display de botones en el teclado
        key_layout = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]

        # botones en el frame uno a uno
        for r_idx, row_keys in enumerate(key_layout):
            for c_idx, d in enumerate(row_keys):
                btn = ttk.Button(btn_frame, text=d, 
                                 command=lambda digit=d: play_and_plot(digit),
                                 width=4, style='TButton')
                btn.grid(row=r_idx, column=c_idx, padx=10, pady=10)

        # insert del boton de cargar señal
        load_btn = ttk.Button(master, text="Cargar Señal", command= self.eventSignal,
                              style='Load.TButton')
        # arreglo horizontal
        load_btn.pack(pady=20, padx=20, fill='x')
        # resultado 
        self.result_label = ttk.Label(master, text="Dígitos: ", style='TLabel')
        self.result_label.pack(pady=10)

    def eventSignal(self):
        self.result_label.config(text=f"Dígitos: {signalLoad()}")


