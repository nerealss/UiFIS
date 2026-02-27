import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import pandas as pd
from datetime import datetime
import os
import webbrowser

class ProcessQualityAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ индексов качества процессов")
        self.root.geometry("1000x700")
        
        # Переменные для ввода данных
        self.usl_var = tk.StringVar(value="10.5")
        self.lsl_var = tk.StringVar(value="9.5")
        self.mean_var = tk.StringVar(value="10.2")
        self.sigma_var = tk.StringVar(value="0.1")
        
        # Переменные результатов
        self.cp_var = tk.StringVar(value="0.000")
        self.cpk_var = tk.StringVar(value="0.000")
        self.status_var = tk.StringVar(value="Статус: Не рассчитано")
        
        # История расчетов
        self.history = []
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса с вкладками
        self.setup_tab_control()
        
        # Создание вкладок
        self.setup_calculator_tab()
        self.setup_plot_tab()
        self.setup_history_tab()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Header.TLabel", font=("Arial", 11, "bold"))
        style.configure("Result.TLabel", font=("Arial", 12, "bold"))
        style.configure("Calculate.TButton", font=("Arial", 10, "bold"))
        
    def setup_tab_control(self):
        """Создание вкладок"""
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_calculator_tab(self):
        """Создание вкладки калькулятора"""
        self.calc_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.calc_tab, text="📊 Калькулятор")
        
        # Заголовок
        title_label = ttk.Label(self.calc_tab, text="Анализ индексов качества процессов", 
                                 style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Левая панель - ввод данных
        input_frame = ttk.LabelFrame(self.calc_tab, text="Введите параметры процесса", padding=15)
        input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Поля ввода
        ttk.Label(input_frame, text="Верхняя граница допуска (ВГД):", 
                  style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.usl_var, width=15, 
                  font=("Arial", 11)).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Нижняя граница допуска (НГД):", 
                  style="Header.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.lsl_var, width=15, 
                  font=("Arial", 11)).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Среднее значение (μ):", 
                  style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.mean_var, width=15, 
                  font=("Arial", 11)).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Стандартное отклонение (σ):", 
                  style="Header.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.sigma_var, width=15, 
                  font=("Arial", 11)).grid(row=3, column=1, padx=10, pady=5)
        
        # Кнопки
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="📈 Рассчитать индексы качества", 
                   command=self.calculate_indices,
                   style="Calculate.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="💾 Сохранить в историю", 
                   command=self.save_to_history).pack(side=tk.LEFT, padx=5)
        
        # Правая панель - результаты
        result_frame = ttk.LabelFrame(self.calc_tab, text="Результаты анализа", padding=15)
        result_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        
        # Индексы
        ttk.Label(result_frame, text="Cp:", style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.cp_label = ttk.Label(result_frame, textvariable=self.cp_var, 
                                   font=("Arial", 14, "bold"), foreground="blue")
        self.cp_label.grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Label(result_frame, text="Cpk:", style="Header.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.cpk_label = ttk.Label(result_frame, textvariable=self.cpk_var, 
                                    font=("Arial", 14, "bold"), foreground="blue")
        self.cpk_label.grid(row=1, column=1, sticky="w", padx=10)
        
        # Статус
        ttk.Label(result_frame, text="Статус:", style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.status_label = ttk.Label(result_frame, textvariable=self.status_var, 
                                       font=("Arial", 12, "bold"))
        self.status_label.grid(row=2, column=1, sticky="w", padx=10)
        
        # Интерпретация
        interp_frame = ttk.LabelFrame(result_frame, text="Интерпретация", padding=10)
        interp_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")
        
        interp_text = """
        Cp ≥ 1.33, Cpk ≥ 1.33 – Отлично
        Cp ≥ 1.0, Cpk ≥ 1.0 – Удовлетворительно
        Cp ≥ 0.67, Cpk ≥ 0.67 – Неудовлетворительно
        Cp < 0.67, Cpk < 0.67 – Критично
        """
        ttk.Label(interp_frame, text=interp_text, font=("Arial", 9)).pack()
        
        # Кнопки экспорта
        export_frame = ttk.Frame(result_frame)
        export_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(export_frame, text="📊 Экспорт в Excel", 
                   command=self.export_to_excel).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📄 Экспорт в PDF", 
                   command=self.export_to_pdf).pack(side=tk.LEFT, padx=5)
        
        # Настройка весов колонок
        self.calc_tab.grid_columnconfigure(0, weight=1)
        self.calc_tab.grid_columnconfigure(1, weight=1)
        
    def setup_plot_tab(self):
        """Создание вкладки с графиком"""
        self.plot_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.plot_tab, text="📈 График распределения")
        
        # Создаем фигуру для графика
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопка обновления графика
        ttk.Button(self.plot_tab, text="🔄 Обновить график", 
                   command=self.update_plot).pack(pady=5)
        
    def setup_history_tab(self):
        """Создание вкладки с историей расчетов"""
        self.history_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.history_tab, text="📋 История расчетов")
        
        # Таблица истории
        columns = ("date", "usl", "lsl", "mean", "sigma", "cp", "cpk", "status")
        self.history_tree = ttk.Treeview(self.history_tab, columns=columns, 
                                          show="headings", height=15)
        
        # Заголовки столбцов
        self.history_tree.heading("date", text="Дата/Время")
        self.history_tree.heading("usl", text="ВГД")
        self.history_tree.heading("lsl", text="НГД")
        self.history_tree.heading("mean", text="Среднее")
        self.history_tree.heading("sigma", text="σ")
        self.history_tree.heading("cp", text="Cp")
        self.history_tree.heading("cpk", text="Cpk")
        self.history_tree.heading("status", text="Статус")
        
        # Ширина столбцов
        self.history_tree.column("date", width=120)
        self.history_tree.column("usl", width=60)
        self.history_tree.column("lsl", width=60)
        self.history_tree.column("mean", width=70)
        self.history_tree.column("sigma", width=60)
        self.history_tree.column("cp", width=60)
        self.history_tree.column("cpk", width=60)
        self.history_tree.column("status", width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.history_tab, orient=tk.VERTICAL, 
                                   command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Кнопки управления историей
        btn_frame = ttk.Frame(self.history_tab)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="📂 Загрузить из истории", 
                   command=self.load_from_history).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🗑️ Очистить историю", 
                   command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="📊 Экспорт истории в Excel", 
                   command=self.export_history_to_excel).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="📄 Загрузить из Excel", 
                   command=self.load_from_excel).pack(side=tk.LEFT, padx=5)
        
    def calculate_indices(self):
        """Расчет индексов качества Cp и Cpk"""
        try:
            # Получаем значения из полей ввода
            usl = float(self.usl_var.get())
            lsl = float(self.lsl_var.get())
            mean = float(self.mean_var.get())
            sigma = float(self.sigma_var.get())
            
            # Проверка корректности данных
            if sigma <= 0:
                messagebox.showerror("Ошибка", "Стандартное отклонение должно быть больше 0")
                return
                
            if usl <= lsl:
                messagebox.showerror("Ошибка", "Верхняя граница допуска должна быть больше нижней")
                return
            
            # Расчет Cp
            cp = (usl - lsl) / (6 * sigma)
            
            # Расчет Cpk
            cpu = (usl - mean) / (3 * sigma)
            cpl = (mean - lsl) / (3 * sigma)
            cpk = min(cpu, cpl)
            
            # Обновляем отображение
            self.cp_var.set(f"{cp:.3f}")
            self.cpk_var.set(f"{cpk:.3f}")
            
            # Определяем статус
            if cpk >= 1.33:
                status = "Отлично"
                color = "green"
            elif cpk >= 1.0:
                status = "Удовлетворительно"
                color = "blue"
            elif cpk >= 0.67:
                status = "Неудовлетворительно"
                color = "orange"
            else:
                status = "Критично"
                color = "red"
            
            self.status_var.set(f"Статус: {status}")
            self.status_label.config(foreground=color)
            
            # Обновляем график
            self.update_plot()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
            
    def update_plot(self):
        """Обновление графика нормального распределения"""
        try:
            # Получаем данные
            usl = float(self.usl_var.get())
            lsl = float(self.lsl_var.get())
            mean = float(self.mean_var.get())
            sigma = float(self.sigma_var.get())
            cp = float(self.cp_var.get())
            cpk = float(self.cpk_var.get())
            
            # Очищаем график
            self.ax.clear()
            
            # Генерируем данные для нормального распределения
            x = np.linspace(mean - 4*sigma, mean + 4*sigma, 1000)
            y = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mean)/sigma)**2)
            
            # Рисуем распределение
            self.ax.plot(x, y, 'b-', linewidth=2, label='Распределение процесса')
            
            # Закрашиваем области вне допусков
            x_out_lsl = x[x < lsl]
            y_out_lsl = y[x < lsl]
            x_out_usl = x[x > usl]
            y_out_usl = y[x > usl]
            
            if len(x_out_lsl) > 0:
                self.ax.fill_between(x_out_lsl, 0, y_out_lsl, color='red', alpha=0.3, label='Вне допуска')
            if len(x_out_usl) > 0:
                self.ax.fill_between(x_out_usl, 0, y_out_usl, color='red', alpha=0.3)
            
            # Закрашиваем область в допуске
            x_in = x[(x >= lsl) & (x <= usl)]
            y_in = y[(x >= lsl) & (x <= usl)]
            self.ax.fill_between(x_in, 0, y_in, color='green', alpha=0.3, label='В допуске')
            
            # Рисуем границы допуска
            self.ax.axvline(x=lsl, color='red', linestyle='--', linewidth=2, label=f'НГД = {lsl}')
            self.ax.axvline(x=usl, color='red', linestyle='--', linewidth=2, label=f'ВГД = {usl}')
            self.ax.axvline(x=mean, color='blue', linestyle='-', linewidth=2, label=f'Среднее = {mean:.2f}')
            
            # Добавляем информацию на график
            self.ax.set_xlabel('Значение')
            self.ax.set_ylabel('Плотность вероятности')
            self.ax.set_title(f'Нормальное распределение процесса\nCp = {cp:.3f}, Cpk = {cpk:.3f}')
            self.ax.legend(loc='upper right')
            self.ax.grid(True, alpha=0.3)
            
            # Обновляем канву
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {str(e)}")
            
    def save_to_history(self):
        """Сохранение текущего расчета в историю"""
        try:
            # Проверяем, есть ли рассчитанные значения
            if self.cp_var.get() == "0.000":
                messagebox.showwarning("Предупреждение", "Сначала выполните расчет")
                return
                
            # Создаем запись
            record = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'usl': self.usl_var.get(),
                'lsl': self.lsl_var.get(),
                'mean': self.mean_var.get(),
                'sigma': self.sigma_var.get(),
                'cp': self.cp_var.get(),
                'cpk': self.cpk_var.get(),
                'status': self.status_var.get().replace("Статус: ", "")
            }
            
            # Добавляем в историю
            self.history.append(record)
            
            # Обновляем отображение в таблице
            self.history_tree.insert('', 'end', values=(
                record['date'],
                record['usl'],
                record['lsl'],
                record['mean'],
                record['sigma'],
                record['cp'],
                record['cpk'],
                record['status']
            ))
            
            messagebox.showinfo("Успешно", "Расчет сохранен в историю")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")
            
    def load_from_history(self):
        """Загрузка данных из истории"""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись из истории")
            return
            
        # Получаем данные
        item = self.history_tree.item(selected[0])
        values = item['values']
        
        # Загружаем в поля ввода
        self.usl_var.set(values[1])
        self.lsl_var.set(values[2])
        self.mean_var.set(values[3])
        self.sigma_var.set(values[4])
        
        # Выполняем расчет
        self.calculate_indices()
        
        messagebox.showinfo("Успешно", "Данные загружены из истории")
        
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Очистить историю расчетов?"):
            self.history.clear()
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
                
    def export_to_excel(self):
        """Экспорт текущего расчета в Excel"""
        try:
            # Проверяем, есть ли рассчитанные значения
            if self.cp_var.get() == "0.000":
                messagebox.showwarning("Предупреждение", "Сначала выполните расчет")
                return
                
            # Создаем DataFrame
            data = {
                'Параметр': ['ВГД', 'НГД', 'Среднее', 'Ст. отклонение', 'Cp', 'Cpk', 'Статус'],
                'Значение': [
                    self.usl_var.get(),
                    self.lsl_var.get(),
                    self.mean_var.get(),
                    self.sigma_var.get(),
                    self.cp_var.get(),
                    self.cpk_var.get(),
                    self.status_var.get().replace("Статус: ", "")
                ]
            }
            
            df = pd.DataFrame(data)
            
            # Сохраняем в файл
            filename = f"quality_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     initialfile=filename,
                                                     filetypes=[("Excel files", "*.xlsx")])
            
            if filepath:
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Успешно", f"Данные экспортированы в {filepath}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
            
    def export_history_to_excel(self):
        """Экспорт всей истории в Excel"""
        try:
            if not self.history:
                messagebox.showwarning("Предупреждение", "История пуста")
                return
                
            # Создаем DataFrame из истории
            df = pd.DataFrame(self.history)
            
            # Сохраняем в файл
            filename = f"quality_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     initialfile=filename,
                                                     filetypes=[("Excel files", "*.xlsx")])
            
            if filepath:
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Успешно", f"История экспортирована в {filepath}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
            
    def load_from_excel(self):
        """Загрузка истории из Excel"""
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            
            if filepath:
                df = pd.read_excel(filepath)
                
                # Преобразуем в список словарей
                records = df.to_dict('records')
                
                # Очищаем текущую историю
                self.clear_history()
                
                # Добавляем записи
                for record in records:
                    # Преобразуем для совместимости
                    rec = {
                        'date': str(record.get('date', '')),
                        'usl': str(record.get('usl', '')),
                        'lsl': str(record.get('lsl', '')),
                        'mean': str(record.get('mean', '')),
                        'sigma': str(record.get('sigma', '')),
                        'cp': str(record.get('cp', '')),
                        'cpk': str(record.get('cpk', '')),
                        'status': str(record.get('status', ''))
                    }
                    
                    self.history.append(rec)
                    
                    # Добавляем в таблицу
                    self.history_tree.insert('', 'end', values=(
                        rec['date'],
                        rec['usl'],
                        rec['lsl'],
                        rec['mean'],
                        rec['sigma'],
                        rec['cp'],
                        rec['cpk'],
                        rec['status']
                    ))
                
                messagebox.showinfo("Успешно", f"Загружено {len(records)} записей")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {str(e)}")
            
    def export_to_pdf(self):
        """Экспорт текущего расчета в PDF (имитация)"""
        try:
            # Проверяем, есть ли рассчитанные значения
            if self.cp_var.get() == "0.000":
                messagebox.showwarning("Предупреждение", "Сначала выполните расчет")
                return
                
            # Создаем HTML-отчет
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Анализ качества процесса</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 50%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>Анализ индексов качества процесса</h1>
                <p>Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>Входные параметры:</h2>
                <table>
                    <tr><th>Параметр</th><th>Значение</th></tr>
                    <tr><td>Верхняя граница допуска (ВГД)</td><td>{self.usl_var.get()}</td></tr>
                    <tr><td>Нижняя граница допуска (НГД)</td><td>{self.lsl_var.get()}</td></tr>
                    <tr><td>Среднее значение (μ)</td><td>{self.mean_var.get()}</td></tr>
                    <tr><td>Стандартное отклонение (σ)</td><td>{self.sigma_var.get()}</td></tr>
                </table>
                
                <h2>Результаты анализа:</h2>
                <table>
                    <tr><th>Показатель</th><th>Значение</th></tr>
                    <tr><td>Индекс Cp</td><td>{self.cp_var.get()}</td></tr>
                    <tr><td>Индекс Cpk</td><td>{self.cpk_var.get()}</td></tr>
                    <tr><td>Статус процесса</td><td>{self.status_var.get().replace("Статус: ", "")}</td></tr>
                </table>
                
                <p>Сгенерировано программой "Анализ индексов качества процессов"</p>
            </body>
            </html>
            """
            
            # Сохраняем как HTML (вместо PDF для простоты)
            filename = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = filedialog.asksaveasfilename(defaultextension=".html",
                                                     initialfile=filename,
                                                     filetypes=[("HTML files", "*.html")])
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Открываем в браузере
                webbrowser.open(filepath)
                messagebox.showinfo("Успешно", f"Отчет сохранен как HTML: {filepath}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

def main():
    root = tk.Tk()
    app = ProcessQualityAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()