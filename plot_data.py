import pandas as pd
import matplotlib.pyplot as plt

def plot_data_from_file(file_path):
    data = pd.read_excel(file_path, engine='openpyxl')
    
    plt.figure(figsize=(8, 6))
    
    plt.plot(data['Time'], data['Temperature'], label='Temperature', color='blue', marker='o')
    
    plt.title('График температуры из контрольно-измерительной машины')
    plt.xlabel('Время')
    plt.ylabel('Температура') 
    plt.legend()
    
    plt.show()
