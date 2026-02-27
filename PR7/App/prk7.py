import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ReliabilityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет показателей достоверности информации (Вариант 5)")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Заголовок
        title_label = ttk.Label(root, text="Определение единичных показателей достоверности информации", 
                                 font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Вариант 5
        var_frame = ttk.Frame(root)
        var_frame.pack(fill=tk.X, padx=20)
        
        var_label = ttk.Label(var_frame, 
                              text="Вариант 5: Время коррекции ошибок (минуты): 5, 7, 6, 8, 10, 4, 9, 11, 7, 13",
                              font=("Arial", 10), foreground="blue")
        var_label.pack()
        
        # Основной контейнер
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - ввод данных
        left_frame = ttk.LabelFrame(main_container, text="Ввод данных", padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Поле для ввода времен коррекции
        ttk.Label(left_frame, text="Времена коррекции ошибок (минуты):", 
                  font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(left_frame, text="Введите числа через запятую или пробел:", 
                  font=("Arial", 9)).pack(anchor=tk.W)
        
        self.times_text = tk.Text(left_frame, height=8, width=40, font=("Consolas", 10))
        self.times_text.pack(fill=tk.X, pady=5)
        self.times_text.insert(tk.END, "5, 7, 6, 8, 10, 4, 9, 11, 7, 13")
        
        # Кнопки
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Рассчитать показатели", 
                   command=self.calculate, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Очистить", 
                   command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Пример", 
                   command=self.load_example).pack(side=tk.LEFT, padx=5)
        
        # Статистика
        stats_frame = ttk.LabelFrame(left_frame, text="Статистика", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=10, width=40, font=("Consolas", 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Правая панель - результаты и графики
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Результаты
        result_frame = ttk.LabelFrame(right_frame, text="Результаты расчета", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=15, font=("Consolas", 11))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # График
        plot_frame = ttk.LabelFrame(right_frame, text="Визуализация", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Создаем фигуру для графика
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 3))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к расчетам. Введите данные и нажмите 'Рассчитать'")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Стиль для кнопки
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        
        # Выполним начальный расчет
        self.calculate()
    
    def parse_times(self):
        """Парсит введенные времена коррекции"""
        text = self.times_text.get(1.0, tk.END).strip()
        
        # Заменяем запятые на пробелы и разбиваем
        text = text.replace(',', ' ')
        parts = text.split()
        
        times = []
        for part in parts:
            try:
                times.append(float(part))
            except ValueError:
                pass
        
        return times
    
    def calculate(self):
        """Расчет показателей достоверности"""
        try:
            times = self.parse_times()
            
            if len(times) == 0:
                messagebox.showerror("Ошибка", "Введите хотя бы одно значение времени коррекции")
                return
            
            # Основные статистические показатели
            n = len(times)  # количество ошибок
            sum_times = sum(times)  # суммарное время
            mean_time = sum_times / n  # среднее время коррекции Tи
            
            # Дополнительные статистические показатели
            sorted_times = sorted(times)
            min_time = min(times)
            max_time = max(times)
            median_time = sorted_times[n // 2] if n % 2 == 1 else (sorted_times[n//2 - 1] + sorted_times[n//2]) / 2
            
            # Дисперсия и среднеквадратическое отклонение
            variance = sum((t - mean_time) ** 2 for t in times) / n
            std_dev = math.sqrt(variance)
            
            # Коэффициент вариации
            cv = std_dev / mean_time if mean_time > 0 else 0
            
            # Доверительный интервал (для 95% доверительной вероятности)
            import scipy.stats as stats
            confidence = 0.95
            degrees_freedom = n - 1
            t_value = stats.t.ppf((1 + confidence) / 2, degrees_freedom)
            margin_error = t_value * (std_dev / math.sqrt(n))
            ci_lower = mean_time - margin_error
            ci_upper = mean_time + margin_error
            
            # Очищаем текстовые поля
            self.result_text.delete(1.0, tk.END)
            self.stats_text.delete(1.0, tk.END)
            
            # Вывод исходных данных
            self.stats_text.insert(tk.END, "ИСХОДНЫЕ ДАННЫЕ:\n")
            self.stats_text.insert(tk.END, "-" * 40 + "\n")
            self.stats_text.insert(tk.END, f"Количество ошибок: {n}\n")
            self.stats_text.insert(tk.END, f"Времена коррекции (мин):\n")
            
            # Выводим времена в несколько столбцов
            for i, t in enumerate(times):
                self.stats_text.insert(tk.END, f"{t:8.2f}")
                if (i + 1) % 5 == 0:
                    self.stats_text.insert(tk.END, "\n")
            self.stats_text.insert(tk.END, "\n\n")
            
            self.stats_text.insert(tk.END, "СТАТИСТИЧЕСКИЕ ПОКАЗАТЕЛИ:\n")
            self.stats_text.insert(tk.END, "-" * 40 + "\n")
            self.stats_text.insert(tk.END, f"Суммарное время: {sum_times:.2f} мин\n")
            self.stats_text.insert(tk.END, f"Минимальное время: {min_time:.2f} мин\n")
            self.stats_text.insert(tk.END, f"Максимальное время: {max_time:.2f} мин\n")
            self.stats_text.insert(tk.END, f"Медиана: {median_time:.2f} мин\n")
            self.stats_text.insert(tk.END, f"Дисперсия: {variance:.4f}\n")
            self.stats_text.insert(tk.END, f"Ср. кв. отклонение: {std_dev:.4f} мин\n")
            self.stats_text.insert(tk.END, f"Коэффициент вариации: {cv:.4f}\n")
            
            # Вывод результатов
            self.result_text.insert(tk.END, "=" * 60 + "\n")
            self.result_text.insert(tk.END, "РЕЗУЛЬТАТ РАСЧЕТА ПО ВАРИАНТУ 5\n")
            self.result_text.insert(tk.END, "=" * 60 + "\n\n")
            
            self.result_text.insert(tk.END, "ЗАДАНИЕ:\n")
            self.result_text.insert(tk.END, "В системе было зафиксировано 10 ошибок.\n")
            self.result_text.insert(tk.END, "Время на их идентификацию и исправление составило:\n")
            self.result_text.insert(tk.END, f"{', '.join([str(t) for t in times])} минут\n\n")
            
            self.result_text.insert(tk.END, "РЕШЕНИЕ:\n")
            self.result_text.insert(tk.END, "-" * 60 + "\n")
            
            self.result_text.insert(tk.END, "Среднее время коррекции информации Tи вычисляется по формуле:\n\n")
            self.result_text.insert(tk.END, "      1   N\n")
            self.result_text.insert(tk.END, "Tи = - * Σ ti\n")
            self.result_text.insert(tk.END, "      N  i=1\n\n")
            
            self.result_text.insert(tk.END, "где:\n")
            self.result_text.insert(tk.END, "N = 10 - количество ошибок\n")
            self.result_text.insert(tk.END, "ti - время коррекции i-й ошибки\n\n")
            
            self.result_text.insert(tk.END, "ПОДСТАНОВКА ЗНАЧЕНИЙ:\n")
            self.result_text.insert(tk.END, f"Tи = (1/10) * ({' + '.join([str(t) for t in times])})\n")
            self.result_text.insert(tk.END, f"Tи = (1/10) * {sum_times:.2f}\n\n")
            
            self.result_text.insert(tk.END, "РЕЗУЛЬТАТ:\n")
            self.result_text.insert(tk.END, "═" * 60 + "\n")
            self.result_text.insert(tk.END, f"Среднее время коррекции информации Tи = {mean_time:.2f} минут\n")
            self.result_text.insert(tk.END, "═" * 60 + "\n\n")
            
            self.result_text.insert(tk.END, "ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:\n")
            self.result_text.insert(tk.END, "-" * 60 + "\n")
            self.result_text.insert(tk.END, f"• Доверительный интервал (95%): [{ci_lower:.2f}; {ci_upper:.2f}] мин\n")
            self.result_text.insert(tk.END, f"• С вероятностью 95% истинное среднее время коррекции\n")
            self.result_text.insert(tk.END, f"  находится в указанном интервале\n")
            
            # Обновляем графики
            self.update_plots(times, mean_time, std_dev, ci_lower, ci_upper)
            
            self.status_var.set(f"Расчет выполнен. Среднее время коррекции: {mean_time:.2f} минут")
            
        except ImportError:
            # Если scipy не установлен, рассчитываем без доверительного интервала
            messagebox.showwarning("Предупреждение", 
                                   "Для расчета доверительного интервала установите библиотеку scipy\n"
                                   "pip install scipy")
            self.show_basic_results(times)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def show_basic_results(self, times):
        """Показывает базовые результаты без доверительного интервала"""
        n = len(times)
        sum_times = sum(times)
        mean_time = sum_times / n
        
        # Очищаем текстовые поля
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        self.result_text.insert(tk.END, "РЕЗУЛЬТАТ РАСЧЕТА ПО ВАРИАНТУ 5\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")
        
        self.result_text.insert(tk.END, f"Среднее время коррекции информации Tи = {mean_time:.2f} минут\n\n")
        self.result_text.insert(tk.END, f"(рассчитано по {n} значениям)\n")
    
    def update_plots(self, times, mean_time, std_dev, ci_lower, ci_upper):
        """Обновление графиков"""
        # Очищаем оси
        self.ax1.clear()
        self.ax2.clear()
        
        # График 1: Гистограмма распределения времен коррекции
        self.ax1.hist(times, bins=8, edgecolor='black', alpha=0.7, color='#3498db')
        self.ax1.axvline(x=mean_time, color='red', linestyle='--', linewidth=2, 
                         label=f'Среднее = {mean_time:.2f}')
        self.ax1.axvline(x=ci_lower, color='green', linestyle=':', linewidth=1.5, 
                         label=f'Дов. интервал')
        self.ax1.axvline(x=ci_upper, color='green', linestyle=':', linewidth=1.5)
        
        self.ax1.set_xlabel('Время коррекции (минуты)')
        self.ax1.set_ylabel('Частота')
        self.ax1.set_title('Распределение времен коррекции')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # График 2: Точечный график времен коррекции
        x = range(1, len(times) + 1)
        self.ax2.scatter(x, times, color='#e74c3c', s=50, alpha=0.7, label='Время коррекции')
        self.ax2.axhline(y=mean_time, color='blue', linestyle='--', linewidth=2, 
                         label=f'Среднее = {mean_time:.2f}')
        
        # Добавляем значения над точками
        for i, t in zip(x, times):
            self.ax2.annotate(f'{t:.1f}', (i, t), textcoords="offset points", 
                             xytext=(0,10), ha='center', fontsize=8)
        
        self.ax2.set_xlabel('Номер ошибки')
        self.ax2.set_ylabel('Время коррекции (минуты)')
        self.ax2.set_title('Времена коррекции по ошибкам')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_xticks(x)
        
        # Обновляем канву
        self.fig.tight_layout()
        self.canvas.draw()
    
    def clear_fields(self):
        """Очищает поля ввода"""
        self.times_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.status_var.set("Поля очищены")
        
        # Очищаем графики
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()
    
    def load_example(self):
        """Загружает пример из задания"""
        self.times_text.delete(1.0, tk.END)
        self.times_text.insert(tk.END, "5, 7, 6, 8, 10, 4, 9, 11, 7, 13")
        self.status_var.set("Загружен пример из варианта 5")
        self.calculate()

def main():
    root = tk.Tk()
    app = ReliabilityCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()