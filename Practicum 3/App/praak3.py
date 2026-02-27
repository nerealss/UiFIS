import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MotionAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор механического движения")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Переменные для ввода
        self.v0_var = tk.StringVar(value="0")
        self.a_var = tk.StringVar(value="0")
        self.t_var = tk.StringVar(value="10")
        
        # Переменные для результатов
        self.motion_type_var = tk.StringVar(value="—")
        self.path_var = tk.StringVar(value="—")
        self.final_velocity_var = tk.StringVar(value="—")
        self.description_var = tk.StringVar(value="—")
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Создание графика
        self.setup_plot()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 11, "bold"))
        style.configure("Result.TLabel", font=("Arial", 11))
        style.configure("Value.TLabel", font=("Arial", 11, "bold"), foreground="blue")
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="📊 Анализатор механического движения", 
                                 style="Title.TLabel")
        title_label.pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - ввод данных и результаты
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Рамка для входных данных
        input_frame = ttk.LabelFrame(left_frame, text="Входные данные", padding=15)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Начальная скорость
        v0_frame = ttk.Frame(input_frame)
        v0_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(v0_frame, text="Начальная скорость v₀ (м/с):", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        v0_entry = ttk.Entry(v0_frame, textvariable=self.v0_var, width=10, 
                              font=("Arial", 11), justify=tk.RIGHT)
        v0_entry.pack(side=tk.RIGHT)
        v0_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Ускорение
        a_frame = ttk.Frame(input_frame)
        a_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(a_frame, text="Ускорение a (м/с²):", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        a_entry = ttk.Entry(a_frame, textvariable=self.a_var, width=10, 
                             font=("Arial", 11), justify=tk.RIGHT)
        a_entry.pack(side=tk.RIGHT)
        a_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Время движения
        t_frame = ttk.Frame(input_frame)
        t_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(t_frame, text="Время движения t (с):", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        t_entry = ttk.Entry(t_frame, textvariable=self.t_var, width=10, 
                             font=("Arial", 11), justify=tk.RIGHT)
        t_entry.pack(side=tk.RIGHT)
        t_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Кнопки управления
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.calc_btn = ttk.Button(btn_frame, text="Рассчитать", 
                                     command=self.calculate_motion,
                                     style="Action.TButton")
        self.calc_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="Очистить", 
                                      command=self.clear_fields,
                                      style="Action.TButton")
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Рамка для результатов
        result_frame = ttk.LabelFrame(left_frame, text="Результаты", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Тип движения
        type_frame = ttk.Frame(result_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Тип движения:", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        self.type_label = ttk.Label(type_frame, textvariable=self.motion_type_var,
                                      style="Value.TLabel")
        self.type_label.pack(side=tk.RIGHT)
        
        # Пройденный путь
        path_frame = ttk.Frame(result_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="Пройденный путь S (м):", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        self.path_label = ttk.Label(path_frame, textvariable=self.path_var,
                                      style="Value.TLabel")
        self.path_label.pack(side=tk.RIGHT)
        
        # Конечная скорость
        vel_frame = ttk.Frame(result_frame)
        vel_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(vel_frame, text="Конечная скорость v (м/с):", 
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        self.vel_label = ttk.Label(vel_frame, textvariable=self.final_velocity_var,
                                     style="Value.TLabel")
        self.vel_label.pack(side=tk.RIGHT)
        
        # Разделитель
        ttk.Separator(result_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Описание движения
        ttk.Label(result_frame, text="Описание движения:", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=5)
        
        self.desc_label = ttk.Label(result_frame, textvariable=self.description_var,
                                      style="Result.TLabel", wraplength=300)
        self.desc_label.pack(anchor=tk.W, pady=5)
        
        # Правая панель - график
        right_frame = ttk.LabelFrame(main_frame, text="График зависимости пути от времени S(t)", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Создаем фигуру для графика
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Уравнение движения
        self.equation_var = tk.StringVar(value="S(t) = 0·t + 0·t²/2")
        equation_label = ttk.Label(right_frame, textvariable=self.equation_var,
                                     font=("Arial", 11, "italic"), foreground="blue")
        equation_label.pack(pady=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе. Введите данные и нажмите 'Рассчитать'")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Привязка событий
        self.root.bind('<Return>', lambda e: self.calculate_motion())
        
        # Начальный расчет
        self.calculate_motion()
        
    def setup_plot(self):
        """Настройка графика"""
        self.ax.set_xlabel('Время t (с)')
        self.ax.set_ylabel('Путь S (м)')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        
    def on_input_change(self, event=None):
        """Обработка изменения полей ввода"""
        # Можно добавить автоматический расчет при изменении
        pass
        
    def calculate_motion(self):
        """Расчет параметров движения"""
        try:
            # Получаем значения
            v0 = float(self.v0_var.get())
            a = float(self.a_var.get())
            t = float(self.t_var.get())
            
            # Проверка корректности времени
            if t < 0:
                messagebox.showerror("Ошибка", "Время не может быть отрицательным!")
                return
                
            if t == 0:
                self.path_var.set("0.00")
                self.final_velocity_var.set(f"{v0:.2f}")
                self.motion_type_var.set("Мгновенное состояние")
                self.description_var.set("Время движения равно нулю. Тело находится в начальной точке.")
                self.equation_var.set(f"S(t) = {v0}·t + {a}·t²/2")
                self.update_plot(v0, a, t)
                self.status_var.set("Время равно нулю - показано начальное состояние")
                return
            
            # Расчет пути и конечной скорости
            path = v0 * t + (a * t**2) / 2
            final_v = v0 + a * t
            
            # Путь не может быть отрицательным (это длина траектории)
            path = abs(path)
            
            # Форматируем результаты
            self.path_var.set(f"{path:.2f}")
            self.final_velocity_var.set(f"{final_v:.2f}")
            
            # Определяем тип движения
            motion_type = self.determine_motion_type(v0, a, final_v, t)
            self.motion_type_var.set(motion_type)
            
            # Формируем описание
            description = self.generate_description(v0, a, t, path, final_v)
            self.description_var.set(description)
            
            # Формируем уравнение
            a_sign = "+" if a >= 0 else "-"
            a_abs = abs(a)
            self.equation_var.set(f"S(t) = {v0}·t {a_sign} {a_abs}·t²/2")
            
            # Обновляем график
            self.update_plot(v0, a, t)
            
            self.status_var.set("Расчет выполнен успешно")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
            
    def determine_motion_type(self, v0, a, final_v, t):
        """Определение типа движения"""
        if a == 0:
            if v0 == 0:
                return "Состояние покоя"
            else:
                return "Равномерное прямолинейное движение"
        elif a > 0:
            if v0 == 0:
                return "Равноускоренное движение из состояния покоя"
            else:
                return "Равноускоренное движение"
        else:  # a < 0
            if final_v > 0:
                return "Равнозамедленное движение"
            elif final_v == 0:
                return "Остановка в конце движения"
            else:
                return "Равнозамедленное движение (смена направления)"
    
    def generate_description(self, v0, a, t, path, final_v):
        """Генерация описания движения"""
        description = []
        
        if a == 0:
            if v0 == 0:
                description.append("Тело находится в состоянии покоя.")
            else:
                description.append(f"Тело движется равномерно со скоростью {v0:.2f} м/с.")
                description.append(f"За время {t:.2f} с тело прошло путь {path:.2f} м.")
        elif a > 0:
            description.append(f"Тело движется равноускоренно с ускорением {a:.2f} м/с².")
            if v0 == 0:
                description.append("Движение начинается из состояния покоя.")
            else:
                description.append(f"Начальная скорость составляет {v0:.2f} м/с.")
            description.append(f"К концу движения скорость увеличится до {final_v:.2f} м/с.")
            description.append(f"За время {t:.2f} с пройден путь {path:.2f} м.")
        else:  # a < 0
            abs_a = abs(a)
            stop_time = v0 / abs_a
            
            if t < stop_time:
                description.append(f"Тело движется равнозамедленно с ускорением {a:.2f} м/с².")
                description.append(f"Начальная скорость {v0:.2f} м/с к концу движения")
                description.append(f"уменьшится до {final_v:.2f} м/с.")
                description.append(f"До полной остановки осталось {stop_time - t:.2f} с.")
            elif t == stop_time:
                description.append(f"Тело двигалось равнозамедленно и остановилось в конце пути.")
                description.append(f"Время торможения составило {stop_time:.2f} с.")
                description.append(f"Тормозной путь равен {path:.2f} м.")
            else:
                description.append(f"Тело остановилось через {stop_time:.2f} с,")
                description.append(f"после чего начало движение в обратном направлении.")
                description.append(f"К моменту времени {t:.2f} с скорость составляет {final_v:.2f} м/с")
                description.append(f"в направлении, противоположном начальному.")
        
        return "\n".join(description)
    
    def update_plot(self, v0, a, t_max):
        """Обновление графика"""
        self.ax.clear()
        
        # Генерируем точки времени
        t = np.linspace(0, t_max, 100)
        
        # Рассчитываем путь для каждого момента времени
        # S = v0*t + (a*t^2)/2, но путь всегда положительный
        s = v0 * t + (a * t**2) / 2
        s = np.abs(s)  # путь - это модуль
        
        # Строим график
        self.ax.plot(t, s, 'b-', linewidth=2, label='S(t)')
        
        # Отмечаем ключевые точки
        self.ax.plot(0, abs(v0 * 0 + (a * 0**2) / 2), 'ro', markersize=8)  # начальная точка
        self.ax.plot(t_max, abs(v0 * t_max + (a * t_max**2) / 2), 'ro', markersize=8)  # конечная точка
        
        # Если есть торможение до остановки и время больше времени остановки
        if a < 0:
            stop_time = v0 / abs(a)
            if 0 < stop_time < t_max:
                stop_path = abs(v0 * stop_time + (a * stop_time**2) / 2)
                self.ax.plot(stop_time, stop_path, 'go', markersize=8, label='Момент остановки')
        
        # Настройка графика
        self.ax.set_xlabel('Время t (с)')
        self.ax.set_ylabel('Путь S (м)')
        self.ax.set_title('Зависимость пути от времени')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.legend()
        
        # Обновляем канву
        self.canvas.draw()
    
    def clear_fields(self):
        """Очистка полей ввода и результатов"""
        self.v0_var.set("0")
        self.a_var.set("0")
        self.t_var.set("10")
        
        self.motion_type_var.set("—")
        self.path_var.set("—")
        self.final_velocity_var.set("—")
        self.description_var.set("—")
        self.equation_var.set("S(t) = 0·t + 0·t²/2")
        
        self.update_plot(0, 0, 10)
        
        self.status_var.set("Поля очищены")

def main():
    root = tk.Tk()
    app = MotionAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()