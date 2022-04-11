#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk


class NumberOfMachines:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.root.title("Error")
        tk.Label(self.root, text='Error!', font='arial 12 bold').grid(row=0, column=0, padx=10, pady=[20, 0])
        tk.Label(self.root, text='The number of machines cannot exceed the number of products', font='arial 11').grid(row=1, column=0, padx=10, pady=0)
        tk.Label(self.root, text='The desired value has been set to the maximum', font='arial 10').grid(row=2, column=0, padx=10, pady=20)
