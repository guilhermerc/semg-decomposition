#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

window = tk.Tk(className='S-EMG Decomposition')

window.rowconfigure([0, 1], weight=1)
window.columnconfigure([0, 1], weight=1)

# each frame act as a container
frame_a = tk.Frame(master=window, borderwidth=1)
frame_b = tk.Frame(master=window, borderwidth=1)

frame_a.grid(row=0, column=0, padx=5, pady=5)
frame_b.grid(row=1, column=0, padx=5, pady=5)

description = tk.Label(master=frame_a, text="This is a simple GUI built with tkinter")
description.pack(padx=5, pady=5)

button1 = tk.Button(master=frame_b, text="Click me!")
button1.pack(padx=5, pady=5)

button2 = tk.Button(master=frame_b, text="Close")
button2.pack(padx=5, pady=5)

W, H = 300, 225
WS, HS = window.winfo_screenwidth(), window.winfo_screenheight()
# defining the size of the window and also centering it on the screen
window.geometry('%dx%d+%d+%d' % (W, H, (WS - W)/2, (HS - H)/2))

window.mainloop()
