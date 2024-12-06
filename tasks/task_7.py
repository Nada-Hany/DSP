from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button, FilterConfig, ReSampling
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


fileName_sampling = {
    1:"/Sampling_Down.txt",
    2:"/Sampling_Up.txt",
    3:"/Sampling_Up_Down.txt",
}

class Task7:

    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.FIR_frame = guiHelpers.right_frame(self.right_section)
        self.sampling_frame = guiHelpers.right_frame(self.right_section)
        self.filters = ["Low pass", "High pass", "Band pass", "Band stop"]
        self.signals = []
        self.coeff = []
        self.indicies = []
        self.testCaseNum = 0
        self.FIR = True
        self.filterConfig = FilterConfig() 
        self.resampler = ReSampling()
        self.graph = Graph()

    
    def destroyFrames(self):
        self.FIR_frame.destroy()
        self.sampling_frame.destroy()

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)

        test_case_entry = ttk.Entry(left_frame)
        
        # far2 80 ben kol button w el tany
        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        FIR_btn = Button(btn_x, 120, "FIR", lambda:self.to_FIR_frame(test_case_entry))
        sampling_btn = Button(btn_x, 200, "sampling", lambda:self.to_sampling_frame(test_case_entry))
       
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(FIR_btn)
        buttons.append(sampling_btn)



        test_case_label = ttk.Label(left_frame, text="test case number")
        test_case_label.place(x=btn_x, y=250)
        test_case_entry.place(x=btn_x, y=270, width=115)
    

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame
    

    def getFilterConfig(self, filename):
        self.filterConfig.read_from_file(f'{staticPath}{filename}{self.testCaseNum}/Filter Specifications.txt')
        self.filterConfig.deltaF = self.filterConfig.transition_band / self.filterConfig.fs
        
        self.filterConfig.window = utils.getWindowFunction(self.filterConfig.stop_band_attenuation)
        self.filterConfig.N = utils.getCoeffNumber(self.filterConfig.window, self.filterConfig.deltaF)
        self.filterConfig.edge = int((self.filterConfig.N-1)/2)

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
            self.testCaseNum = int(testCase)
            self.calculate_FIR()

            # convolve signal if required 
            if (self.testCaseNum % 2 == 0 and self.FIR):
                signal = self.signals[0]
                self.indicies, self.coeff = utils.calculate_convolution(signal.x, signal.y, self.indicies, self.coeff)
            print("-------------- output of FIR --------------")
            print("indices:\n", self.indicies)
            print("coefficients:\n", self.coeff)
            print("-------------- results --------------")
            print(f"lenth of result = {len(self.coeff)}")
            print(f"lenth of indicies = {len(self.indicies)}")
   
            test.SignalSamplesAreEqual(f"{staticPath}{FIR_path}{self.testCaseNum}{fileName_FIR[self.testCaseNum]}",self.indicies, self.coeff)

        else:
            noSignalError.place(x=200,y=200)

    # should specifiy which test case we're working on before calling
    def calculate_FIR(self):
        self.indicies.clear()
        self.coeff.clear()
        if self.FIR:
            self.getFilterConfig(FIR_path)
        f = self.filterConfig
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

        self.getCoeff(f.edge, f.filter_type, f.window, f.fs, f1, f.N, f2)
        
       

    def getCoeff(self, edge, filter, window, fs, f1, N, f2 = 0):
        for i in range(0, int(edge)+1):
            self.coeff.append(round(utils.getHVal(filter, i, fs, f1, f2) * utils.getWindowVal(window, i, N), 11))

        negativeVal = self.coeff[1:]
        negativeVal.reverse()
        self.coeff = negativeVal + self.coeff   
        self.indicies = [i for i in range(-1*edge, edge+1)]

      

    def to_sampling_frame(self,testCaseEntry):
        self.destroyFrames()
        self.sampling_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.sampling_frame, text="please read a signal first")
        testCase = testCaseEntry.get()
        # if utils.is_int(testCase) and len(self.signals) == 1:
        if True:
            self.testCaseNum = int(testCase)
            self.FIR = False
            self.getFilterConfig(samplingPath)
            self.resampler.read_from_file(f'{staticPath}{samplingPath}{self.testCaseNum}/readme.txt')
            # resample signal itself 
            self.resample()
            # should sample first before convolving [sampled signal with LP]
            print("-------------- output of sampling --------------")
            print("indices:\n", self.indicies)
            print("coefficients:\n", self.coeff)
            print("-------------- results --------------")
            signal = self.signals[0]
            test.SignalSamplesAreEqual(f"{staticPath}{samplingPath}{self.testCaseNum}{fileName_sampling[self.testCaseNum]}",signal.x, signal.y)

        else:
            noSignalError.place(x=200,y=200)


    def resample(self):
        signal = self.signals[0]
        L = self.resampler.L
        M = self.resampler.M
        first_index = int(signal.x[0])
        print(f"sample numebr before sampling  == {len(self.signals[0].y)}")

        # smapling up
        self.calculate_FIR()
        if L != 0 and M == 0:
            upsampled_signal = []
            for sample in signal.y:
                upsampled_signal.append(sample)  
                upsampled_signal.extend([0] * (L - 1)) 
            new_indices = [i for i in range(first_index, len(upsampled_signal)-first_index)]
            self.signals[0].y = upsampled_signal
            self.signals[0].x = new_indices
            print(f"sample numebr after sampling == y = {len(self.signals[0].y) } ,, x={len(new_indices)} ")

            self.signals[0].x, self.signals[0].y = utils.calculate_convolution(self.signals[0].x, self.signals[0].y, self.indicies, self.coeff)


        # sampling down
        if L == 0 and M != 0:
            self.signals[0].x, self.signals[0].y = utils.calculate_convolution(signal.x, signal.y, self.indicies, self.coeff)
            self.signals[0].x = self.signals[0].x[::M]

            downsampled_signal = self.signals[0].y[::M]
            self.signals[0].y = downsampled_signal


        # sampling up then sampling down
        if L != 0 and M != 0:
            upsampled_signal = []
            for sample in signal.y:
                upsampled_signal.append(sample)  
                upsampled_signal.extend([0] * (L - 1)) 
            new_indices = [i for i in range(first_index, len(upsampled_signal)-first_index)]
            
            self.signals[0].x = new_indices
            self.signals[0].y = upsampled_signal

            self.signals[0].x, self.signals[0].y = utils.calculate_convolution(signal.x, signal.y, self.indicies, self.coeff)

            self.signals[0].y = self.signals[0].y[::M]
            self.signals[0].x  = self.signals[0].x[::M]


        print(f"filter samples == {self.filterConfig.N}")
        # self.signals[0].x = [i for i in range(0, len(self.signals[0].y))]
        print("indicies after:\n", self.signals[0].x)
        # print("samples after:\n", self.signals[0].y)



    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self