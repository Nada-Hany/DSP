from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button, FilterConfig
import utils, files, test, math 
from tkinter import ttk
import numpy as np
from utils import ReadSignal
from guiHelpers import Graph
import math

staticPath = './files/task7/'
FIR_path = 'FIR/Testcase'
samplingPath = 'sampling/Testcase'


fileName_FIR = {
    1:"/LPFCoefficients.txt",
    2:"/ecg_low_pass_filtered.txt",
    3:"/HPFCoefficients.txt",
    4:"/ecg_high_pass_filtered.txt",
    5:"/BPFCoefficients.txt",
    6:"/ecg_band_pass_filtered.txt",
    7:"/BSFCoefficients.txt",
    8:"/ecg_band_stop_filtered.txt",
}


class Task7:

    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.FIR_frame = guiHelpers.right_frame(self.right_section)
        self.filters = ["Low pass", "High pass", "Band pass", "Band stop"]
        self.signals = []
        self.coeff = []
        self.indicies = []
        self.ans = [] 
        self.testCaseNum = 0
        self.graph = Graph()

    
    def destroyFrames(self):
        self.FIR_frame.destroy()

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)

        test_case_entry = ttk.Entry(left_frame)
        
        # far2 80 ben kol button w el tany
        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        FIR_btn = Button(btn_x, 120, "FIR", lambda:self.to_FIR_frame(test_case_entry))
       
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(FIR_btn)



        test_case_label = ttk.Label(left_frame, text="test case number")
        test_case_label.place(x=btn_x, y=170)
        test_case_entry.place(x=btn_x, y=190, width=115)
    

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame
    

    def to_FIR_frame(self, testCaseEntry):
        self.destroyFrames()
        self.FIR_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.FIR_frame, text="please read a signal first")
        testCase = testCaseEntry.get()
        testCorr = utils.is_int(testCase) 
        convolve = testCorr and len(self.signals) == 1 and int(testCase)%2==0
        coeffOnly = testCorr and int(testCase)%2 != 0
        # if convolve or coeffOnly:
        if True:
            # signal = self.signals[0]
            self.testCaseNum = int(testCase)
            print(f"==============test case num = {self.testCaseNum}")
            # print("\n\nfilter specifications:")
            # print(f"fs = {f.fs}, filter = {f.filter_type}, f1/fc = {f.fc}, f2 = {f.f2}, band stop = {f.stop_band_attenuation}, transition = {f.transition_band}\n\n")
            self.calculate_FIR()
            print("-------------- output of FIR --------------")
            print("indices:\n", self.indicies)
            print("coefficients:\n", self.coeff)
            print("-------------- results --------------")
            test.SignalSamplesAreEqual(f"{staticPath}{FIR_path}{self.testCaseNum}{fileName_FIR[self.testCaseNum]}",self.indicies, self.coeff)

        else:
            noSignalError.place(x=200,y=200)

    # should specifiy which test case we're working on before calling
    def calculate_FIR(self):
        self.indicies.clear()
        self.coeff.clear()
        filterConfig = FilterConfig() 
        filterConfig.read_from_file(f'{staticPath}{FIR_path}{self.testCaseNum}/Filter Specifications.txt')
        f = filterConfig
        deltaF = f.transition_band / f.fs
        window = utils.getWindowFunction(f.stop_band_attenuation)
        N = utils.getCoeffNumber(window, deltaF)
        edge = (N-1)/2
        f2 = 0
        if f.filter_type == 'Low pass':
            f1 = (f.fc + f.transition_band / 2) / f.fs
  
        elif f.filter_type == "High pass":
            f1 = (f.fc - f.transition_band / 2) / f.fs

        elif f.filter_type == "Band pass":
            f1 = (f.fc - f.transition_band / 2) / f.fs
            f2 = (f.f2 + f.transition_band / 2) / f.fs

        elif f.filter_type == "Band stop":
            f1 = (f.fc + f.transition_band / 2) / f.fs
            f2 = (f.f2 - f.transition_band / 2) / f.fs

        self.getCoeff(int(edge), f.filter_type, window, f.fs, f1, N, f2)
        
       

    def getCoeff(self, edge, filter, window, fs, f1, N, f2 = 0):
        for i in range(0, int(edge)+1):
            self.coeff.append(round(utils.getHVal(filter, i, fs, f1, f2) * utils.getWindowVal(window, i, N), 11))

        negativeVal = self.coeff[1:]
        negativeVal.reverse()
        self.coeff = negativeVal + self.coeff   
        self.indicies = [i for i in range(-1*edge, edge+1)]

        # convolve signal if required 
        if self.testCaseNum % 2 == 0:

            signal = self.signals[0]
            N2 = signal.sampleNo
            len_result = N + N2 - 1
            result = [0] * len_result
            indices = [0] * len_result

            for i in range(N):
                for j in range(N2):
                    indices[i+j] = self.indicies[i] + signal.x[j]
                    result[i + j] += self.coeff[i] * signal.y[j]

            self.indicies = indices
            self.coeff = result
            



    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self