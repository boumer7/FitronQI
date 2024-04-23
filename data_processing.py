import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sqlite3

def manage_process():

    num_plastin = 5
    conn = sqlite3.connect('measurement_results.db')
    c = conn.cursor()

    # Создаем таблицу для хранения результатов измерений
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                 (measurement_id INTEGER PRIMARY KEY,
                 length REAL,
                 width REAL)''')

    c.execute('''INSERT INTO measurements (measurement_id, length, width) VALUES (?, ?, ?)''', (0, 40, 18))

    def generate_random_value(base_value):
        return base_value + np.random.uniform(-0.03*base_value, 0.03*base_value)

    def update(frame, needle, black_x, black_y, measurement_text, L, W, cur_num):
        x = []
        y = []

        if frame <= L:
            x.append(frame)
            y.append(0)
        elif frame <= L + W:
            x.append(L)
            y.append(frame - L)
        elif frame <= 2 * L + W:
            x.append(L - (frame - (L + W)))
            y.append(W)
        else:
            x.append(0)
            y.append(2 * (L + W) - frame)

        needle.set_data(x, y) 

        black_x.append(x[-1])
        black_y.append(y[-1])

        needle_line.set_data(black_x, black_y)

        measurement_text.set_text(f'Текущая деталь №{cur_num}\nДлина (L): {L:.1f} мм.\nШирина (W): {W:.1f} мм.')



        return needle, needle_line, measurement_text

    fig, ax = plt.subplots()

    def end_measurement(ax):
        ax.clear()
        ax.text(0.5, 0.5, f"Измерение партии пластин из {num_plastin} шт. завершено!", ha='center', va='center', fontsize=16, transform=ax.transAxes)
        plt.show()
        conn.close()

    for i in range(num_plastin):
        ax.clear()
        ax.set_xlim(-2, 50)
        ax.set_ylim(-2, 20)
        
        L = generate_random_value(40)
        W = generate_random_value(18)

        # Сохраняем результаты измерений в базу данных
        c.execute("INSERT INTO measurements (length, width) VALUES (?, ?)", ('%.3f'%(L), '%.3f'%(W)))
        conn.commit()

        black_x = []
        black_y = []

        needle, = ax.plot([], [], 'ro') 
        needle_line, = ax.plot([], [], 'k-')
        measurement_text = ax.text(0.5, 1.05, '', ha='center', va='center', transform=ax.transAxes)

        for frame in np.linspace(0, 2 * (L + W), 100):
            update(frame, needle, black_x, black_y, measurement_text, L, W, i+1)

            plt.pause(0.024)

        # Генерация новых значений для следующего измерения
        L = generate_random_value(40)
        W = generate_random_value(18)

    end_measurement(ax)
