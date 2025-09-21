import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np


class App3:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App3")
        self.root.geometry("200x50")
        self.upload_button = ttk.Button(self.root, text="Upload file", command=self.upload_file)
        self.upload_button.pack(pady=5)
        self.scales = {
            "hue": 0,
            "sat": 1.0,
            "val": 1.0
        }
        self.pil_image = None
        self.tk_image = None
        self.rgb_matrix = None
        self.hsv_matrix = None
        self.new_image = None

    def create_new_window(self, width, height):
        new_window = tk.Toplevel(self.root)
        new_window.geometry(f"{width+40}x{height+300}")

        hue_var = tk.IntVar(value=0)
        hue_label = ttk.Label(new_window, textvariable=hue_var)
        hue_label.pack()
        hue_scale = ttk.Scale(new_window, variable=hue_var, orient=tk.HORIZONTAL, length=width-20, from_=0, to=360, value=0,
                              command=self.hue_scale_handler)
        hue_scale.pack(pady=5)

        sat_var = tk.DoubleVar(value=1.0)
        sat_label = ttk.Label(new_window, textvariable=sat_var)
        sat_label.pack()
        saturation_scale = ttk.Scale(new_window, variable=sat_var, orient=tk.HORIZONTAL, length=width-20, from_=0, to=2, value=1,
                                     command=self.saturation_scale_handler)
        saturation_scale.pack(pady=5)

        val_var = tk.DoubleVar(value=1.0)
        val_label = ttk.Label(new_window, textvariable=val_var)
        val_label.pack()
        value_scale = ttk.Scale(new_window, variable=val_var, orient=tk.HORIZONTAL, length=width-20, from_=0, to=2, value=1,
                                command=self.value_scale_handler)
        value_scale.pack(pady=5)


        self.canvas = tk.Canvas(new_window, width=width, height=height, bg="white")
        self.canvas.pack()
        update_image_button = ttk.Button(new_window, text="Update image", command=self.update_image_button_handler)
        update_image_button.pack(pady=5)
        download_image_button = ttk.Button(new_window, text="Download image", command=self.download_image_button_handler)
        download_image_button.pack(pady=5)

        return new_window

    def download_image_button_handler(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if not file_path:
            return
        try:
            self.pil_image.save(file_path)
        except Exception as e:
            print(f"Ошибка скачивания изображения: {e}")


    def hsv2rgb(self, hsv_matrix):
        height, width, _ = hsv_matrix.shape
        new_rgb_matrix = np.zeros((height, width, 3))
        for i in range(height):
            for j in range(width):
                h, s, v = hsv_matrix[i, j]
                hi = np.floor(h / 60) % 6
                f = h / 60 - np.floor(h / 60)
                p = v * (1 - s)
                q = v * (1 - f * s)
                t = v * (1 - (1 - f) * s)
                if hi == 0:
                    r, g, b = v, t, p
                elif hi == 1:
                    r, g, b = q, v, p
                elif hi == 2:
                    r, g, b = p, v, t
                elif hi == 3:
                    r, g, b = p, q, v
                elif hi == 4:
                    r, g, b = t, p, v
                elif hi == 5:
                    r, g, b = v, p, q
                new_rgb_matrix[i, j] = [r, g, b]
        return new_rgb_matrix

    def rgb2hsv(self, rgb_matrix):
        try:
            rgb_matrix = rgb_matrix / 255
            height, width, _ = rgb_matrix.shape
            new_hsv_matrix = np.zeros((height, width, 3))
            for i in range(height):
                for j in range(width):
                    r, g, b = rgb_matrix[i, j]
                    cmax = np.max(rgb_matrix[i, j])
                    cmin = np.min(rgb_matrix[i, j])
                    delta = cmax - cmin
                    if cmax == cmin:
                        h = 0
                    elif cmax == r and g >= b:
                        h = 60 * (g - b) / delta
                    elif cmax == r and g < b:
                        h = 60 * (g - b) / delta + 360
                    elif cmax == g:
                        h = (b - r) / delta + 120
                    elif cmax == b:
                        h = 60 * (r - g) / delta + 240
                    if cmax == 0:
                        s = 0
                    else:
                        s = 1 - cmin / cmax
                    v = cmax
                    new_hsv_matrix[i, j, 0] = h
                    new_hsv_matrix[i, j, 1] = s
                    new_hsv_matrix[i, j, 2] = v
            return new_hsv_matrix
        except Exception as e:
            print(f"Ошибка rgb2hsv: {e}")

    def hue_scale_handler(self, val):
        val = float(val)
        self.scales["hue"] = val

    def saturation_scale_handler(self, val):
        val = float(val)
        self.scales["sat"] = val

    def value_scale_handler(self, val):
        val = float(val)
        self.scales["val"] = val

    def update_image_button_handler(self):
        new_hsv_matrix = self.hsv_matrix.copy()
        new_hsv_matrix[..., 0] = np.clip(self.hsv_matrix[..., 0] + self.scales["hue"], 0, 359)
        new_hsv_matrix[..., 1] = np.clip(self.hsv_matrix[..., 1] * self.scales["sat"], 0, 1)
        new_hsv_matrix[..., 2] = np.clip(self.hsv_matrix[..., 2] * self.scales["val"], 0, 1)
        new_rgb_matrix = self.hsv2rgb(new_hsv_matrix)
        self.pil_image = Image.fromarray((new_rgb_matrix * 255).astype(np.uint8))
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)


    def upload_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if not filename:
            return
        try:
            self.pil_image = Image.open(filename)
            self.rgb_matrix = np.array(self.pil_image)
            self.hsv_matrix = self.rgb2hsv(self.rgb_matrix)
            width, height = self.pil_image.size
            self.new_window = self.create_new_window(width, height)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")


    def run(self):
        self.root.mainloop()