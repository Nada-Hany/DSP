from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button
import utils, files
from tkinter import ttk
import numpy as np

staticPath= './files/task2/'


class Task2:
    def __init__(self, root, main):
        self.root =root
        self.left_section, self.right_section = self.sections()
        self.add_signals_frame = guiHelpers.right_frame(self.right_section)
        self.subtract_signals_frame = guiHelpers.right_frame(self.right_section)
        self.multiply_signals_frame = guiHelpers.right_frame(self.right_section)
        self.square_signals_frame = guiHelpers.right_frame(self.right_section)
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        self.signal_1 = None
        self.signal_2 = None
        self.main = main
        
    def destroyFrames(self):
        self.add_signals_frame.destroy()
        self.subtract_signals_frame.destroy()
        self.multiply_signals_frame.destroy()
        self.square_signals_frame.destroy()
        self.normalization_frame.destroy()
        self.accumulation_frame.destroy()

   
    def goBack(self):

        print("in go back func")
        self.add_signals_frame.destroy()
        self.subtract_signals_frame.destroy()
        self.multiply_signals_frame.destroy()
        self.square_signals_frame.destroy()
        self.normalization_frame.destroy()
        self.square_signals_frame.destroy()
        self.right_section.destroy()
        self.left_section.destroy()
        # main.main_window()
        self.main.main_window()
        del self


    #left section for all buttons - right section for displaying 
    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x

        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)
        
        add_signal_btn = Button(btn_x, 20, "Add Signals", lambda:self.to_add_signals())
        subtract_signal_btn = Button(btn_x, 70, "Subtract Signals", lambda:self.to_subtract_signals())
        multiply_signal_btn = Button(btn_x, 120, "Multiply Signals", lambda:self.to_multiply_signals())
        square_signal_btn = Button(btn_x, 170, "Square Signals", lambda:self.to_square_signals())
        normalization_btn = Button(btn_x, 220, "Normalize", lambda:self.to_normalization())
        accumulation_btn = Button(btn_x, 270, "Accumulation", lambda:self.to_accumulation())
        read_signal1_btn = Button(btn_x, 320, "read signal-1", lambda:self.read_signal1())
        read_signal2_btn = Button(btn_x, 370, "read signal-2", lambda:self.read_signal2())
        
        
        buttons = []
        buttons.append(add_signal_btn)
        buttons.append(subtract_signal_btn)
        buttons.append(multiply_signal_btn)
        buttons.append(square_signal_btn)
        buttons.append(normalization_btn)
        buttons.append(accumulation_btn)
        buttons.append(read_signal1_btn)
        buttons.append(read_signal2_btn)
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
        
        return  left_frame, right_frame
    

    def to_add_signals(self):
        print("in add signals")
        self.destroyFrames()
        self.add_signals_frame= guiHelpers.right_frame(self.right_section)
        nosignal=tk.Label(self.right_section, text="please read a signal first")
        signal= self.signal_1 and self.signal_2
        if signal:
            nosignal.destroy()
            min_len = min(len(self.signal_1.y), len(self.signal_2.y))
            signal_1_truncated = self.signal_1.y[:min_len]
            signal_2_truncated = self.signal_2.y[:min_len]
            combined_signal_y = signal_1_truncated + signal_2_truncated
            combined_signal =(combined_signal_y, np.arange(1, len(combined_signal_y) + 1))
            guiHelpers.discreteGraph(self.add_signals_frame, 'top', combined_signal)
            guiHelpers.continousGraph(self.add_signals_frame, 'top', combined_signal)
            files.writeOnFile_read(combined_signal, f"{staticPath}added_signals.txt")
        else:
            nosignal.pack()  # Show message if no signal is loaded
        print("No signal loaded to add.")
            

    
    def to_subtract_signals(self):
        print("in subtract signals")
        self.destroyFrames()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
    
    def to_multiply_signals(self):
        print("in multiply signals")
        self.destroyFrames()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
    
    def to_square_signals(self):
        print("in square signals")
        self.destroyFrames()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
    
    def to_normalization(self):
        print("in normalization")
    
        self.destroyFrames()
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.right_section, text="please read a signal first")
        # range of normalization [-1,1]
        new_min, new_max = -1, 1
        signal = self.signal_1 or self.signal_2
        if signal:
            noSignalError.destroy()
            y_min, y_max = np.min(signal.y), np.max(signal.y)
            signal.y = (signal.y - y_min) / (y_max - y_min) * (new_max - new_min) + new_min

            signal.x = np.arange(1, len(signal.y) + 1)

            guiHelpers.discreteGraph(self.normalization_frame, 'top', signal)
            guiHelpers.continousGraph(self.normalization_frame, 'top', signal)

            files.writeOnFile_read(signal, f"{staticPath}normalization.txt")

        else:
            noSignalError.place(x=200,y=200)
            
    def to_accumulation(self):

        self.destroyFrames()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.right_section, text="please read a signal first")

        signal = self.signal_1 or self.signal_2
        if signal:
            noSignalError.destroy()
            accumulation = []
            accumulation.append(0)
            for i in range(1, len(signal.y)):
                tmp = i + accumulation[i-1]
                accumulation.append(tmp)
            
            guiHelpers.discreteGraph(self.accumulation_frame, "top", signal)
            guiHelpers.continousGraph(self.accumulation_frame, "top", signal)
            signal.y = accumulation
            files.writeOnFile_read(signal, f"{staticPath}accumulation.txt")

        else:
            noSignalError.place(x=200,y=200)
    


    def read_signal1(self):
        print("in read signal 1")
        file = utils.browse_file()
        self.signal_1 = files.getSignalFromFile(file)


    def read_signal2(self):
        print("in read signal 2")
        file = utils.browse_file()
        self.signal_2 = files.getSignalFromFile(file)
