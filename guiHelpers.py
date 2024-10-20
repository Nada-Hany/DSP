import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import  make_interp_spline
import numpy as np


back_btn_y = 460
btn_x = 20




def right_frame(root):
    frame = tk.Frame(root, width=520, height=480, bg="#d3d3d3")  # Darker frame color
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
    return frame

def sections(root):
        left_frame = tk.Frame(root, width=150, height=500, bg="#d3d3d3")
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(root, width=450, height=500, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)
       
        return  left_frame, right_frame
    
places = {
     "top": tk.TOP,
     "bottom":tk.BOTTOM
}

markers = ['x', 'o', '*', '^0', '<', ">"]
colors = ['blue', 'red', 'yellow', 'green', 'black']

class Graph:
    def __init__(self):
        self.fig = Figure(figsize=(5, 2.1), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)
        

    def clear(self):
        self.plot.clear()
         
    def discreteGraph(self, root, signals):
        # self.plot.close(self.fig)
        self.fig = Figure(figsize=(5, 2.1), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)

    
        for i in range(len(signals)):
            self.plot.plot([i, i], [0, signals[i].y[i]], 'b-') 

            self.plot.scatter(signals[i].x, signals[i].y, color=f"{colors[i]}", marker=f"{markers[i]}")  

        self.plot.grid(True)
        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


    def continousGraph(self, root, signals):
        self.fig = Figure(figsize=(5, 2.1), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)
        
        for i in range(len(signals)):
            x = signals[i].x
            y = signals[i].y
            x_y_Spline = make_interp_spline(x=x, y=y)
            x = np.linspace(min(x), max(x), 500)
            y = x_y_Spline(x)

            self.plot.plot(x, y, color=f'{colors[i]}')  
        self.plot.grid(True)
        
        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)