import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sqlite3
from matplotlib.widgets import Button

conn = sqlite3.connect('temperature_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS temperature_data 
             (timestamp TEXT, temperature INTEGER)''')

def save_to_db(timestamp, temperature):
    c.execute("INSERT INTO temperature_data (timestamp, temperature) VALUES (?, ?)", (timestamp, temperature))
    conn.commit()

def close_and_save(event):
    global times, temperatures
    for i in range(len(times)):
        save_to_db(times[i], temperatures[i])
    conn.close()
    plt.close('all')
    plt.clf()

def manage_process():
    global times, temperatures
    fig, ax = plt.subplots()
    times = []
    temperatures = []

    stat_label = ax.text(0.02, 0.85, '', transform=ax.transAxes)

    button_ax = plt.axes([0.81, 0.9, 0.1, 0.05])
    close_save_btn = Button(button_ax, 'Закрыть и сохранить')
    close_save_btn.on_clicked(close_and_save)

    def update_plot(frame):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")  
        if not times:
            times.append(current_time)
            temperatures.append(random.randint(10, 50))
        else:
            new_time = datetime.datetime.now().strftime("%H:%M:%S")
            if new_time != times[-1]:
                temperature = temperatures[-1] + random.randint(-5, 5)
                temperature = max(10, min(temperature, 50))
                times.append(new_time)
                temperatures.append(temperature)

        mean_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        median_temp = sorted(temperatures)[len(temperatures)//2] if len(temperatures) % 2 != 0 else (sorted(temperatures)[len(temperatures)//2-1] + sorted(temperatures)[len(temperatures)//2]) / 2

        stat_label.set_text(f'Средняя температура: {mean_temp:.2f}°C\n'
                            f'Максимальная температура: {max_temp}°C\n'
                            f'Минимальная температура: {min_temp}°C\n'
                            f'Медиана температуры: {median_temp}°C')

        ax.plot(times[-10:], temperatures[-10:], marker='o', color='b')
        ax.set_xlabel('Время (сек.)')
        ax.set_ylabel('Температура (°C)')
        ax.set_title('Симуляция изменения температуры в реальном времени с измерительной машины')

    ani = animation.FuncAnimation(fig, update_plot, interval=1000, save_count=len(times))

    plt.show()

    time.sleep(10)  

    conn.close()