import tkinter as tk
from tkinter import font
# from task_1 import Task1


class mainPage:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("DSP Design")

    def runMain(self):
        self.main_window()
        self.root.mainloop()

    def main_window(self):
        header_font = font.Font(family="Helvetica", size=60, weight="bold")
        quote_font = font.Font(family="Helvetica", size=12)
        button_font = font.Font(family="Helvetica", size=12)

        # define styles in a dict
        styles = {
            "header": {
                "font": header_font,
                "fg": "black"
            },
            "quote": {
                "font": quote_font,
                "fg": "gray"
            },
            "button": {
                "font": button_font,
                "bg": "#888888",
                "fg": "white",
                "relief": "flat",
                "padx": 20,
                "pady": 10
            }
        }
        contentFrame = tk.Frame(self.root)
        contentFrame.pack(fill="both", expand=True)

        dsp_label = tk.Label(contentFrame, text="DSP", **styles["header"])
        dsp_label.pack(pady=(50, 10))  # Adjust padding to position at top


        quote_label = tk.Label(contentFrame, text="“Data really powers everything that we do.” — Jeff Weiner", **styles["quote"])
        quote_label.pack(pady=(0, 40))  # Adjust padding to position below DSP


        button_frame = tk.Frame(contentFrame)
        button_frame.pack(pady=10)


        task_button_1 = tk.Button(button_frame, text="task 01", **styles["button"], command=lambda: self.toTask_1(contentFrame))
        task_button_1.grid(row=0, column=0, padx=10, pady=10)

        task_button_2 = tk.Button(button_frame, text="task 02", **styles["button"], command=lambda: self.toTask_2(contentFrame))
        task_button_2.grid(row=0, column=1, padx=10, pady=10)

        task_button_3 = tk.Button(button_frame, text="task 03", **styles["button"], command=lambda: self.toTask_3(contentFrame))
        task_button_3.grid(row=0, column=2, padx=10, pady=10)

        task_button_4 = tk.Button(button_frame, text="task 04", **styles["button"], command=lambda: self.toTask_4(contentFrame))
        task_button_4.grid(row=1, column=0, padx=10, pady=10)

        task_button_5 = tk.Button(button_frame, text="task 05", **styles["button"], command=lambda: self.toTask_5(contentFrame))
        task_button_5.grid(row=1, column=1, padx=10, pady=10)

        task_button_6 = tk.Button(button_frame, text="task 06", **styles["button"], command=lambda: self.toTask_6(contentFrame))
        task_button_6.grid(row=1, column=2, padx=10, pady=10)

    def toTask_1(self,frame):
        from  tasks.task_1 import Task1
        frame.destroy()
        task = Task1(self.root, main)

    def toTask_2(self,frame):
        from  tasks.task_2 import Task2
        frame.destroy()
        task = Task2(self.root, main)
    
    def toTask_3(self, frame):
        from tasks.task_3 import Task3
        frame.destroy()
        task = Task3(self.root, main)
    
    def toTask_4(self, frame):
        from tasks.task_4 import Task4
        frame.destroy()
        task = Task4(self.root, main)

    def toTask_5(self, frame):
        from tasks.task_5 import Task5
        frame.destroy()
        task = Task5(self.root, main)

    def toTask_6(self, frame):
        from tasks.task_6 import Task6
        frame.destroy()
        task = Task6(self.root, main)


main = mainPage()
main.runMain()