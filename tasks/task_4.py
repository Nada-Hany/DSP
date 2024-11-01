from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button
import utils, files, test
from tkinter import ttk
import numpy as np
from utils import ReadSignal
from guiHelpers import Graph

staticPath = './files/task4/'


class Task4:
    def __init__(self, root, main):
        self.root = root
        self.main = main
        self.left_section, self.right_section = self.sections()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        self.signals=[]
        self.baseSignals = []
        self.graph = Graph()


    def destroyFrames(self):
        pass

    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)


        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
     
           
        buttons = []
        buttons.append(read_signal_btn)

        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame

    def select_files(self):
        self.signals = guiHelpers.select_files()
        self.baseSignals = self.signals
        
    def goBack(self):
        self.destroyFrames()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self

       