import tkinter as tk
import sqlite3
from configparser import ConfigParser
from gigachat import GigaChat

def predict_temperature():
    # Чтение конфигурационного файла
    config = ConfigParser()
    config.read('config.ini')
    gigachat_auth = config.get('gigachat', 'token')

    # Подключение к БД
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()

    # Чтение последних 20 значений температуры из БД
    c.execute("SELECT * FROM temperature_data ORDER BY timestamp DESC LIMIT 15")
    rows = c.fetchall()
    temperatures = [row[1] for row in rows]

    # Строка для запроса к ИИ
    array_str = ', '.join(str(temp) for temp in temperatures)

    with GigaChat(credentials=gigachat_auth, verify_ssl_certs=False) as giga:
        response = giga.chat(f"На основе следующего массива данных спрогнозируй следующее значение температуры изделия, без лишних вопросов, уточнения и без кода. Мне нужно просто значение и краткое обоснование: {array_str}")
        predicted_temp = response.choices[0].message.content

        # Создаем окно tkinter и выводим результат
        root = tk.Tk()
        root.title("Прогнозирование следующей температуры на основе ИИ Сбера")
        root.minsize(300, 400)
        root.configure(bg='#FFD859')

        # Создаем стиль для текста Montserrat
        style = tk.font.Font(family="Montserrat", size=14, weight="bold")

        result_label = tk.Label(root, text=f"Прогнозируемое значение температуры:\n{predicted_temp}", bg='#FFD859', font=style, wraplength=400)
        result_label.pack(padx=20, pady=20)

        root.mainloop()
