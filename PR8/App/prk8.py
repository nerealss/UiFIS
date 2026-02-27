import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import math
import re

class DeliveryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор доставки")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # История расчетов
        self.history = []
        
        # Тарифы транспорта (руб/км)
        self.transport_rates = {
            "Автомобиль": 40,
            "Грузовик": 60,
            "Мотоцикл": 25,
            "Фургон": 50,
            "Экспресс": 80
        }
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.setup_ui()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Result.TLabel", font=("Arial", 11))
        style.configure("Calculate.TButton", font=("Arial", 11, "bold"))
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = ttk.Label(title_frame, text="🚚 Калькулятор доставки", 
                                 style="Title.TLabel")
        title_label.pack()
        
        # Основной контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - параметры доставки
        left_frame = ttk.LabelFrame(main_container, text="Параметры доставки", padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Пункт отправления
        ttk.Label(left_frame, text="Пункт отправления:", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        self.from_entry = ttk.Entry(left_frame, font=("Arial", 11), width=40)
        self.from_entry.pack(fill=tk.X, pady=(0, 15))
        self.from_entry.insert(0, "Москва, Красная площадь")
        
        # Подсказка для координат
        ttk.Label(left_frame, text="(можно ввести адрес или координаты: 55.7558, 37.6173)", 
                  font=("Arial", 8), foreground="gray").pack(anchor=tk.W, pady=(0, 10))
        
        # Пункт назначения
        ttk.Label(left_frame, text="Пункт назначения:", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        self.to_entry = ttk.Entry(left_frame, font=("Arial", 11), width=40)
        self.to_entry.pack(fill=tk.X, pady=(0, 15))
        self.to_entry.insert(0, "Санкт-Петербург, Невский проспект")
        
        # Тип транспорта
        ttk.Label(left_frame, text="Тип транспорта:", 
                  style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        self.transport_var = tk.StringVar(value="Автомобиль")
        transport_combo = ttk.Combobox(left_frame, textvariable=self.transport_var,
                                        values=list(self.transport_rates.keys()),
                                        font=("Arial", 11), state="readonly", width=38)
        transport_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Кнопки управления
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.calc_btn = ttk.Button(button_frame, text="🚀 Рассчитать", 
                                    command=self.calculate_delivery,
                                    style="Calculate.TButton")
        self.calc_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Очистить", 
                                     command=self.clear_fields)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к расчету")
        status_label = ttk.Label(left_frame, textvariable=self.status_var,
                                  font=("Arial", 10), foreground="green")
        status_label.pack(anchor=tk.W, pady=10)
        
        # Правая панель - результаты и история
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Результат расчета
        result_frame = ttk.LabelFrame(right_frame, text="Результат расчета", padding=10)
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.result_text = tk.Text(result_frame, height=12, width=40,
                                    font=("Consolas", 10), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # История расчетов
        history_frame = ttk.LabelFrame(right_frame, text="История расчетов", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Таблица истории
        columns = ("time", "from", "to", "transport", "cost")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, 
                                          show="headings", height=8)
        
        self.history_tree.heading("time", text="Время")
        self.history_tree.heading("from", text="Откуда")
        self.history_tree.heading("to", text="Куда")
        self.history_tree.heading("transport", text="Транспорт")
        self.history_tree.heading("cost", text="Стоимость")
        
        self.history_tree.column("time", width=80)
        self.history_tree.column("from", width=120)
        self.history_tree.column("to", width=120)
        self.history_tree.column("transport", width=80)
        self.history_tree.column("cost", width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                   command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязка события выбора из истории
        self.history_tree.bind('<Double-Button-1>', self.load_from_history)
        
        # Кнопка очистки истории
        ttk.Button(history_frame, text="Очистить историю", 
                   command=self.clear_history).pack(pady=5)
        
    def parse_coordinates(self, text):
        """Парсит координаты из строки"""
        # Паттерн для поиска координат: число, число
        pattern = r'(-?\d+\.?\d*)\s*[,;\s]\s*(-?\d+\.?\d*)'
        match = re.search(pattern, text)
        
        if match:
            try:
                lat = float(match.group(1))
                lon = float(match.group(2))
                return lat, lon
            except ValueError:
                return None
        return None
    
    def geocode_address(self, address):
        """Преобразует адрес в координаты с помощью Nominatim API"""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            
            headers = {
                'User-Agent': 'DeliveryCalculator/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    display_name = data[0]['display_name']
                    return lat, lon, display_name
                    
        except requests.exceptions.RequestException as e:
            print(f"Ошибка геокодирования: {e}")
            
        return None
    
    def calculate_route(self, from_coords, to_coords):
        """Рассчитывает маршрут с помощью OSRM API"""
        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{from_coords[1]},{from_coords[0]};{to_coords[1]},{to_coords[0]}"
            params = {
                'overview': 'false',
                'geometries': 'geojson'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 'Ok':
                    route = data['routes'][0]
                    distance = route['distance'] / 1000  # в километры
                    duration = route['duration'] / 60    # в минуты
                    return distance, duration
                    
        except requests.exceptions.RequestException as e:
            print(f"Ошибка расчета маршрута: {e}")
            
        return None
    
    def calculate_delivery(self):
        """Основная функция расчета доставки"""
        
        # Получаем значения из полей ввода
        from_text = self.from_entry.get().strip()
        to_text = self.to_entry.get().strip()
        transport = self.transport_var.get()
        
        # Проверка на пустые поля
        if not from_text or not to_text:
            messagebox.showerror("Ошибка", "Заполните оба пункта!")
            self.status_var.set("Ошибка: не все поля заполнены")
            return
        
        self.status_var.set("Выполняется расчет...")
        self.root.update()
        
        try:
            # Определяем координаты для пункта отправления
            from_coords = self.parse_coordinates(from_text)
            from_display = from_text
            
            if not from_coords:
                # Если это не координаты, геокодируем адрес
                result = self.geocode_address(from_text)
                if result:
                    from_coords = (result[0], result[1])
                    from_display = result[2]
                else:
                    messagebox.showerror("Ошибка", f"Не удалось найти адрес: {from_text}")
                    self.status_var.set("Ошибка геокодирования")
                    return
            
            # Определяем координаты для пункта назначения
            to_coords = self.parse_coordinates(to_text)
            to_display = to_text
            
            if not to_coords:
                result = self.geocode_address(to_text)
                if result:
                    to_coords = (result[0], result[1])
                    to_display = result[2]
                else:
                    messagebox.showerror("Ошибка", f"Не удалось найти адрес: {to_text}")
                    self.status_var.set("Ошибка геокодирования")
                    return
            
            # Рассчитываем маршрут
            route_result = self.calculate_route(from_coords, to_coords)
            
            if route_result:
                distance, duration = route_result
                
                # Рассчитываем стоимость
                rate = self.transport_rates[transport]
                cost = distance * rate
                
                # Форматируем время
                hours = int(duration // 60)
                minutes = int(duration % 60)
                
                if hours > 0:
                    time_str = f"{hours} ч {minutes} мин"
                else:
                    time_str = f"{minutes} мин"
                
                # Формируем результат
                current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                
                result = f"""
╔════════════════════════════════════════════╗
║          РЕЗУЛЬТАТ РАСЧЕТА                 ║
╠════════════════════════════════════════════╣
║ Откуда: {self.truncate_text(from_display, 30):<30} ║
║ Куда:   {self.truncate_text(to_display, 30):<30} ║
║ Транспорт: {transport:<20}          ║
║ Расстояние: {distance:<8.1f} км                   ║
║ Время: {time_str:<18}             ║
║ Стоимость: {cost:>10.2f} руб.                ║
║ Рассчитано: {current_time}      ║
╚════════════════════════════════════════════╝
                """
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
                
                # Добавляем в историю
                history_item = {
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'from': self.truncate_text(from_display, 25),
                    'to': self.truncate_text(to_display, 25),
                    'transport': transport[:10],
                    'cost': f"{cost:.0f} руб.",
                    'full_data': {
                        'from': from_display,
                        'to': to_display,
                        'transport': transport,
                        'distance': distance,
                        'duration': duration,
                        'cost': cost,
                        'timestamp': current_time
                    }
                }
                
                self.history.append(history_item)
                self.update_history_display()
                
                self.status_var.set("✅ Расчет выполнен успешно")
                
            else:
                messagebox.showerror("Ошибка", "Не удалось построить маршрут")
                self.status_var.set("Ошибка расчета маршрута")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.status_var.set("Ошибка при выполнении расчета")
    
    def truncate_text(self, text, max_length):
        """Обрезает текст до нужной длины"""
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text
    
    def update_history_display(self):
        """Обновляет отображение истории"""
        # Очищаем текущую историю
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Добавляем записи из истории (с конца, чтобы новые были сверху)
        for item in reversed(self.history[-20:]):  # Показываем последние 20 записей
            self.history_tree.insert('', 'end', values=(
                item['time'],
                item['from'],
                item['to'],
                item['transport'],
                item['cost']
            ))
    
    def load_from_history(self, event):
        """Загружает данные из истории при двойном клике"""
        selected = self.history_tree.selection()
        if selected:
            # Получаем индекс выбранного элемента
            index = self.history_tree.index(selected[0])
            # Находим соответствующий элемент в истории
            history_item = list(reversed(self.history))[index]
            
            if 'full_data' in history_item:
                data = history_item['full_data']
                self.from_entry.delete(0, tk.END)
                self.from_entry.insert(0, data['from'])
                self.to_entry.delete(0, tk.END)
                self.to_entry.insert(0, data['to'])
                self.transport_var.set(data['transport'])
                
                self.status_var.set("Данные загружены из истории")
    
    def clear_fields(self):
        """Очищает поля ввода"""
        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("Поля очищены")
    
    def clear_history(self):
        """Очищает историю расчетов"""
        self.history.clear()
        self.update_history_display()
        self.status_var.set("История очищена")

def main():
    root = tk.Tk()
    app = DeliveryCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()