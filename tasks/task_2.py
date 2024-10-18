import guiHelpers
import tkinter as tk
from utils import Button
import utils, files
from tkinter import ttk


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
        guiHelpers.goBack(self.left_section, self.right_section,self.generate_frame,self.read_frame,  self.main, self)


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
    
    def to_subtract_signals(self):
        print("in subtract signals")
    
    def to_multiply_signals(self):
        print("in multiply signals")
    
    def to_square_signals(self):
        print("in square signals")
    
    def to_normalization(self):
        print("in normalization")
    
        self.destroyFrames()
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
    
    def to_accumulation(self):
        print("in accumulation signals")
    
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
        # print(self.signal_2.isPeriodic)
        # print(self.signal_2.sampleList)
        # print(self.signal_2.sampleNo)
        # print(self.signal_2.signalType)
   