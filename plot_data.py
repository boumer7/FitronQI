import matplotlib.pyplot as plt
import sqlite3

def plot_data_from_db(file_path_db):

    conn = sqlite3.connect(file_path_db)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS measurements (measurement_id INTEGER PRIMARY KEY, length REAL, width REAL)")
    c.execute("SELECT * FROM measurements ORDER BY length ASC")

    rows = c.fetchall()

    c.execute("SELECT length FROM measurements LIMIT 1")
    first_length = c.fetchall()[0]
    print(first_length)
    
    lengths = [row[1] for row in rows]
    nums = list(range(1, len(lengths) + 1))

    plt.figure(figsize=(10, 6))
    
    plt.plot(nums, lengths, label='Длина (мм.)', color='blue', marker='o', linestyle='-')
    
    plt.axhline(y=first_length, color='black', linestyle='--', label='Значение эталона')

    plt.title('График длины пластины с координатно-измерительной машины')
    plt.xlabel('Длина (мм)')
    plt.ylabel('Ширина (мм)') 
    plt.legend()
    
    plt.show()

    conn.close()