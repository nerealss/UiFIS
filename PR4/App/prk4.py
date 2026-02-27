import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TechUtilizationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет коэффициента технического использования (Вариант 5)")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        # Заголовок
        title_label = ttk.Label(root, text="Расчет комплексных показателей надежности", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Вариант 5
        var_label = ttk.Label(root, 
                              text="Вариант 5: Система с периодическим ТО. T = 1000 ч, Tв = 10 ч, Tто = 2 ч, rто = 100 ч",
                              font=("Arial", 10), foreground="blue")
        var_label.pack(pady=5)
        
        # Основная рамка для ввода данных
        input_frame = ttk.LabelFrame(root, text="Исходные данные", padding=15)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Средняя наработка на отказ
        ttk.Label(input_frame, text="Средняя наработка на отказ T (часы):").grid(
            row=0, column=0, sticky="w", pady=8)
        self.t_var = tk.StringVar(value="1000")
        t_entry = ttk.Entry(input_frame, textvariable=self.t_var, width=15, font=("Arial", 10))
        t_entry.grid(row=0, column=1, sticky="w", pady=8, padx=10)
        
        # Среднее время восстановления
        ttk.Label(input_frame, text="Среднее время восстановления Tв (часы):").grid(
            row=1, column=0, sticky="w", pady=8)
        self.tb_var = tk.StringVar(value="10")
        tb_entry = ttk.Entry(input_frame, textvariable=self.tb_var, width=15, font=("Arial", 10))
        tb_entry.grid(row=1, column=1, sticky="w", pady=8, padx=10)
        
        # Средняя продолжительность ТО
        ttk.Label(input_frame, text="Средняя продолжительность ТО Tто (часы):").grid(
            row=2, column=0, sticky="w", pady=8)
        self.tto_var = tk.StringVar(value="2")
        tto_entry = ttk.Entry(input_frame, textvariable=self.tto_var, width=15, font=("Arial", 10))
        tto_entry.grid(row=2, column=1, sticky="w", pady=8, padx=10)
        
        # Период между ТО
        ttk.Label(input_frame, text="Период между ТО rто (часы):").grid(
            row=3, column=0, sticky="w", pady=8)
        self.rto_var = tk.StringVar(value="100")
        rto_entry = ttk.Entry(input_frame, textvariable=self.rto_var, width=15, font=("Arial", 10))
        rto_entry.grid(row=3, column=1, sticky="w", pady=8, padx=10)
        
        # Кнопка расчета
        calc_button = ttk.Button(input_frame, text="РАССЧИТАТЬ КОЭФФИЦИЕНТ ТЕХНИЧЕСКОГО ИСПОЛЬЗОВАНИЯ", 
                                  command=self.calculate_kti, style="Accent.TButton")
        calc_button.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Рамка для результатов
        result_frame = ttk.LabelFrame(root, text="Результаты расчета", padding=15)
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Создаем текстовое поле для вывода результатов с прокруткой
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=12, width=50, wrap=tk.WORD, 
                                    font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Рамка для графика
        plot_frame = ttk.Frame(result_frame)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Создаем фигуру для графика
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 6))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Введите данные и нажмите 'Рассчитать'")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Стиль для кнопки
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        
        # Выполним начальный расчет
        self.calculate_kti()
    
    def calculate_kti(self):
        """Расчет коэффициента технического использования"""
        try:
            # Получаем исходные данные
            T = float(self.t_var.get())
            Tb = float(self.tb_var.get())
            Tto = float(self.tto_var.get())
            rto = float(self.rto_var.get())
            
            # Проверка на положительные значения
            if T <= 0 or Tb <= 0 or Tto <= 0 or rto <= 0:
                messagebox.showerror("Ошибка", "Все значения должны быть положительными числами")
                return
            
            # Расчет интенсивностей
            lambda_rate = 1 / T  # интенсивность отказов
            mu_rate = 1 / Tb      # интенсивность восстановления
            
            # Расчет коэффициента готовности
            Kg = T / (T + Tb)
            
            # Расчет коэффициента простоя
            Kp = Tb / (T + Tb)
            
            # РАСЧЕТ КОЭФФИЦИЕНТА ТЕХНИЧЕСКОГО ИСПОЛЬЗОВАНИЯ
            # Полная формула с учетом периодичности ТО
            Kti_full = T / (T + Tb + (T * Tto) / rto)
            
            # Упрощенная формула (без учета периодичности)
            Kti_simple = T / (T + Tb + Tto)
            
            # Среднее количество отказов за период между ТО
            n_failures = T / rto
            
            # Среднее время восстановления за период с учетом ТО
            total_downtime = Tb * n_failures + Tto
            total_time = T + total_downtime
            Kti_alt = T / total_time  # альтернативный расчет для проверки
            
            # Расчет оптимального периода между ТО
            rto_opt = math.sqrt(2 * Tto * T)
            
            # Очищаем текстовое поле
            self.result_text.delete(1.0, tk.END)
            
            # Заголовок результатов
            self.result_text.insert(tk.END, "="*60 + "\n")
            self.result_text.insert(tk.END, "РАСЧЕТ КОЭФФИЦИЕНТА ТЕХНИЧЕСКОГО ИСПОЛЬЗОВАНИЯ\n")
            self.result_text.insert(tk.END, "="*60 + "\n\n")
            
            # Исходные данные
            self.result_text.insert(tk.END, "ИСХОДНЫЕ ДАННЫЕ:\n")
            self.result_text.insert(tk.END, "-"*40 + "\n")
            self.result_text.insert(tk.END, f"Средняя наработка на отказ T = {T:.2f} ч\n")
            self.result_text.insert(tk.END, f"Среднее время восстановления Tв = {Tb:.2f} ч\n")
            self.result_text.insert(tk.END, f"Средняя продолжительность ТО Tто = {Tto:.2f} ч\n")
            self.result_text.insert(tk.END, f"Период между ТО rто = {rto:.2f} ч\n\n")
            
            # Промежуточные расчеты
            self.result_text.insert(tk.END, "ПРОМЕЖУТОЧНЫЕ РАСЧЕТЫ:\n")
            self.result_text.insert(tk.END, "-"*40 + "\n")
            self.result_text.insert(tk.END, f"Интенсивность отказов λ = 1/T = {lambda_rate:.6f} 1/ч\n")
            self.result_text.insert(tk.END, f"Интенсивность восстановления μ = 1/Tв = {mu_rate:.6f} 1/ч\n")
            self.result_text.insert(tk.END, f"Коэффициент готовности Kг = T/(T+Tв) = {Kg:.6f}\n")
            self.result_text.insert(tk.END, f"Коэффициент простоя Kп = Tв/(T+Tв) = {Kp:.6f}\n")
            self.result_text.insert(tk.END, f"Среднее число отказов за период ТО = T/rто = {n_failures:.4f}\n\n")
            
            # Основные результаты
            self.result_text.insert(tk.END, "РЕЗУЛЬТАТЫ РАСЧЕТА:\n")
            self.result_text.insert(tk.END, "-"*40 + "\n")
            
            self.result_text.insert(tk.END, "ПОЛНАЯ ФОРМУЛА (с учетом периодичности ТО):\n")
            self.result_text.insert(tk.END, f"Kти = T / (T + Tв + (T × Tто)/rто) = \n")
            self.result_text.insert(tk.END, f"     = {T:.2f} / ({T:.2f} + {Tb:.2f} + ({T:.2f} × {Tto:.2f})/{rto:.2f})\n")
            self.result_text.insert(tk.END, f"     = {Kti_full:.8f}\n")
            self.result_text.insert(tk.END, f"     = {Kti_full*100:.4f}%\n\n")
            
            self.result_text.insert(tk.END, "УПРОЩЕННАЯ ФОРМУЛА (без учета периодичности):\n")
            self.result_text.insert(tk.END, f"Kти(упр) = T / (T + Tв + Tто) = \n")
            self.result_text.insert(tk.END, f"         = {T:.2f} / ({T:.2f} + {Tb:.2f} + {Tto:.2f})\n")
            self.result_text.insert(tk.END, f"         = {Kti_simple:.8f}\n")
            self.result_text.insert(tk.END, f"         = {Kti_simple*100:.4f}%\n\n")
            
            self.result_text.insert(tk.END, f"Разница между формулами: {abs(Kti_full - Kti_simple)*100:.4f}%\n\n")
            
            self.result_text.insert(tk.END, "ОПТИМАЛЬНЫЙ ПЕРИОД МЕЖДУ ТО:\n")
            self.result_text.insert(tk.END, f"rто(опт) = √(2 × Tто × T) = √(2 × {Tto:.2f} × {T:.2f}) = {rto_opt:.2f} ч\n")
            self.result_text.insert(tk.END, f"Текущий период rто = {rto:.2f} ч\n")
            
            if rto < rto_opt:
                self.result_text.insert(tk.END, "▶ Рекомендуется увеличить период между ТО\n")
            elif rto > rto_opt:
                self.result_text.insert(tk.END, "▶ Рекомендуется уменьшить период между ТО\n")
            else:
                self.result_text.insert(tk.END, "✓ Период между ТО оптимальный\n")
            
            # Обновляем графики
            self.update_plots(T, Tb, Tto, rto, Kti_full, Kg)
            
            self.status_var.set(f"Расчет выполнен. Kти = {Kti_full*100:.2f}%")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def update_plots(self, T, Tb, Tto, rto, Kti, Kg):
        """Обновление графиков"""
        # Очищаем оси
        self.ax1.clear()
        self.ax2.clear()
        
        # График 1: Зависимость Kти от периода ТО
        r_values = np.linspace(10, 500, 100)
        kti_values = T / (T + Tb + (T * Tto) / r_values)
        
        self.ax1.plot(r_values, kti_values * 100, 'b-', linewidth=2, label='Kти(rто)')
        self.ax1.axhline(y=Kg*100, color='r', linestyle='--', label=f'Kг = {Kg*100:.1f}%')
        self.ax1.axvline(x=rto, color='g', linestyle='--', label=f'Текущий rто = {rto:.0f}')
        
        # Оптимальная точка
        rto_opt = math.sqrt(2 * Tto * T)
        kti_opt = T / (T + Tb + (T * Tto) / rto_opt)
        self.ax1.plot(rto_opt, kti_opt * 100, 'ro', markersize=8, label=f'Оптимум: rто={rto_opt:.0f}')
        
        self.ax1.set_xlabel('Период между ТО rто (часы)')
        self.ax1.set_ylabel('Kти, %')
        self.ax1.set_title('Зависимость Kти от периода ТО')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(loc='best')
        self.ax1.set_ylim([90, 100])
        
        # График 2: Сравнение коэффициентов
        categories = ['Kг', 'Kти (полн)', 'Kти (упр)']
        values = [Kg * 100, Kti * 100, (T / (T + Tb + Tto)) * 100]
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        bars = self.ax2.bar(categories, values, color=colors, alpha=0.7)
        self.ax2.set_ylabel('Значение, %')
        self.ax2.set_title('Сравнение коэффициентов')
        self.ax2.set_ylim([90, 100])
        
        # Добавляем значения на столбцы
        for bar, val in zip(bars, values):
            height = bar.get_height()
            self.ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                         f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')
        
        self.ax2.grid(True, alpha=0.3, axis='y')
        
        # Обновляем канву
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = TechUtilizationCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()