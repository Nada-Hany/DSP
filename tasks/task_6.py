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


    def to_DC_removale_frame(self):
        self.destroyFrames()
        self.DC_removale_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.DC_removale_frame, text="please read a signal first")
        if len(self.signals) == 1:
            signal = self.signals[0]
            freq_domain = utils.DFT(signal)
            freq_domain[0] = 0
            self.signals[0].y = utils.IDFT(signal, freq_domain)
            self.signals[0].y = [round(i, 3) for i in self.signals[0].y]
            print("DC removale output frequency domain: ", self.signals[0].y)
            test.SignalSamplesAreEqual(f"{staticPath}DC_component_output.txt", self.signals[0].x, self.signals[0].y)
            # self.graph.discreteGraph(self.DC_removale_frame, self.signals)

            N = signal.sampleNo
            mean = sum(signal.y) / N
            self.signals[0].y = [(i - mean) for i in signal.y]
            self.signals[0].y = [round(i, 3) for i in self.signals[0].y]
            print("DC removale output time domain: ", self.signals[0].y)
            test.SignalSamplesAreEqual(f"{staticPath}DC_component_output.txt", self.signals[0].x, self.signals[0].y)
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
            print("smoothed signal: ", result)
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

            N1 = signal_1.sampleNo
            N2 = signal_2.sampleNo

            len_result = N1 + N2 - 1
            result = [0] * len_result
            indices = [0] * len_result

            # calculate convolution
            for i in range(N1):
                for j in range(N2):
                    indices[i+j] = signal_1.x[i] + signal_2.x[j]
                    result[i + j] += signal_1.y[i] * signal_2.y[j]
            
            print("convolution")
            print("indices: ", indices)
            print("values: ", result)
            test.ConvTest(indices, result)
        else:
            noSignalError.place(x=200,y=200)
    

    def to_correlation_frame(self):
        self.destroyFrames()
        self.smothing_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.smothing_frame, text="please read a signal first")

        if len(self.signals) == 2:
            signal_1 = self.signals[0]
            signal_2 = self.signals[1]

            N = signal_1.sampleNo

            # Pre-compute squared sums for normalization
            X1_squared_sum = np.sum(i**2 for i in signal_1.y)
            X2_squared_sum = np.sum(i**2 for i in signal_2.y)
            normalization = np.sqrt(X1_squared_sum * X2_squared_sum)

   
            r12 = []
            for j in range(N):
                numerator = sum(signal_1.y[i] * signal_2.y[(i + j) % N] for i in range(N))  
                r12.append(numerator / normalization)

            r12 = np.array(r12)
            print("correlation values: ", r12)
            test.SignalSamplesAreEqual(f"{staticPath}CorrOutput.txt", signal_1.x, r12)
        else:
            noSignalError.place(x=200,y=200)


    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self