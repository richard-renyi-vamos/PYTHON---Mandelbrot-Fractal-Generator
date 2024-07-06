import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk

def mandelbrot(h, w, max_iter):
    y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime

class FractalGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Fractal Generator")

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.generate_button = ttk.Button(master, text="Generate Fractal", command=self.generate_fractal)
        self.generate_button.pack()

        self.iterations_label = ttk.Label(master, text="Max Iterations:")
        self.iterations_label.pack()

        self.iterations_entry = ttk.Entry(master)
        self.iterations_entry.insert(0, "100")
        self.iterations_entry.pack()

    def generate_fractal(self):
        max_iter = int(self.iterations_entry.get())
        fractal = mandelbrot(400, 400, max_iter)
        
        # Normalize the fractal array to 0-255
        fractal = (fractal - fractal.min()) * 255.0 / (fractal.max() - fractal.min())
        fractal = fractal.astype('uint8')

        # Create an image from the array
        image = Image.fromarray(fractal)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)

        # Update the canvas with the new image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

root = tk.Tk()
fractal_generator = FractalGenerator(root)
root.mainloop()
