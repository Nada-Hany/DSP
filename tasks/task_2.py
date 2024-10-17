import guiHelpers
import tkinter as tk
from utils import Button
import utils, files
from tkinter import ttk

class Task2:
    def __init__(self, root, main):
        self.root =root
        self.left_section, self.right_section = self.sections()
        self.generate_frame = guiHelpers.right_frame(self.right_section)
        self.read_frame = guiHelpers.right_frame(self.right_section)
        self.add_signals_frame = guiHelpers.right_frame(self.right_section)
        self.subtract_signals_frame = guiHelpers.right_frame(self.right_section)
        self.multiply_signals_frame = guiHelpers.right_frame(self.right_section)
        self.square_signals_frame = guiHelpers.right_frame(self.right_section)
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        self.signal_1 = None
        self.signal_2 = None
        self.main = main


    def goBack(self):
        print("in go back func")
        guiHelpers.goBack(self.left_section, self.right_section,self.generate_frame,self.read_frame,  self.main, self)


    #left section for all buttons - right section for displaying 
    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x

        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)
        
        add_signal_btn = Button(btn_x, 20, "Add Signals", lambda:self.to_add_signals(self.add_signals_frame))
        subtract_signal_btn = Button(btn_x, 70, "Subtract Signals", lambda:self.to_subtract_signals(self.subtract_signals_frame))
        multiply_signal_btn = Button(btn_x, 120, "Multiply Signals", lambda:self.to_multiply_signals(self.multiply_signals_frame))
        square_signal_btn = Button(btn_x, 170, "Square Signals", lambda:self.to_square_signals(self.square_signals_frame))
        normalization_btn = Button(btn_x, 220, "Normalize", lambda:self.to_normalization(self.normalization_frame))
        accumulation_btn = Button(btn_x, 270, "Accumulation", lambda:self.to_accumulation(self.accumulation_frame))
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
    
    def to_accumulation(self):
        print("in accumulation signals")


    def read_signal1(self):
        print("in read signal 1")
        file = utils.browse_file()
        self.signal_1 = files.getSignalFromFile(file)
        # print(self.signal_1.isPeriodic)
        # print(self.signal_1.sampleList)
        # print(self.signal_1.sampleNo)
        # print(self.signal_1.signalType)


    def read_signal2(self):
        print("in read signal 2")
        file = utils.browse_file()
        self.signal_2 = files.getSignalFromFile(file)
        # print(self.signal_2.isPeriodic)
        # print(self.signal_2.sampleList)
        # print(self.signal_2.sampleNo)
        # print(self.signal_2.signalType)
        

