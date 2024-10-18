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
    

def goBack(left_section, right_section,generate_frame, read_frame, main, self):

    print("in go back func")
    generate_frame.destroy()
    read_frame.destroy()
    right_section.destroy()
    left_section.destroy()
    # main.main_window()
    main.main_window()
    del self


places = {
     "top": tk.TOP,
     "bottom":tk.BOTTOM
}

def discreteGraph(root, place, signal_1, signal_2 = None):
    fig = Figure(figsize=(5, 2.1), dpi=100)
    plot = fig.add_subplot(1, 1, 1)


    for i in range(len(signal_1.x)):
        plot.plot([i, i], [0, signal_1.y[i]], 'b-') 

    plot.scatter(signal_1.x, signal_1.y, color="blue", marker="x")  
    if signal_2:
        plot.scatter(signal_2.x, signal_2.y, color="red", marker="o")  
        for i in range(len(signal_2.x)):
            plot.plot([i, i], [0, signal_2.y[i]], 'b-') 
         
    plot.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=places[place], fill=tk.BOTH, expand=1)


def continousGraph(root, place, signal_1, signal_2 = None):
    
    x_y_Spline = make_interp_spline(x=signal_1.x, y=signal_1.y)
    x_quad = np.linspace(min(signal_1.x), max(signal_1.x), 500)
    y_quad = x_y_Spline(x_quad)

    fig = Figure(figsize=(5, 2), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(x_quad, y_quad, color='blue')  
    plot.grid(True)
    
    if signal_2:
        x_y_Spline = make_interp_spline(x=signal_2.x, y=signal_2.y)
        x_quad = np.linspace(min(signal_2.x), max(signal_2.x), 500)
        y_quad = x_y_Spline(x_quad)
        plot.plot(x_quad, y_quad, color='red')  

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=places[place], fill=tk.BOTH, expand=1)