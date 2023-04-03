# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 01:27:03 2023

@author: Kia
"""

from win10toast import ToastNotifier
from tkinter import *
import keyboard as kb
import subprocess
import pyautogui
import threading
import datetime
import sys
import os
from time import sleep


desktop = os.path.expanduser("~/Desktop")
toast = ToastNotifier()
    
def take_bounded_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    image.save(f"{desktop}/{file_name}.png")
    toast.show_toast(
        "Yui Sniptool",
        "Your screenshot has been saved to your desktop",
        duration = 20,
        threaded = True,
    )
        

def take_screenshot_with_shortkey():
    while True:
        print("run")
        sleep(2)

class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        root.geometry('250x50+200+200')  # set new geometry
        root.title('Yui Sniptool')
        # root.attributes('-topmost', True)
        root.resizable(0,0)

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH,
                             expand=YES,
                             padx=1,
                             pady=1
                        )

        self.buttonBar = Frame(
            self.menu_frame,
            bg="")
        self.buttonBar.pack()

        self.snipButton = Button(
            self.buttonBar,
            command=self.create_screen_canvas,
            text="Take Screenshot")
        self.snipButton.pack()
        
        self.label = Label(
                text="Sniptool for Yui - v0.1.2 Beta",
                foreground="white", 
                background="black"  
            )
        self.label.pack()
        
        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(
            self.master_screen,
            background="maroon3"
        )
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            take_bounded_screenshot(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            take_bounded_screenshot(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            take_bounded_screenshot(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='white', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)



if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    # take_screenshot_with_shortkey()
    root.mainloop()