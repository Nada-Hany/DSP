from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button
import utils, files, test, math 
from tkinter import ttk
import numpy as np
from utils import ReadSignal
from guiHelpers import Graph
import cmath 



staticPath = './files/task4/'


class Task4:
    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.DFT_frame = guiHelpers.right_frame(self.right_section)
        self.IDFT_frame = guiHelpers.right_frame(self.right_section)
        self.signals=[]
        self.baseSignals = []
        self.graph = Graph()
        self.amp_DFT = []
        self.phase_DFT = []
        self.amp_IDFT = []
        self.phase_IDFT = []

    def get_Avtual_lists(self):
        s = files.getSignalFromFile(f'{staticPath}Output_Signal_IDFT.txt')
        self.amp_IDFT = s.x
        self.phase_IDFT = s.y
        s = files.getSignalFromFile(f'{staticPath}Output_Signal_DFT_A,Phase.txt')
        self.amp_DFT = s.x
        self.phase_DFT = s.y
        print('\n\n\n\n\namplitude from file')
        print(self.amp_DFT)

    def destroyFrames(self):
        self.DFT_frame.destroy()
        self.IDFT_frame.destroy()

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)


        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        DFT_btn = Button(btn_x, 120, "DFT", lambda:self.DFT())
        IDFT_btn = Button(btn_x, 200, "IDFT", lambda:self.IDFT())
     
           
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(DFT_btn)
        buttons.append(IDFT_btn)

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame


    def getComponents(self, signal : ReadSignal, inverse = None):
        sign = 1 if inverse else -1
        scale = (1/signal.sampleNo) if inverse else 1
        N = signal.sampleNo
        result = []
        real = np.zeros(N)
        imag = np.zeros(N)
        inv = np.zeros(N)

        if inverse:
            for i in range(N):
                amp = signal.x[i]
                theta = signal.y[i]
                real[i] = amp * np.cos(theta)
                imag[i] = amp * np.cos(theta)

        for k in range(N): 
            sum_real = 0
            sum_imag = 0
            for n in range(N):
                power = n * np.pi * 2 * sign * k / N
                if not inverse:
                    sum_real += signal.y[n] * math.cos(power)
                    sum_imag += signal.y[n] * math.sin(power)
                else:
                    # inv[k] += real[n] * np.cos(power) - imag[n] * np.sin(power)
                    inv[k] += real[n] * np.cos(power) - imag[n] * np.sin(power)

            result.append((scale * sum_real, scale * sum_imag))
            
        if not inverse:
            return result
        else:
            return inv / N
    


    def get_amp_phase(self, data):
        amp = []
        phase = []
        # data -> [[real, imaginary], []]
        for i in data:
            number = np.sqrt(i[0]**2 + i[1]**2)
            amp.append(round(number, 15 - len(str(int(number)))))
            phase.append(math.atan2(i[1], i[0]))
        N = self.signals[0].sampleNo
        Fs = 4
        fundamental_freq = (2 * np.pi * Fs) / (N)
        frequencies = np.arange(1,N + 1) * fundamental_freq
        return amp, phase, frequencies

    def DFT(self):
        self.destroyFrames()
        self.DFT_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.DFT_frame, text="please read a signal first")
        if len(self.signals) == 1:
            res = self.getComponents(self.signals[0])
            amp, phase, freq = self.get_amp_phase(res)
  
            self.signals[0].x = freq
            self.signals[0].y = phase

            self.graph.discreteGraph(self.DFT_frame, self.signals)
            print(test.SignalComaprePhaseShift(self.phase_DFT, phase))
            print("phase --- ")
            print(phase)
            # self.signals = self.baseSignals
            print("my amp --- ")
            print(amp)
            print("actual amp")
            print(self.amp_DFT)
            self.signals[0].y = amp
            self.graph.discreteGraph(self.DFT_frame, self.signals)
            print(test.SignalComapreAmplitude(self.amp_DFT, amp))
        else:
            noSignalError.place(x=200,y=200)


    def IDFT(self):
        self.destroyFrames()
        self.IDFT_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.IDFT_frame, text="please read a signal first")
        if len(self.signals) == 1:
            res = self.getComponents(self.signals[0], 1)
            print(res)
        else:
            noSignalError.place(x=200,y=200)


    def select_files(self):
        self.get_Avtual_lists()
        self.signals = guiHelpers.select_files()
        self.baseSignals = self.signals
        
    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self

       