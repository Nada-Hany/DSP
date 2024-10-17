import tkinter as tk
from tkinter import font
# from task_1 import Task1


class mainPage:
    
    def __init__(self):
        self.run = True
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
        task_button_1.grid(row=0, column=0, padx=10)

        task_button_2 = tk.Button(button_frame, text="task 02", **styles["button"], command=lambda: self.toTask_2(contentFrame))
        task_button_2.grid(row=0, column=1, padx=10)
  


    def toTask_1(self,frame):
        from  task_1 import Task1
        self.run = False
        frame.destroy()
        task = Task1(self.root, main)

    def toTask_2(self,frame, root):
        self.run = False
        frame.destroy()
        

main = mainPage()
main.runMain()