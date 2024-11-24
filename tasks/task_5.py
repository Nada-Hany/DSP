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

staticPath = './files/task5/'


class Task5:
    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.DCT_frame = guiHelpers.right_frame(self.right_section)
        self.shift_frame = guiHelpers.right_frame(self.right_section)
        self.derivative_frame = guiHelpers.right_frame(self.right_section)
        self.signals=[]
        self.isFolded = False
        self.isShiftedRight = False
        self.graph = Graph()

    
    def destroyFrames(self):
        self.DCT_frame.destroy()
        self.shift_frame.destroy()
        self.derivative_frame.destroy()

    
    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)


        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        shift_fold_btn = Button(btn_x, 120, "Shift/Fold", lambda:self.to_shift_fold())
        DCT_btn = Button(btn_x, 200, "DCT", lambda:self.to_DCT())
        derivative_btn = Button(btn_x, 280, "derivative", lambda:self.to_derivative_frame())
           
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(shift_fold_btn)
        buttons.append(DCT_btn)
        buttons.append(derivative_btn)
    

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame
    

    def shift_and_fold(self, shiftedRight, value, isFolded = 0):
        # shift right
        if (shiftedRight and not isFolded) or (not shiftedRight and isFolded):
            for i in range(len(self.signals[0].x)):
                pass
        # shift left
        elif (shiftedRight and isFolded) or (not shiftedRight and not isFolded):
            pass
        else:
            return 0

    def get_folded(self, checkbox_var):
        if checkbox_var.get():
            self.isFolded = True
        else:
            self.isFolded =  False

    def get_shifted(self, checkbox_var):
        if checkbox_var.get():
            self.isShiftedRight = True
        else:
            self.isShiftedRight =  False

    def to_shift_fold(self):
        self.destroyFrames()
        self.shift_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.shift_frame, text="please read a signal first")

        if len(self.signals) == 1:
        # if True:
            folded_var = tk.IntVar()
            folded_checkbox = tk.Checkbutton(self.shift_frame, text="Fold Signal", variable=folded_var, command=lambda:self.get_folded(folded_var))
            folded_checkbox.place(x=40, y=80)

            shifted_var = tk.IntVar()
            shifted_checkbox = tk.Checkbutton(self.shift_frame, text="Shift Signal Right", variable=shifted_var, command=lambda:self.get_shifted(shifted_var))
            shifted_checkbox.place(x=40, y=100)

            number_entry = tk.Entry(self.shift_frame, width=20)
            number_entry.place(x= 200, y=90)

         
            shift_fold_btn = Button(400, 400, "Run", lambda:self.shift_fold_signal(number_entry))
            tmp = tk.Button(self.shift_frame, text=f"{shift_fold_btn.name}", bg="#808080", fg="white", width=15, height=2, command=shift_fold_btn.onClick)
            tmp.place(x=shift_fold_btn.x, y=shift_fold_btn.y)
        else:
            noSignalError.place(x=200,y=200)


    def shift_fold_signal(self, number_entry):
        not_valid_number = tk.Label(self.shift_frame, text="please enter a valid number")
        if not number_entry.get() or not utils.is_int(number_entry.get()):
            not_valid_number.place(x=200,y=200)
        else:
            signal = self.signals[0]

            shift = number_entry.get()
            self.destroyFrames()
            self.shift_frame = guiHelpers.right_frame(self.right_section)
            shift = int(shift)
            
            if not self.isShiftedRight:
                shift = shift * -1
            
            originIndex = 0
            for i in range(signal.sampleNo):
                if signal.x[i] == 0:
                    originIndex = i
                    break

            new_indices = [(x + shift) for x in signal.x]
            self.signals[0].x = new_indices

            first_indices = signal.y[0:originIndex]
            second_indices = signal.y[originIndex+1:]
            folded_signal = first_indices + second_indices
            folded_signal.reverse()
            folded_signal.insert(originIndex, signal.y[originIndex])
            folded_signal = [int(y) for y in folded_signal]

            if self.isFolded:
                self.signals[0]. y = folded_signal
            # print("indeciss numbers ")
            # print(len( self.signals[0].x))
            print( self.signals[0].x)
            print("\n\n\n\n\n")
            print(self.signals[0].y)
            if shift == 500:
                test.Shift_Fold_Signal(f'{staticPath}Output_ShifFoldedby500.txt', new_indices, folded_signal)
            if shift == -500:
                test.Shift_Fold_Signal(f'{staticPath}Output_ShiftFoldedby-500.txt', new_indices, folded_signal)
            test.Shift_Fold_Signal(f'{staticPath}Output_fold.txt', new_indices, signal.y)

            self.graph.discreteGraph(self.shift_frame, self.signals)
           

    def calculate_dct(self):
        signal = self.signals[0]
        samples = signal.y

        result = 0
        final = 0
        k_list = []
        N = signal.sampleNo

        for k in range(N):
            result = 0
            for n in range(N):
                sum1 = (180 / (4 * N)) * (2 * n - 1) * (2 * k - 1)
                c = math.cos(math.radians(sum1))
                result += samples[n] * c
                final = math.sqrt(2 /N) * result
            k_list.append(float(final))
        
        return k_list
            

    def to_DCT(self):
        self.destroyFrames()
        self.DCT_frame = guiHelpers.right_frame(self.right_section)

        noSignalError = tk.Label(self.DCT_frame, text="please read a signal first")

        if len(self.signals) == 1:
            signal = self.signals[0]
            self.signals[0].y = self.calculate_dct()
            print(self.signals[0].y)
            self.graph.discreteGraph(self.DCT_frame, self.signals)
            test.SignalSamplesAreEqual(f'{staticPath}DCT_output.txt', signal.x, signal.y)
        else:
            noSignalError.place(x=200,y=200)
        
    
    def to_derivative_frame(self):
        InputSignal=[1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100 ]  
        tmp = [f"{i}" for i in range(len(InputSignal))]
        # print(InputSignal)
        self.destroyFrames()
        self.derivative_frame = guiHelpers.right_frame(self.right_section)
        x = [str(i) for i in range(len(InputSignal))]
        signal = ReadSignal('none', 0, len(InputSignal), tmp, x)
        self.signals.append(signal)
        N = len(InputSignal)
        firstDrev = []
        secondDrev = []
        for i in range(1, N):
            a = InputSignal[i-1] if i > 0 else 0
            b = InputSignal[i]
            firstDrev.append(b-a)
        print(firstDrev)
        # signal.y = firstDrev

        # self.graph.discreteGraph(self.derivative_frame, self.signals)
        for i in range(1, N-1):
            a = InputSignal[i-1] if i > 0 else 0
            b = InputSignal[i]
            c = InputSignal[i+1] if i < N-1 else 0
            secondDrev.append(c-2*b+a)
        # signal.y = secondDrev
        print(secondDrev)
        # self.graph.discreteGraph(self.derivative_frame, self.signals)
        test.DerivativeSignal(firstDrev, secondDrev)


    def select_files(self):
        self.signals = guiHelpers.select_files()


    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self