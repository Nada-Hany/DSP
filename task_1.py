import tkinter as tk
from tkinter import ttk,PhotoImage
from PIL import Image, ImageTk
from utils import Button
import utils, signals, files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import  make_interp_spline

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
        self.left_section, self.right_section = self.sections(root)
        self.generate_frame = self.right_frame(self.right_section)
        self.read_frame = self.right_frame(self.right_section)
        self.main = main
        # self.generate_signal_input(self.right_frame)    
      
    def to_generate_signal(self, rightFrame):
        rightFrame.destroy()
        self.generate_frame = self.right_frame(self.right_section)
        self.generate_signal_input(self.generate_frame)
        print("to_generate_signal btn triggered")

    def display_read_signal(self, oldFrame):
        file  = utils.browse_file()
        oldFrame.destroy()
        self.read_frame = self.right_frame(self.right_section)
        if file:
            #TODO display graph and construct signal 
            signal = files.getSignalFromFile(file)
            fig = Figure(figsize=(5, 2.1), dpi=100)
            plot = fig.add_subplot(1, 1, 1)

            # Sample data for discrete points
            y = [float(i) for i in signal.sampleList]
            x = [i for i in range(0, len(y))]
            
            # drawing y value for each point
            for i in range(len(x)):
                # plot.text(x[i], y[i], f'{y[i]}', fontsize=9, ha='right', va='bottom')
                plot.plot([i, i], [0, y[i]], 'b-') 

            plot.scatter(x, y, color="blue", marker="x")  # Discrete points with circular markers
            plot.grid(True)
            
            canvas = FigureCanvasTkAgg(fig, master=self.read_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # continous ----
            fig = Figure(figsize=(5, 2.1), dpi=100)
            plot = fig.add_subplot(1, 1, 1)

            
            x_y_Spline = make_interp_spline(x=x, y=y)
            x_quad = np.linspace(min(x), max(x), 500)
            y_quad = x_y_Spline(x_quad)


            plot.plot(x_quad, y_quad)
            plot.grid(True)
            plot.set_xlabel("time")
            plot.set_ylabel("signal")
            
            canvas = FigureCanvasTkAgg(fig, master=self.read_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


            
        print("in read file func")

    def to_read_file(self, rightFrame):
        rightFrame.destroy()
        self.read_frame = self.right_frame(self.right_section)
        get_file = tk.Button(self.read_frame, text="Select File", bg="#808080", fg="white", width=15, height=2, command=lambda: self.display_read_signal(self.generate_frame))
        get_file.place(x=380, y=400)
        print("in read file func")

    def goBack(self):
        import main

        print("in go back func")
        self.generate_frame.destroy()
        self.read_frame.destroy()
        self.right_section.destroy()
        self.left_section.destroy()
        # main.main_window()
        self.main.main_window()
        del self

    #left section for all buttons - right section for displaying 
    def sections(self, root):
        left_frame = tk.Frame(root, width=150, height=500, bg="#d3d3d3")
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        image_button = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        image_button.place(x= 20, y=450)
        
        right_frame = tk.Frame(root, width=450, height=500, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        btn_x = 20
        generate_signal_btn = Button(btn_x, 40, "Generate Signal", lambda:self.to_generate_signal(self.read_frame))
        read_file_btn = Button(btn_x, 120, "Read File", lambda:self.to_read_file(self.generate_frame))
        buttons = []
        buttons.append(generate_signal_btn)
        buttons.append(read_file_btn)
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
        
        return  left_frame, right_frame
    



    def right_frame(self, root):
        frame = tk.Frame(root, width=520, height=480, bg="#d3d3d3")  # Darker frame color
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
        return frame

    def display_graph(self, error_lbl, old_frame, root):
        error_lbl.place(x=900, y=300)
        #valid inputs -> construct signal obj and go to displaying the graphs
        if(utils.valid_inputs(entries, error_lbl)):
            signal_data = utils.get_data(entries) 
            signal, time = signals.generate_signal(signal_data, error_lbl)
            if signal:
                x_samples = [i for i in range(len(signal.y_values))]
                print(signal.func)
                if signal.func=='Sine':
                    files.writeOnFile(signal, 'sin_output.txt')
                else:
                    files.writeOnFile(signal, 'cos_output.txt')

                old_frame.destroy()
                self.generate_frame = self.right_frame(self.right_section)
    
                fig = Figure(figsize=(5, 2), dpi=100)
                plot = fig.add_subplot(1, 1, 1)
        
                plot.scatter(x_samples, signal.y_values, color="blue", marker="x")  # Discrete points with circular markers
                plot.set_xlabel("time")
                plot.set_ylabel("signal")
                plot.grid(True)
                # plot.set_xlim(0, 1)
                # attach the figure into the Tkinter canvas
                canvas = FigureCanvasTkAgg(fig, master=self.generate_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                x_y_Spline = make_interp_spline(x=time, y=signal.y_values)
                x_quad = np.linspace(min(x_samples), max(x_samples), 500)
                y_quad = x_y_Spline(x_quad)

                fig = Figure(figsize=(5, 2), dpi=100)
                plot = fig.add_subplot(1, 1, 1)
                plot.grid(True)
                plot.plot(x_quad, y_quad)  
                plot.set_xlabel("time")
                plot.set_ylabel("signal")

                canvas = FigureCanvasTkAgg(fig, master=self.generate_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

                print("in display graphs")
        else:
            error_lbl.place(x=200, y=300)


    def generate_signal_input(self, root):
        
        frame = self.right_frame(root)
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

   
