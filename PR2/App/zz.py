import tkinter as tk
from tkinter import ttk, messagebox
import math

class ReliabilityApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Определение показателей безотказности системы")
        self.root.geometry("700x500")
        
        self.setup_ui()
        
        self.root.mainloop()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Определение показателей безотказности системы", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        task1_frame = ttk.Frame(notebook)
        task2_frame = ttk.Frame(notebook)
        task3_frame = ttk.Frame(notebook)
        
        notebook.add(task1_frame, text="Задание 1")
        notebook.add(task2_frame, text="Задание 2")
        notebook.add(task3_frame, text="Задание 3")
        
        self.setup_task1(task1_frame)
        self.setup_task2(task2_frame)
        self.setup_task3(task3_frame)
    
    def setup_task1(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Задание 1", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        desc_text = "За исследуемый период эксплуатации система отказала 6 раз.\n" \
                   "До первого отказа система проработала 185 часов, до второго – 342 часа,\n" \
                   "до третьего – 268 часов, до четвертого – 220 часов, до пятого – 96 часов,\n" \
                   "до шестого – 102 часа."
        
        ttk.Label(frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        input_frame = ttk.LabelFrame(frame, text="Введите наработки до отказов (часы)", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        entries_frame = ttk.Frame(input_frame)
        entries_frame.pack()
        
        self.task1_entries = []
        default_values = [185, 342, 268, 220, 96, 102]
        
        for i in range(6):
            ttk.Label(entries_frame, text=f"t{i+1}:").grid(row=i, column=0, padx=5, pady=2)
            entry = ttk.Entry(entries_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entry.insert(0, str(default_values[i]))
            self.task1_entries.append(entry)
        
        result_frame = ttk.LabelFrame(frame, text="Результат", padding="10")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.task1_result = ttk.Label(result_frame, text="", font=('Arial', 11))
        self.task1_result.pack()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Рассчитать", command=self.calculate_task1, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_task1, width=15).pack(side=tk.LEFT, padx=5)
    
    def setup_task2(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Задание 2", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        desc_text = "В течение некоторого времени проводилось наблюдение за работой 3 экземпляров\n" \
                   "одинаковых информационных систем. Каждая из систем проработала ti часов\n" \
                   "и имела ni отказов."
        
        ttk.Label(frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        input_frame = ttk.LabelFrame(frame, text="Данные по системам", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        header_frame = ttk.Frame(input_frame)
        header_frame.pack()
        
        ttk.Label(header_frame, text="Система", width=10).grid(row=0, column=0, padx=5)
        ttk.Label(header_frame, text="Наработка (часы)", width=15).grid(row=0, column=1, padx=5)
        ttk.Label(header_frame, text="Кол-во отказов", width=15).grid(row=0, column=2, padx=5)
        
        self.task2_entries_t = []
        self.task2_entries_n = []
        default_t = [358, 385, 400]
        default_n = [4, 3, 2]
        
        for i in range(3):
            ttk.Label(header_frame, text=f"{i+1}").grid(row=i+1, column=0, padx=5)
            
            entry_t = ttk.Entry(header_frame, width=15)
            entry_t.grid(row=i+1, column=1, padx=5, pady=2)
            entry_t.insert(0, str(default_t[i]))
            self.task2_entries_t.append(entry_t)
            
            entry_n = ttk.Entry(header_frame, width=15)
            entry_n.grid(row=i+1, column=2, padx=5, pady=2)
            entry_n.insert(0, str(default_n[i]))
            self.task2_entries_n.append(entry_n)
        
        result_frame = ttk.LabelFrame(frame, text="Результат", padding="10")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.task2_result = ttk.Label(result_frame, text="", font=('Arial', 11))
        self.task2_result.pack()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Рассчитать", command=self.calculate_task2, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_task2, width=15).pack(side=tk.LEFT, padx=5)
    
    def setup_task3(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Задание 3", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        desc_text = "По результатам исследования двух автоматизированных систем определить,\n" \
                   "какая из систем является более надежной по коэффициенту готовности."
        
        ttk.Label(frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        input_frame = ttk.LabelFrame(frame, text="Данные по системам", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        data_frame = ttk.Frame(input_frame)
        data_frame.pack()
        
        ttk.Label(data_frame, text="Система 1", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(data_frame, text="Система 2", font=('Arial', 10, 'bold')).grid(row=0, column=2, columnspan=2, pady=5)
        
        ttk.Label(data_frame, text="Время работы до отказа (t0):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.task3_t0_1 = ttk.Entry(data_frame, width=10)
        self.task3_t0_1.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(data_frame, text="Время работы до отказа (t0):").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.task3_t0_2 = ttk.Entry(data_frame, width=10)
        self.task3_t0_2.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(data_frame, text="Время ремонта (tв):").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.task3_tv_1 = ttk.Entry(data_frame, width=10)
        self.task3_tv_1.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(data_frame, text="Время ремонта (tв):").grid(row=2, column=2, sticky=tk.W, padx=5)
        self.task3_tv_2 = ttk.Entry(data_frame, width=10)
        self.task3_tv_2.grid(row=2, column=3, padx=5, pady=2)
        
        ttk.Button(data_frame, text="Заполнить по варианту 1", command=self.fill_variant1, width=20).grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(data_frame, text="Заполнить по варианту 16", command=self.fill_variant16, width=20).grid(row=4, column=0, columnspan=4, pady=5)
        
        result_frame = ttk.LabelFrame(frame, text="Результат", padding="10")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.task3_result1 = ttk.Label(result_frame, text="", font=('Arial', 11))
        self.task3_result1.pack(anchor=tk.W)
        
        self.task3_result2 = ttk.Label(result_frame, text="", font=('Arial', 11))
        self.task3_result2.pack(anchor=tk.W)
        
        self.task3_result_compare = ttk.Label(result_frame, text="", font=('Arial', 11, 'bold'))
        self.task3_result_compare.pack(anchor=tk.W, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Рассчитать", command=self.calculate_task3, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_task3, width=15).pack(side=tk.LEFT, padx=5)
    
    def calculate_task1(self):
        try:
            times = []
            for entry in self.task1_entries:
                value = float(entry.get())
                if value <= 0:
                    messagebox.showerror("Ошибка", "Значения должны быть положительными")
                    return
                times.append(value)
            
            total_time = sum(times)
            n = len(times)
            mtbf = total_time / n
            
            result_text = f"Суммарная наработка: {total_time:.2f} часов\n" \
                         f"Количество отказов: {n}\n" \
                         f"Средняя наработка на отказ (T₀) = {mtbf:.2f} часов"
            
            self.task1_result.config(text=result_text)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def calculate_task2(self):
        try:
            total_time = 0
            total_failures = 0
            
            for i in range(3):
                t = float(self.task2_entries_t[i].get())
                n = int(self.task2_entries_n[i].get())
                
                if t <= 0 or n <= 0:
                    messagebox.showerror("Ошибка", "Значения должны быть положительными")
                    return
                
                total_time += t
                total_failures += n
            
            mtbf = total_time / total_failures
            
            result_text = f"Суммарная наработка всех систем: {total_time:.2f} часов\n" \
                         f"Общее количество отказов: {total_failures}\n" \
                         f"Средняя наработка на отказ (T₀) = {mtbf:.2f} часов"
            
            self.task2_result.config(text=result_text)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def calculate_task3(self):
        try:
            t0_1 = float(self.task3_t0_1.get())
            tv_1 = float(self.task3_tv_1.get())
            t0_2 = float(self.task3_t0_2.get())
            tv_2 = float(self.task3_tv_2.get())
            
            if t0_1 <= 0 or tv_1 <= 0 or t0_2 <= 0 or tv_2 <= 0:
                messagebox.showerror("Ошибка", "Все значения должны быть положительными")
                return
            
            kg1 = t0_1 / (t0_1 + tv_1)
            kg2 = t0_2 / (t0_2 + tv_2)
            
            result1_text = f"Система 1: T₀ = {t0_1:.2f} ч, Tв = {tv_1:.2f} ч, Кг = {kg1:.4f}"
            result2_text = f"Система 2: T₀ = {t0_2:.2f} ч, Tв = {tv_2:.2f} ч, Кг = {kg2:.4f}"
            
            self.task3_result1.config(text=result1_text)
            self.task3_result2.config(text=result2_text)
            
            if kg1 > kg2:
                compare_text = f"✓ Система 1 более надежна (Кг = {kg1:.4f} > {kg2:.4f})"
            elif kg2 > kg1:
                compare_text = f"✓ Система 2 более надежна (Кг = {kg2:.4f} > {kg1:.4f})"
            else:
                compare_text = f"Системы одинаково надежны (Кг = {kg1:.4f})"
            
            self.task3_result_compare.config(text=compare_text)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def fill_variant1(self):
        self.task3_t0_1.delete(0, tk.END)
        self.task3_t0_1.insert(0, "24")
        self.task3_tv_1.delete(0, tk.END)
        self.task3_tv_1.insert(0, "16")
        self.task3_t0_2.delete(0, tk.END)
        self.task3_t0_2.insert(0, "400")
        self.task3_tv_2.delete(0, tk.END)
        self.task3_tv_2.insert(0, "32")
    
    def fill_variant16(self):
        self.task3_t0_1.delete(0, tk.END)
        self.task3_t0_1.insert(0, "304")
        self.task3_tv_1.delete(0, tk.END)
        self.task3_tv_1.insert(0, "16")
        self.task3_t0_2.delete(0, tk.END)
        self.task3_t0_2.insert(0, "4")
        self.task3_tv_2.delete(0, tk.END)
        self.task3_tv_2.insert(0, "8")
    
    def clear_task1(self):
        for entry in self.task1_entries:
            entry.delete(0, tk.END)
        self.task1_result.config(text="")
    
    def clear_task2(self):
        for entry in self.task2_entries_t:
            entry.delete(0, tk.END)
        for entry in self.task2_entries_n:
            entry.delete(0, tk.END)
        self.task2_result.config(text="")
    
    def clear_task3(self):
        self.task3_t0_1.delete(0, tk.END)
        self.task3_tv_1.delete(0, tk.END)
        self.task3_t0_2.delete(0, tk.END)
        self.task3_tv_2.delete(0, tk.END)
        self.task3_result1.config(text="")
        self.task3_result2.config(text="")
        self.task3_result_compare.config(text="")

if __name__ == "__main__":
    app = ReliabilityApp()