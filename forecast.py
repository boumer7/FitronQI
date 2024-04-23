import tkinter as tk
import sqlite3
from configparser import ConfigParser
from gigachat import GigaChat
import decimal

def predict_temperature():
    # Чтение конфигурационного файла
    config = ConfigParser()
    config.read('config.ini')
    gigachat_auth = config.get('gigachat', 'token')

    # Подключение к БД
    conn = sqlite3.connect('measurement_results.db')
    c = conn.cursor()

    c.execute("SELECT * FROM measurements LIMIT 1")

    rows = c.fetchall()
    

    standard_length = rows[0][1]
    standard_width = rows[0][2]

    # Чтение последних 15 значений температуры из БД
    c.execute("SELECT * FROM measurements DESC LIMIT 15")
    rows = c.fetchall()

    lengths_dif = ['%.3f'%(row[1]-standard_length) for row in rows]
    widths_dif = ['%.3f'%(row[2]-standard_width) for row in rows]
    print(lengths_dif, '\n', widths_dif)

    lengths_dif_str = ', '.join(str(dif) for dif in lengths_dif)
    widths_dif_str = ', '.join(str(dif) for dif in widths_dif)

    with GigaChat(credentials=gigachat_auth, verify_ssl_certs=False) as giga:
        response_lengths = giga.chat(f"В вольной форме на основе следующего массива данных спрогнозируй следующее значение длины отклонения: {lengths_dif_str}")
        predicted_value_lengths = response_lengths.choices[0].message.content

        # response_widths = giga.chat(f"В вольной форме на основе следующего массива данных спрогнозируй следующее значение ширины отклонения: {widths_dif_str}")
        # predicted_value_widths = response_widths.choices[0].message.content

        # Создаем окно tkinter и выводим результат
        root = tk.Tk()
        root.title("Прогнозирование следующего отклонения от нормы на основе ИИ Сбера")
        root.minsize(300, 400)
        root.configure(bg='#FFD859')

        # Создаем стиль для текста Montserrat
        style = tk.font.Font(family="Montserrat", size=14, weight="bold")

        result_label = tk.Label(root, text=f"Прогнозируемое значение длины:\n{predicted_value_lengths}", bg='#FFD859', font=style, wraplength=400)
        result_label.pack(padx=20, pady=20)

        # result_label = tk.Label(root, text=f"Прогнозируемое значение ширины:\n{predicted_value_widths}", bg='#FFD859', font=style, wraplength=400)
        # result_label.pack(padx=20, pady=20)

        root.mainloop()
