import tkinter as tk
from PIL import Image, ImageTk
from plot_data import plot_data_from_db
from data_processing import manage_process
from simulate_measurement import simulate_movement
from forecast import predict_temperature
from db_view import display_data

def open_control_panel():
    control_panel = tk.Toplevel()
    control_panel.title("Панель управления")
    control_panel.geometry("600x400")
    
    status_label = tk.Label(control_panel, text="КИМ m.era ZIRCON ULTRA 10128\nСтатус: Подключено", font=('Montserrat', 14))
    status_label.pack(pady=20)
    
    protocol_label = tk.Label(control_panel, text="Интерфейс: USB", font=('Montserrat', 14))
    protocol_label.pack()

def open_plot_window():
    plot_data_from_db('measurement_results.db')

def execute_selected_action(selected_action, target_x=None, target_y=None):
    print(selected_action)
    if selected_action == "manage_process":
        manage_process()
    elif selected_action == "connected_devices":
        open_control_panel()
    elif selected_action == "plot_data_file":
        open_plot_window()
    elif selected_action == 'predict_temperature':
        predict_temperature()
    elif selected_action == 'display_data':
        display_data()

def main():
    root = tk.Tk()
    root.title("FitronQI — управление процессом контроля качества")

    root.iconbitmap('img/icon.ico')
    root.geometry("800x600")
    root.configure(bg='#E8B91F')

    img = Image.open("img/logo.png")
    img = img.resize((img.width // 4, img.height // 4))
    img = ImageTk.PhotoImage(img)

    logo_label = tk.Label(image=img)
    logo_label.image = img
    logo_label.pack()

    actions = {
        "manage_process": "Управление процессом",
        "connected_devices": "Панель управления устройств",
        "plot_data_file": "Построение графика на основе данных из КИМ",
        "predict_temperature": "Прогноз размеров изделия от ИИ Сбера",
        "display_data": "Открыть БД"
    }

    for action_key, action_value in actions.items():
        btn_action = tk.Button(root, text=action_value, command=lambda action_key=action_key: execute_selected_action(action_key), bg="#FFD859", fg="#443A18", font=('Montserrat', 12, 'bold'), bd=0, activebackground='#FFD859', activeforeground='#B89C40', cursor='hand2')
        btn_action.pack(pady=10, ipadx=20, ipady=10)
        btn_action.bind("<Enter>", lambda e, b=btn_action: b.config(bg="#FFEC8B"))
        btn_action.bind("<Leave>", lambda e, b=btn_action: b.config(bg="#FFD859"))

    root.mainloop()

if __name__ == '__main__':
    main()
