import tkinter as tk
from tkinter import font

def simulate_movement(target_x, target_y):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    current_x = 0
    current_y = 0
    steps = 10

    canvas.font = tk.font.Font(family="Montserrat", size=12, weight="bold")

    for i in range(steps):
        progress = (i + 1) / steps
        next_x = current_x + (target_x - current_x) * progress
        next_y = current_y + (target_y - current_y) * progress
        
        # Рисуем линию между текущей и следующей позицией
        canvas.create_line(current_x, current_y, next_x, next_y, fill="blue")

        # Создаем круг для отображения текущей позиции наконечника
        canvas.create_oval(next_x, next_y, next_x + 7, next_y + 7, fill="black")

        canvas.update()
        canvas.after(300)  # Задержка в миллисекундах

        current_x = next_x
        current_y = next_y

    # Добавляем текстовое сообщение о достижении целевой позиции
    canvas.create_text(300, 300, text="Измерительный наконечник\nдостиг целевой позиции", font=canvas.font, fill="black")