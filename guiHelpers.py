import tkinter as tk


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

