import tkinter as tk
from tkinter import ttk,PhotoImage
from PIL import Image, ImageTk
from utils import Button
import utils, signals, files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import  make_interp_spline
import guiHelpers


# Input Labels and Fields
labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Signal Generator"]
entries = {}

# Place labels and entries
positions = [
    (60, 50), (300, 50),  # Row 1
    (60, 120), (300, 120),  # Row 2
    (60, 200) # Row 3
]


class Task1:

    def __init__(self, root, main):
        self.root =root
        self.left_section, self.right_section = self.sections()
        self.generate_frame = guiHelpers.right_frame(self.right_section)
        self.read_frame = guiHelpers.right_frame(self.right_section)
        self.main = main
        # self.generate_signal_input(guiHelpers.right_frame)    
      
    def to_generate_signal(self, rightFrame):
        rightFrame.destroy()
        self.generate_frame = guiHelpers.right_frame(self.right_section)
        self.generate_signal_input(self.generate_frame)
        print("to_generate_signal btn triggered")

    def display_read_signal(self, oldFrame):
        file  = utils.browse_file()
        oldFrame.destroy()
        self.read_frame = guiHelpers.right_frame(self.right_section)
        if file:
            #TODO display graph and construct signal 
            signal = files.getSignalFromFile(file)

            guiHelpers.discreteGraph(self.read_frame, "top", signal)

            guiHelpers.continousGraph(self.read_frame, "top", signal)
            
        print("in read file func")

    def to_read_file(self, rightFrame):
        rightFrame.destroy()
        self.read_frame = guiHelpers.right_frame(self.right_section)
        get_file = tk.Button(self.read_frame, text="Select File", bg="#808080", fg="white", width=15, height=2, command=lambda: self.display_read_signal(self.generate_frame))
        get_file.place(x=380, y=400)
        print("in read file func")


    #left section for all buttons - right section for displaying 
    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)

        btn_x = guiHelpers.btn_x

        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)
        
        generate_signal_btn = Button(btn_x, 40, "Generate Signal", lambda:self.to_generate_signal(self.read_frame))
        read_file_btn = Button(btn_x, 120, "Read File", lambda:self.to_read_file(self.generate_frame))
        buttons = []
        buttons.append(generate_signal_btn)
        buttons.append(read_file_btn)
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
        
        return  left_frame, right_frame
    

    def display_graph(self, error_lbl, old_frame, root):
        error_lbl.place(x=900, y=300)
        #valid inputs -> construct signal `obj and go to displaying the graphs
        if(utils.valid_inputs(entries, error_lbl)):
            signal_data = utils.get_data(entries) 
            signal, time = signals.generate_signal(signal_data, error_lbl)
            if signal:
                x_samples = [i for i in range(len(signal.y))]
                print(signal.func)
                if signal.func=='Sine':
                    files.writeOnFile_constructed(signal, './files/task1/sin_output.txt')
                else:
                    files.writeOnFile_constructed(signal, './files/task1/cos_output.txt')

                old_frame.destroy()
                self.generate_frame = guiHelpers.right_frame(self.right_section)
    
                guiHelpers.discreteGraph(self.generate_frame,'top', signal)

                guiHelpers.continousGraph(self.generate_frame,'bottom', signal)
              
                print("in display graphs")
        else:
            error_lbl.place(x=200, y=300)


    def generate_signal_input(self, root):
        
        frame = guiHelpers.right_frame(root)
        #label for trigerring errors 
        error_label = tk.Label(frame, text="enter a valid input")
        # error_label.place(x=200,y=300)
        for i, (text, pos) in enumerate(zip(labels_text, positions)):
            label = tk.Label(frame, text=text.lower(), bg="#d3d3d3")
            label.place(x=pos[0], y=pos[1])
            
            if text == "Signal Generator":
                combo = ttk.Combobox(frame, values=["Sine", "Cosine"], state="readonly", width=27)
                combo.set("choose function")
                combo.place(x=pos[0], y=pos[1]+30)
                entries[text] = combo
            else:
                entry = tk.Entry(frame, width=30)
                entry.place(x=pos[0], y=pos[1]+30)
                entries[text] = entry

        # Display Signal Button
        display_button = tk.Button(frame, text="Display Signal", bg="#808080", fg="white", width=15, height=2, command=lambda:self.display_graph(error_label, frame, root))
        display_button.place(x=380, y=400)

    def goBack(self):

        print("in go back func")
        self.generate_frame.destroy()
        self.read_frame.destroy()
        self.right_section.destroy()
        self.left_section.destroy()
        # main.main_window()
        self.main.main_window()
        del self
