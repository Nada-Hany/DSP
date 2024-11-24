from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button
import utils, files, test, math 
from tkinter import ttk
import numpy as np
from utils import ReadSignal
from guiHelpers import Graph
import math

staticPath = './files/task6/'


class Task6:

    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.DC_removale_frame = guiHelpers.right_frame(self.right_section)
        self.smothing_frame= guiHelpers.right_frame(self.right_section)
        self.convolution_frame= guiHelpers.right_frame(self.right_section)
        self.correlation_frame= guiHelpers.right_frame(self.right_section)
        self.signals=[]
        self.isFolded = False
        self.isShiftedRight = False
        self.graph = Graph()

    
    def destroyFrames(self):
        self.DC_removale_frame.destroy()
        self.smothing_frame.destroy()
        self.convolution_frame.destroy()
        self.correlation_frame.destroy()
    

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)

        # far2 80 ben kol button w el tany
        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        DC_removale_btn = Button(btn_x, 120, "DC removale", lambda:self.to_DC_removale_frame())
        smooth_signal_btn = Button(btn_x, 200, "smooth signal", lambda:self.to_smooth_signal_frame())
        convolution_btn = Button(btn_x, 280, "convolution", lambda:self.to_convolution_frame())
        correlation_btn = Button(btn_x, 360, "correlation", lambda:self.to_correlation_frame())
          
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(DC_removale_btn)
        buttons.append(smooth_signal_btn)
        buttons.append(convolution_btn)
        buttons.append(correlation_btn)
    
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame
    

    def DFT (self):
        signal = self.signals[0]
        N = signal.sampleNo
        res = []
        for k in range(N):
            realSum = 0
            imagSum = 0
            for n in range(N):
                angle = -2 * np.pi * k * n / N
                realSum += signal.y[n] * np.cos(angle)
                imagSum += signal.y[n] * np.sin(angle)
            res.append(complex(realSum, imagSum))
        return res


    def IDFT(self, freq_domain):
        N = len(freq_domain)
        signal = []
        for n in range(N):
            real = sum(freq_domain[k].real * np.cos(2 * np.pi * k * n / N) - 
                        freq_domain[k].imag * np.sin(2 * np.pi * k * n / N) for k in range(N))
            signal.append(real / N)
        return signal


    def to_DC_removale_frame(self):
        self.destroyFrames()
        self.DC_removale_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.DC_removale_frame, text="please read a signal first")
        if len(self.signals) == 1:
            freq_domain = self.DFT()
            freq_domain[0] = 0
            self.signals[0].y = self.IDFT(freq_domain)
            self.signals[0].y = [round(i, 3) for i in self.signals[0].y]
            print(self.signals[0].y)
            test.SignalSamplesAreEqual(f"{staticPath}DC_component_output.txt", self.signals[0].x, self.signals[0].y)
            # self.graph.discreteGraph(self.DC_removale_frame, self.signals)
        else:
            noSignalError.place(x=200,y=200)


    def to_smooth_signal_frame(self):
        self.destroyFrames()
        self.smothing_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.smothing_frame, text="please read a signal first")
        if len(self.signals) == 1:
            value_box = tk.Entry(self.smothing_frame, width=18)
            value_box.place(x=200, y=200)
            run_btn = Button(350, 400, "Smooth", lambda:self.smooth_signal(value_box))
            tmp = tk.Button(self.smothing_frame, text=f"{run_btn.name}", bg="#808080", fg="white", width=15, height=2, command=run_btn.onClick)
            tmp.place(x=run_btn.x, y=run_btn.y)

        else:
            noSignalError.place(x=200,y=200)


    def smooth_signal(self, entry):

        noSignalError = tk.Label(self.smothing_frame, text="please enter a valid number")
        if not entry.get() or not utils.is_int(entry.get()):
            noSignalError.place(x=200,y=100)
        else:
            noSignalError.destroy()
            signal = self.signals[0]
            N = signal.sampleNo
            windowSize = int(entry.get())

            result = np.zeros(N - windowSize + 1)

            for i in range(len(result)):
                result[i] = np.sum(signal.y[i:i+windowSize]) / windowSize
            
            result = [round(i) for i in result]
            signal.y = result
            print(result)
            if(windowSize == 3):
                test.SignalSamplesAreEqual(f"{staticPath}OutMovAvgTest1.txt", signal.x, signal.y)
            else:
                test.SignalSamplesAreEqual(f"{staticPath}OutMovAvgTest2.txt", signal.x, signal.y)


    def to_convolution_frame(self):
        self.destroyFrames()
        self.smothing_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.smothing_frame, text="please read a signal first")

        if len(self.signals) == 2:
            signal_1 = self.signals[0]
            signal_2 = self.signals[1]

            min_ = min(min(signal_1.x), min(signal_2.x))
            
            n_min = min(range(len(signal_1.y))) + min(range(len(signal_2.y)))
            n_max = max(range(len(signal_1.y))) + max(range(len(signal_2.y)))

            y = []
            for n in range(n_min, n_max + 1):
                sum_val = 0
                for k in range(len(signal_1.y)):
                    if 0 <= n - k < len(signal_2.y):  
                        sum_val += signal_1.y[k] * signal_2.y[n - k]
                
                result_index = min_ + n  
                y.append((int(result_index), int(sum_val)))

            N1 = signal_1.sampleNo
            N2 = signal_2.sampleNo
            len_result = N1 + N2 - 1

            result = [0] * len_result

            # calculate convolution
            for n in range(len_result):
                for m in range(N1):
                    if 0 <= n - m < N2:
                        result[n] += signal_1.y[n - m] * signal_2.y[m]

            print(result)
            # print(y[1])

        else:
            noSignalError.place(x=200,y=200)
    

    def to_correlation_frame(self):
        pass


    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self