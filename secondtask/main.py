import os
import enum
import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt

from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk


class Channel(enum.Enum):
    BASE = "base"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class TkinterApp:
    def __init__(self):
        self.root = tk.Tk()

        self.entry_path = tk.Entry(self.root, width=20)
        self.entry_path.pack(side=tk.TOP, pady=2, anchor=tk.W)

        self.selected_opt = tk.StringVar()

        self.channel_list = tk.ttk.Combobox(self.root, textvariable=self.selected_opt,
                                            values=list(x.value for x in Channel))
        self.channel_list.set(Channel.BASE.value)
        self.channel_list.config(state="readonly")
        self.channel_list.pack(side=tk.TOP, pady=4, anchor=tk.W)

        self.button_apply = tk.Button(self.root, text="Применить", command=self.__update_image__)
        self.button_apply.pack(side=tk.TOP, anchor=tk.W)

        self.image = tk.Label(self.root, image=None)
        self.image.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def __update_image__(self):
        path = self.entry_path.get()
        channel_str = self.selected_opt.get()
        try:
            channel_enum = Channel(channel_str)
        except Exception as e:
            print(f"Ошибка: {e}")
            return
        try:
            self.photo = self.change_channel(path, channel_enum)
            self.image.config(image=self.photo)
        except Exception as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def change_channel(filename: str, channel: Channel) -> ImageTk.PhotoImage:
        with Image.open(filename) as img:
            width, height = img.size
            pixels = img.load()
            if channel == Channel.BASE:
                return ImageTk.PhotoImage(img)

            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y][:3]
                    if channel == Channel.RED:
                        pixels[x, y] = (r, 0, 0)
                    elif channel == Channel.GREEN:
                        pixels[x, y] = (0, g, 0)
                    elif channel == Channel.BLUE:
                        pixels[x, y] = (0, 0, b)
            return ImageTk.PhotoImage(img)

    def run(self):
        self.root.mainloop()


def main() -> None:
    app = TkinterApp()
    app.run()


if __name__ == '__main__':
    main()
