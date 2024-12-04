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

staticPath = './files/task7/'
FIR_path = 'FIR/Testcase'
samplingPath = 'sampling/Testcase'


class Task7:

    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.FIR_frame = guiHelpers.right_frame(self.right_section)
        self.filters = ["Low pass", "High pass", "Band pass", "Band stop"]
        self.signals=[]
        self.coeff = []
        self.indicies = []
        self.testCaseNum = 0
        self.graph = Graph()

    
    def destroyFrames(self):
        self.FIR_frame.destroy()

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)

        # far2 80 ben kol button w el tany
        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        FIR_btn = Button(btn_x, 120, "FIR", lambda:self.to_FIR_frame())
       
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(FIR_btn)

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame
    


    def to_FIR_frame(self):
        self.destroyFrames()
        self.FIR_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.FIR_frame, text="please read a signal first")

        # if len(self.signals) == 1:
        if True:
            # signal = self.signals[0]
            filter_label = ttk.Label(self.FIR_frame, text="Select Filter:")
            filter_label.place(x=60, y=60)

            filter_var = tk.StringVar()
            filter_dropdown = ttk.Combobox(self.FIR_frame, textvariable=filter_var)
            filter_dropdown['values'] = self.filters
            filter_dropdown.place(x=60, y=80, width=130)

            test_case_label = ttk.Label(self.FIR_frame, text="test case number")
            test_case_label.place(x=320, y=60)
            test_case_entry = ttk.Entry(self.FIR_frame)
            test_case_entry.place(x=320, y=80, width=95)

            enter_inputs_button = ttk.Button(self.FIR_frame, text="Enter Inputs" , command=lambda: self.showInputs(filter_var, test_case_entry))
            enter_inputs_button.place(x=200, y=80)


        else:
            noSignalError.place(x=200,y=200)


    def showInputs(self, dropdown, test_case_entry):
        noSignalError = tk.Label(self.FIR_frame, text="please select a filter first")
        filter = dropdown.get() 
        num = test_case_entry.get()
        
        if filter and utils.is_int(num):
            noSignalError.destroy()
            self.testCaseNum = int(num)
            
            stop_band_label = ttk.Label(self.FIR_frame, text="Stop Band:")
            stop_band_label.place(x=60, y=130)
            stop_band_entry = ttk.Entry(self.FIR_frame)
            stop_band_entry.place(x=60, y=150, width=170)

            transition_band_label = ttk.Label(self.FIR_frame, text="Transition Band:")
            transition_band_label.place(x=60, y=200)
            transition_band_entry = ttk.Entry(self.FIR_frame)
            transition_band_entry.place(x=60, y=220, width=170)

            fc_label = ttk.Label(self.FIR_frame, text="Fc:")
            fc_label.place(x=60, y=270)
            fc_entry = ttk.Entry(self.FIR_frame)
            fc_entry.place(x=60, y=290, width=170)
            
            fc2_label = ttk.Label(self.FIR_frame, text="F2:")
            fc2_entry = ttk.Entry(self.FIR_frame)

            # if filter is band pass or band stop
            if filter == self.filters[2] or filter == self.filters[3]:  
                fc_label.config(text="F1:")

                fc2_label.place(x=270, y=270)
                fc2_entry.place(x=270, y=290, width=170)

            fs_label = ttk.Label(self.FIR_frame, text="Fs:")
            fs_label.place(x=60, y=340)
            fs_entry = ttk.Entry(self.FIR_frame)
            fs_entry.place(x=60, y=360, width=170)

            # calc FIR button
            calc_btn = Button(350, 420, "Smooth", lambda:self.calculate_FIR(filter, stop_band_entry, transition_band_entry, fc_entry, fc2_entry, fs_entry))
            tmp = tk.Button(self.FIR_frame, text=f"{calc_btn.name}", bg="#808080", fg="white", width=15, height=2, command=calc_btn.onClick)
            tmp.place(x=calc_btn.x, y=calc_btn.y)
            
        else:
            noSignalError.place(x=200,y=20)


    def calculate_FIR(self, filter, stop_band_entry, transition_band_entry, fc_entry, fc2_entry, fs_entry):
        noSignalError = tk.Label(self.FIR_frame, text="please enter valid data") 
        bandFilter = (filter == self.filters[2] or filter == self.filters[2])
        mainInputs = (stop_band_entry.get() and transition_band_entry.get() and fc_entry.get() and fs_entry.get())
        if mainInputs:

            stopBand = stop_band_entry.get()
            transitionBand = transition_band_entry.get()
            fc1 = fc_entry.get()
            fs = fs_entry.get()
            deltaF = transitionBand / fs
            window = utils.getWindowFunction(stopBand)
            N = utils.getCoeffNumber(window, deltaF)
            edge = (N-1)/2
            if bandFilter:
                # valid inputs for band pass and band stop filters
                if fc2_entry.get():
                    noSignalError.destroy()
                    
                    f2 = fc2_entry.get()
                    # band pass
                    if filter == self.filters[2]:
                        f1 = fc1 - deltaF
                        f2 = f2 + deltaF
                    # band stop
                    else:
                        f1 = fc1 + deltaF
                        f2 = f2 - deltaF
                    self.getCoeff(edge, filter, window, fs, f1, N, f2)
                
                else:
                    noSignalError.place(x=200,y=20)    
            # valid inputs for low pass and high pass filter
            else:
                noSignalError.destroy()
                # low pass
                if filter == self.filters[0]:
                    fc1 = (fc1 + deltaF / 2) 
                # high pass
                else:
                    fc1 = (fc1 - deltaF / 2) 
                self.getCoeff(edge, filter, window, fs, fc1, N)
            print("output of FIR ------------------")
            test.SignalSamplesAreEqual("",self.indicies, self.coeff)
        else:
            noSignalError.place(x=200,y=20)    

    def getCoeff(self, edge, filter, window, fs, f1, N, f2 = 0):
        for i in range(0, edge):
            self.coeff.append(utils.getH[filter](i, fs, f1, f2) * utils.getW[window](i, N))

        negativeVal = self.coeff[1:]
        negativeVal.reverse()
        self.coeff = negativeVal + self.coeff   
        self.indicies = [i in range(-edge, edge)]
        
    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self