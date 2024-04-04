import tkinter as tk
import sqlite3
from tkinter import Scrollbar

def on_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mouse_wheel(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def display_data():

    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS temperature_data (timestamp TEXT, temperature INTEGER)")

    c.execute("SELECT * FROM temperature_data")
    rows = c.fetchall()

    root = tk.Tk()
    root.title("Просмотр текущих значений температуры")
    root.geometry("400x300")  # фиксированный размер окна

    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    canvas.bind("<Configure>", lambda event, canvas=canvas: on_configure(event, canvas))
    canvas.bind("<MouseWheel>", lambda event, canvas=canvas: on_mouse_wheel(event, canvas))

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    for idx, row in enumerate(rows, start=1):
        timestamp, temperature = row
        data_label = tk.Label(frame, text=f"Запись #{idx}: Время: {timestamp}, Температура: {temperature}")
        data_label.pack(padx=20, pady=5)

    conn.close()

    root.mainloop()
