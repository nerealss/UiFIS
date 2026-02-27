import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import threading
import json
import os

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Список валют
        self.currencies = {
            "Российский рубль": "RUB",
            "Доллар США": "USD",
            "Евро": "EUR",
            "Китайский юань": "CNY",
            "Южнокорейская вона": "KRW"
        }
        
        # Курсы валют к RUB (по умолчанию)
        self.rates = {
            "USD": 77.70,
            "EUR": 90.34,
            "CNY": 10.96,
            "KRW": 0.0670
        }
        
        # Дата последнего обновления
        self.last_update = None
        
        # Переменные для ввода/вывода
        self.amount_var = tk.StringVar(value="100")
        self.result_var = tk.StringVar(value="")
        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка сохраненных курсов
        self.load_saved_rates()
        
        # Автоматическое обновление курсов при запуске
        self.update_rates_async()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 11, "bold"))
        style.configure("Result.TLabel", font=("Arial", 14, "bold"), foreground="blue")
        style.configure("Rate.TLabel", font=("Arial", 10))
        style.configure("Update.TButton", font=("Arial", 10))
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="💱 Конвертер валют", 
                                 style="Title.TLabel")
        title_label.pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Выбор исходной валюты
        from_frame = ttk.LabelFrame(main_frame, text="Изменить из:", padding=10)
        from_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(from_frame, text="Валюта:", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        
        self.from_combo = ttk.Combobox(from_frame, textvariable=self.from_currency_var,
                                        values=list(self.currencies.keys()),
                                        font=("Arial", 11), state="readonly", width=25)
        self.from_combo.grid(row=0, column=1, padx=5, pady=5)
        self.from_combo.current(0)
        self.from_combo.bind('<<ComboboxSelected>>', self.on_currency_change)
        
        # Символ валюты
        ttk.Label(from_frame, text="₽", font=("Arial", 14)).grid(row=0, column=2, padx=5)
        
        # Выбор целевой валюты
        to_frame = ttk.LabelFrame(main_frame, text="В:", padding=10)
        to_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(to_frame, text="Валюта:", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        
        self.to_combo = ttk.Combobox(to_frame, textvariable=self.to_currency_var,
                                      values=list(self.currencies.keys()),
                                      font=("Arial", 11), state="readonly", width=25)
        self.to_combo.grid(row=0, column=1, padx=5, pady=5)
        self.to_combo.current(1)
        self.to_combo.bind('<<ComboboxSelected>>', self.on_currency_change)
        
        # Символ валюты
        self.to_symbol_label = ttk.Label(to_frame, text="$", font=("Arial", 14))
        self.to_symbol_label.grid(row=0, column=2, padx=5)
        
        # Ввод суммы
        amount_frame = ttk.LabelFrame(main_frame, text="Сумма:", padding=10)
        amount_frame.pack(fill=tk.X, pady=5)
        
        self.amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var,
                                        font=("Arial", 12), width=15)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        self.amount_entry.bind('<KeyRelease>', self.on_amount_change)
        
        # Кнопка конвертации (на случай, если автоматическое не работает)
        ttk.Button(amount_frame, text="Конвертировать", 
                   command=self.convert_currency).pack(side=tk.LEFT, padx=5)
        
        # Результат
        result_frame = ttk.LabelFrame(main_frame, text="Результат:", padding=10)
        result_frame.pack(fill=tk.X, pady=5)
        
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var,
                                        style="Result.TLabel")
        self.result_label.pack(pady=5)
        
        # Курсы валют
        rates_frame = ttk.LabelFrame(main_frame, text="Курсы валют к RUB", padding=10)
        rates_frame.pack(fill=tk.X, pady=5)
        
        self.rates_labels = {}
        currencies_order = ["USD", "EUR", "CNY", "KRW"]
        currency_names = {
            "USD": "Доллар США",
            "EUR": "Евро",
            "CNY": "Китайский юань",
            "KRW": "Южнокорейская вона"
        }
        
        for i, curr in enumerate(currencies_order):
            name = currency_names[curr]
            label_text = f"1 {curr} ({name}) = "
            ttk.Label(rates_frame, text=label_text, style="Rate.TLabel").grid(row=i, column=0, sticky="w", pady=2)
            
            self.rates_labels[curr] = ttk.Label(rates_frame, text=f"{self.rates[curr]:.4f} RUB", 
                                                  style="Rate.TLabel", foreground="blue")
            self.rates_labels[curr].grid(row=i, column=1, sticky="w", pady=2, padx=5)
        
        # Кнопка обновления курсов
        update_frame = ttk.Frame(main_frame)
        update_frame.pack(fill=tk.X, pady=10)
        
        self.update_btn = ttk.Button(update_frame, text="🔄 Обновить курсы", 
                                       command=self.update_rates_async,
                                       style="Update.TButton")
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_status = ttk.Label(update_frame, text="", font=("Arial", 9))
        self.update_status.pack(side=tk.LEFT, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Привязка событий
        self.root.bind('<Return>', lambda e: self.convert_currency())
        
        # Первоначальная конвертация
        self.convert_currency()
        
    def get_currency_symbol(self, currency_name):
        """Возвращает символ валюты по названию"""
        symbols = {
            "Российский рубль": "₽",
            "Доллар США": "$",
            "Евро": "€",
            "Китайский юань": "¥",
            "Южнокорейская вона": "₩"
        }
        return symbols.get(currency_name, "")
    
    def on_currency_change(self, event=None):
        """Обработка изменения валюты"""
        # Обновляем символ для целевой валюты
        to_currency = self.to_currency_var.get()
        if to_currency:
            symbol = self.get_currency_symbol(to_currency)
            self.to_symbol_label.config(text=symbol)
        
        # Выполняем конвертацию
        self.convert_currency()
    
    def on_amount_change(self, event=None):
        """Обработка изменения суммы"""
        self.convert_currency()
    
    def convert_currency(self):
        """Конвертация валюты"""
        try:
            # Получаем сумму
            amount_text = self.amount_var.get().strip()
            if not amount_text:
                return
                
            amount = float(amount_text.replace(',', '.'))
            
            # Получаем валюты
            from_currency_name = self.from_currency_var.get()
            to_currency_name = self.to_currency_var.get()
            
            if not from_currency_name or not to_currency_name:
                return
            
            # Получаем коды валют
            from_code = self.currencies[from_currency_name]
            to_code = self.currencies[to_currency_name]
            
            # Конвертация через RUB
            if from_code == "RUB":
                # Из рублей в другую валюту
                if to_code == "RUB":
                    result = amount
                else:
                    result = amount / self.rates[to_code]
            elif to_code == "RUB":
                # Из другой валюты в рубли
                result = amount * self.rates[from_code]
            else:
                # Из одной валюты в другую (обе не RUB)
                result = (amount * self.rates[from_code]) / self.rates[to_code]
            
            # Форматируем результат
            if abs(result) < 0.01:
                result_str = f"{result:.6f}"
            elif abs(result) < 1:
                result_str = f"{result:.4f}"
            elif abs(result) < 1000:
                result_str = f"{result:,.2f}".replace(',', ' ')
            else:
                result_str = f"{result:,.2f}".replace(',', ' ')
            
            # Добавляем пробелы между тысячами
            parts = result_str.split('.')
            if len(parts) > 1:
                integer_part = parts[0]
                decimal_part = parts[1]
                # Добавляем пробелы между тысячами
                integer_part = ' '.join([integer_part[max(0, i-3):i] 
                                         for i in range(len(integer_part), 0, -3)][::-1])
                result_str = f"{integer_part}.{decimal_part}"
            else:
                result_str = ' '.join([result_str[max(0, i-3):i] 
                                       for i in range(len(result_str), 0, -3)][::-1])
            
            self.result_var.set(f"{result_str} {self.get_currency_symbol(to_currency_name)}")
            self.status_var.set("Конвертация выполнена успешно")
            
        except ValueError:
            self.result_var.set("Ошибка ввода")
            self.status_var.set("Ошибка: введите корректное число")
        except Exception as e:
            self.result_var.set("Ошибка")
            self.status_var.set(f"Ошибка: {str(e)}")
    
    def update_rates_async(self):
        """Асинхронное обновление курсов валют"""
        self.update_btn.config(state=tk.DISABLED)
        self.update_status.config(text="Обновление...", foreground="orange")
        
        # Запускаем обновление в отдельном потоке
        thread = threading.Thread(target=self.update_rates)
        thread.daemon = True
        thread.start()
    
    def update_rates(self):
        """Обновление курсов валют через API"""
        try:
            # Используем бесплатный API exchangerate-api.com
            url = "https://api.exchangerate-api.com/v4/latest/RUB"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Получаем курсы
                rates = data.get('rates', {})
                
                # Обновляем курсы для нужных валют
                if 'USD' in rates:
                    self.rates['USD'] = 1 / rates['USD']  # API дает RUB за USD, нам нужно USD за RUB
                if 'EUR' in rates:
                    self.rates['EUR'] = 1 / rates['EUR']
                if 'CNY' in rates:
                    self.rates['CNY'] = 1 / rates['CNY']
                if 'KRW' in rates:
                    self.rates['KRW'] = 1 / rates['KRW']
                
                self.last_update = datetime.now()
                
                # Сохраняем курсы
                self.save_rates()
                
                # Обновляем отображение в главном потоке
                self.root.after(0, self.update_rates_display)
                self.root.after(0, lambda: self.update_status.config(
                    text=f"Обновлено: {self.last_update.strftime('%H:%M:%S')}", 
                    foreground="green"))
                self.root.after(0, lambda: self.status_var.set("Курсы успешно обновлены"))
            else:
                self.root.after(0, lambda: self.update_status.config(
                    text="Ошибка API", foreground="red"))
                self.root.after(0, lambda: self.status_var.set("Не удалось получить курсы"))
                
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self.update_status.config(
                text="Ошибка сети", foreground="red"))
            self.root.after(0, lambda: self.status_var.set(f"Ошибка сети: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: self.update_status.config(
                text="Ошибка", foreground="red"))
            self.root.after(0, lambda: self.status_var.set(f"Ошибка: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.update_btn.config(state=tk.NORMAL))
            self.root.after(0, self.convert_currency)
    
    def update_rates_display(self):
        """Обновление отображения курсов"""
        for curr, label in self.rates_labels.items():
            label.config(text=f"{self.rates[curr]:.4f} RUB")
    
    def save_rates(self):
        """Сохранение курсов в файл"""
        try:
            data = {
                'rates': self.rates,
                'last_update': self.last_update.isoformat() if self.last_update else None
            }
            with open('currency_rates.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_saved_rates(self):
        """Загрузка сохраненных курсов"""
        try:
            if os.path.exists('currency_rates.json'):
                with open('currency_rates.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                saved_rates = data.get('rates', {})
                for curr in self.rates:
                    if curr in saved_rates:
                        self.rates[curr] = saved_rates[curr]
                
                last_update_str = data.get('last_update')
                if last_update_str:
                    self.last_update = datetime.fromisoformat(last_update_str)
                    self.update_status.config(
                        text=f"Сохранено: {self.last_update.strftime('%H:%M:%S')}",
                        foreground="blue")
                
                self.update_rates_display()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

def main():
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
