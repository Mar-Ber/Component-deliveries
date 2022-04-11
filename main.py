#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import random as rd

"""
class Test:  # https://stackoverflow.com/questions/9542738/python-find-in-list
    def __init__(self, a):
        self.a = a


list_of_test = []
b = [1, 2, 2]

for num in range(0, 3):
    list_of_test.append(Test(b[num]))

result = [i for i, x in enumerate(list_of_test) if x.a == 2]
print(list_of_test)
print(result)
pass


temp_list = np.array([[1.2, 1.1, 3.1],
                      [0.9, 3.4, 7.4],
                      [2.3, 1.1, 5.1]])

print(temp_list[1])

result = np.where(temp_list[0] == np.amax(temp_list[0]))
listOfCordinates = list(zip(result[0]))
if len(listOfCordinates) > 0:
    idx = rd.randint(0, len(listOfCordinates)-1)
    print(listOfCordinates[idx][0])

update_idx_schedule = np.array([1.2, 1.1, 3.1])
max_level_idx = np.where(update_idx_schedule == np.amax(update_idx_schedule))
max_level_idx = (list(zip(max_level_idx[0])))[0][0]
print(update_idx_schedule[max_level_idx])

list1 = [1, 0, 1, 0]
list2 = [0, 1, 1, 0]
list3 = [1, 0, 1, 0]
result = [a*b*c for a, b, c in zip(list1, list2, list3)]
print(result)


a = [np.array([1, 24, 4, 5]), temp_list, np.array([11, 1, 1])]
if np.array_equal(temp_list, a.all()):
    print('oho')


from tkinter import *

for i in range(5):
    for j in range(4):
        l = Label(text='%d.%d' % (i, j), relief=RIDGE)
        l.grid(row=i, column=j, sticky=NSEW)

mainloop()


import time
import tkinter as tk
from tkinter import ttk

def ProcessingScript(self, callback):
    ProcessingPage.UpdateProgressbar(self, 50, 'Halfway there')
    time.sleep(2)
    print('Processing takes place here')
    ProcessingPage.UpdateProgressbar(self, 75, 'Finishing up')
    time.sleep(2)


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=500, height=500)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("500x500")
        self.frames = {}
        frame = ProcessingPage(container, self)
        self.frames[ProcessingPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ProcessingPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class ProcessingPage(tk.Frame):
    def __init__(self, parent, controller, ):
        tk.Frame.__init__(self, parent)
        self.controller = controller



        progressBar = ttk.Progressbar(self, orient="horizontal", length=200,mode="determinate")
        progressBar.place(x=20, y=470)
        progressBar['value'] = 0
        self.progressLabel = tk.Label(self, text='Idle...')
        self.progressLabel.place(x=20, y=440)

        PlotButton = tk.Button(self, text='Plot Data',command= self.PlotData)
        PlotButton.place(x=20, y=320)

    def PlotData(self):
        self.UpdateProgressbar(10, 'Generating...')
        app.update()
        time.sleep(2)
        # Execute Main Plotting Function here
        ProcessingScript(self, self.UpdateProgressbar)
        self.UpdateProgressbar(100, 'Finished Plot')
        app.update()

    def UpdateProgressbar(self, Progress, Action):
        self.progressLabel.destroy()
        self.progressLabel = tk.Label(self, text=Action)
        self.progressLabel.place(x=20, y=440)
        progressBar = ttk.Progressbar(self, orient="horizontal", length=200,mode="determinate")
        progressBar.place(x=20, y=470)
        progressBar['value'] = Progress
        app.update()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
    
"""
