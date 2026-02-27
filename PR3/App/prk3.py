import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from scipy import stats

class ReliabilityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет показателей надежности (Вариант 5)")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        
        # Заголовок
        title_label = ttk.Label(root, text="Расчет показателей надежности", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Вариант 5
        var_label = ttk.Label(root, text="Вариант 5: Среднее квадратическое отклонение ресурса = 400 часов, "
                              "коэффициент вариации = 0,3", font=("Arial", 10))
        var_label.pack(pady=5)
        
        # Основная рамка для ввода данных
        input_frame = ttk.LabelFrame(root, text="Исходные данные", padding=10)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Среднее квадратическое отклонение
        ttk.Label(input_frame, text="Среднее квадратическое отклонение (часы):").grid(
            row=0, column=0, sticky="w", pady=5)
        self.sigma_var = tk.StringVar(value="400")
        sigma_entry = ttk.Entry(input_frame, textvariable=self.sigma_var, width=15)
        sigma_entry.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        
        # Коэффициент вариации
        ttk.Label(input_frame, text="Коэффициент вариации (0-1):").grid(
            row=1, column=0, sticky="w", pady=5)
        self.vx_var = tk.StringVar(value="0.3")
        vx_entry = ttk.Entry(input_frame, textvariable=self.vx_var, width=15)
        vx_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        
        # Расчет средней наработки
        calc_button = ttk.Button(input_frame, text="Рассчитать среднюю наработку", 
                                  command=self.calculate_mean)
        calc_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Средняя наработка (результат)
        ttk.Label(input_frame, text="Средняя наработка на отказ (часы):").grid(
            row=3, column=0, sticky="w", pady=5)
        self.mean_var = tk.StringVar(value="1333.33")
        mean_label = ttk.Label(input_frame, textvariable=self.mean_var, 
                                font=("Arial", 10, "bold"), foreground="blue")
        mean_label.grid(row=3, column=1, sticky="w", pady=5)
        
        # Рамка для ввода наработок
        time_frame = ttk.LabelFrame(root, text="Ввод наработок для расчета", padding=10)
        time_frame.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(time_frame, text="Наработка t1 (часы):").grid(row=0, column=0, sticky="w", pady=5)
        self.t1_var = tk.StringVar(value="1000")
        t1_entry = ttk.Entry(time_frame, textvariable=self.t1_var, width=15)
        t1_entry.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        
        ttk.Label(time_frame, text="Наработка t2 (часы):").grid(row=1, column=0, sticky="w", pady=5)
        self.t2_var = tk.StringVar(value="2000")
        t2_entry = ttk.Entry(time_frame, textvariable=self.t2_var, width=15)
        t2_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        
        ttk.Label(time_frame, text="Наработка t3 (часы):").grid(row=2, column=0, sticky="w", pady=5)
        self.t3_var = tk.StringVar(value="3000")
        t3_entry = ttk.Entry(time_frame, textvariable=self.t3_var, width=15)
        t3_entry.grid(row=2, column=1, sticky="w", pady=5, padx=10)
        
        # Кнопка расчета
        calc_all_button = ttk.Button(root, text="РАССЧИТАТЬ ПОКАЗАТЕЛИ НАДЕЖНОСТИ", 
                                      command=self.calculate_reliability, 
                                      style="Accent.TButton")
        calc_all_button.pack(pady=20)
        
        # Рамка для результатов
        result_frame = ttk.LabelFrame(root, text="Результаты расчета", padding=10)
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Создаем текстовое поле для вывода результатов с прокруткой
        self.result_text = tk.Text(result_frame, height=15, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к расчетам")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Стиль для кнопки
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 11, "bold"))
        
        # Выполним начальный расчет для отображения результатов
        self.calculate_reliability()
    
    def calculate_mean(self):
        """Расчет средней наработки по формуле M = sigma / vx"""
        try:
            sigma = float(self.sigma_var.get())
            vx = float(self.vx_var.get())
            
            if vx <= 0:
                messagebox.showerror("Ошибка", "Коэффициент вариации должен быть больше 0")
                return
            
            mean_value = sigma / vx
            self.mean_var.set(f"{mean_value:.2f}")
            self.status_var.set(f"Средняя наработка рассчитана: {mean_value:.2f} часов")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def calculate_reliability(self):
        """Расчет всех показателей надежности"""
        try:
            # Получаем исходные данные
            sigma = float(self.sigma_var.get())
            vx = float(self.vx_var.get())
            
            if sigma <= 0 or vx <= 0:
                messagebox.showerror("Ошибка", "Значения должны быть положительными")
                return
            
            # Рассчитываем среднюю наработку
            mean_value = sigma / vx
            self.mean_var.set(f"{mean_value:.2f}")
            
            # Получаем значения наработок
            t1 = float(self.t1_var.get())
            t2 = float(self.t2_var.get())
            t3 = float(self.t3_var.get())
            
            times = [t1, t2, t3]
            
            # Очищаем текстовое поле
            self.result_text.delete(1.0, tk.END)
            
            # Заголовок результатов
            self.result_text.insert(tk.END, "="*70 + "\n")
            self.result_text.insert(tk.END, "РАСЧЕТ ПОКАЗАТЕЛЕЙ НАДЕЖНОСТИ (ВАРИАНТ 5)\n")
            self.result_text.insert(tk.END, "="*70 + "\n\n")
            
            # Исходные данные
            self.result_text.insert(tk.END, "ИСХОДНЫЕ ДАННЫЕ:\n")
            self.result_text.insert(tk.END, f"• Среднее квадратическое отклонение (σ): {sigma:.2f} часов\n")
            self.result_text.insert(tk.END, f"• Коэффициент вариации (vx): {vx:.3f}\n")
            self.result_text.insert(tk.END, f"• Средняя наработка на отказ (M): {mean_value:.2f} часов\n")
            self.result_text.insert(tk.END, f"• Закон распределения: нормальный\n\n")
            
            # Расчет для каждого значения наработки
            self.result_text.insert(tk.END, "РЕЗУЛЬТАТЫ РАСЧЕТА:\n")
            self.result_text.insert(tk.END, "-"*70 + "\n")
            
            for i, t in enumerate(times, 1):
                self.result_text.insert(tk.END, f"\nДЛЯ НАРАБОТКИ t{i} = {t:.0f} часов:\n")
                self.result_text.insert(tk.END, "-"*50 + "\n")
                
                # Квантиль нормированного нормального распределения
                u = (t - mean_value) / sigma
                
                # Функция Лапласа (нормированная функция распределения)
                # Используем функцию распределения нормального закона
                phi = stats.norm.cdf(u)
                
                # Вероятность отказа Q(t)
                q = phi
                
                # Вероятность безотказной работы P(t)
                p = 1 - q
                
                # Частота отказов f(t) - плотность вероятности
                f = stats.norm.pdf(u) / sigma  # делим на sigma для корректной плотности
                
                # Интенсивность отказов λ(t)
                lambda_t = f / p if p > 0 else float('inf')
                
                # Вывод результатов
                self.result_text.insert(tk.END, f"Квантиль Up: {u:.4f}\n")
                self.result_text.insert(tk.END, f"Функция Лапласа Ф(Up): {phi:.6f}\n\n")
                
                self.result_text.insert(tk.END, f"Вероятность отказа Q(t) = Ф(Up) = {q:.6f}\n")
                self.result_text.insert(tk.END, f"или {q*100:.2f}%\n\n")
                
                self.result_text.insert(tk.END, f"Вероятность безотказной работы P(t) = 1 - Q(t) = {p:.6f}\n")
                self.result_text.insert(tk.END, f"или {p*100:.2f}%\n\n")
                
                self.result_text.insert(tk.END, f"Частота отказов f(t): {f:.8f} 1/час\n")
                
                if lambda_t != float('inf'):
                    self.result_text.insert(tk.END, f"Интенсивность отказов λ(t): {lambda_t:.8f} 1/час\n")
                else:
                    self.result_text.insert(tk.END, f"Интенсивность отказов λ(t): бесконечность\n")
                
                self.result_text.insert(tk.END, "-"*50 + "\n")
            
            # Дополнительная информация
            self.result_text.insert(tk.END, "\n" + "="*70 + "\n")
            self.result_text.insert(tk.END, "ПОЯСНЕНИЯ:\n")
            self.result_text.insert(tk.END, "• При нормальном законе распределения:\n")
            self.result_text.insert(tk.END, "  Q(t) = Ф((t - M)/σ) - вероятность отказа\n")
            self.result_text.insert(tk.END, "  P(t) = 1 - Q(t) - вероятность безотказной работы\n")
            self.result_text.insert(tk.END, "  f(t) = φ((t-M)/σ)/σ - частота отказов\n")
            self.result_text.insert(tk.END, "  λ(t) = f(t)/P(t) - интенсивность отказов\n")
            self.result_text.insert(tk.END, "="*70 + "\n")
            
            self.status_var.set(f"Расчет выполнен успешно для t = {t1}, {t2}, {t3} часов")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

def main():
    root = tk.Tk()
    app = ReliabilityCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()