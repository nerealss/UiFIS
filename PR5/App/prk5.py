import tkinter as tk
from tkinter import ttk
import time
import threading
import random
from datetime import datetime
import queue
import math

class Packet:
    """Класс, представляющий сетевой пакет"""
    def __init__(self, packet_id, source, destination, size):
        self.id = packet_id
        self.source = source
        self.destination = destination
        self.size = size
        self.start_time = time.time()
        self.status = "created"  # created, in_transit, at_switch, delivered
        self.position = 0.0  # позиция для анимации (0-1)
        self.color = self.generate_color()
        
    def generate_color(self):
        """Генерирует цвет на основе ID пакета"""
        colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FF33F3', '#33FFF3']
        return colors[self.id % len(colors)]
    
    def get_delay(self):
        """Возвращает задержку доставки в мс"""
        return int((time.time() - self.start_time) * 1000)

class NetworkTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Сетевой терминал - Имитация ЛВС")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Параметры сети
        self.packets = []
        self.packet_counter = 0
        self.is_running = False
        self.speed = 2  # пакетов в секунду
        self.switch_buffer = []
        
        # Очередь для обновления GUI из потоков
        self.update_queue = queue.Queue()
        
        # Цвета для состояний
        self.colors = {
            'idle': '#808080',      # серый
            'active': '#00FF00',     # зеленый
            'sending': '#FFFF00',    # желтый
            'receiving': '#FFA500',  # оранжевый
            'switch': '#00FFFF'      # голубой
        }
        
        # Создание интерфейса
        self.setup_ui()
        
        # Запуск обработки очереди обновлений
        self.process_queue()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Верхняя панель с элементами управления
        control_frame = ttk.Frame(self.root, padding="5")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Старт", command=self.start_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Стоп", command=self.stop_simulation).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Пакеты в сек.:").pack(side=tk.LEFT, padx=(20,5))
        self.speed_var = tk.StringVar(value="2")
        speed_spinbox = ttk.Spinbox(control_frame, from_=1, to=10, width=5, 
                                     textvariable=self.speed_var)
        speed_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Очистить", command=self.clear_console).pack(side=tk.LEFT, padx=20)
        
        # Статус
        self.status_label = ttk.Label(control_frame, text="Готов к работе")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Основная область
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая часть - визуализация сети
        self.canvas = tk.Canvas(main_frame, width=500, height=400, bg='#2b2b2b', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Правая часть - консоль
        console_frame = ttk.LabelFrame(main_frame, text="КОНСОЛЬ", padding="5")
        console_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Текстовое поле для консоли с прокруткой
        console_text_frame = ttk.Frame(console_frame)
        console_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console = tk.Text(console_text_frame, height=20, width=40, 
                                bg='black', fg='#00FF00', font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(console_text_frame, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Счетчик пакетов
        stats_frame = ttk.Frame(console_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stats_frame, text="Всего передано пакетов:").pack(side=tk.LEFT)
        self.packet_count_label = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
        self.packet_count_label.pack(side=tk.LEFT, padx=5)
        
        # Рисуем топологию сети
        self.draw_network()
        
    def draw_network(self):
        """Рисует топологию сети (звезда)"""
        self.canvas.delete("all")
        
        # Координаты устройств
        self.devices = {
            'SWITCH': (250, 200),
            'ПК1': (50, 50),
            'ПК2': (450, 50),
            'ПК3': (50, 350),
            'ПК4': (450, 350)
        }
        
        # Рисуем линии соединений (звезда)
        self.lines = {}
        for device, coords in self.devices.items():
            if device != 'SWITCH':
                line_id = self.canvas.create_line(self.devices['SWITCH'][0], self.devices['SWITCH'][1],
                                                   coords[0], coords[1], 
                                                   fill='#404040', width=2, dash=(5, 3))
                self.lines[f"{device}_link"] = line_id
        
        # Рисуем устройства
        self.device_items = {}
        for name, (x, y) in self.devices.items():
            if name == 'SWITCH':
                # Коммутатор (голубой)
                rect_id = self.canvas.create_rectangle(x-40, y-30, x+40, y+30, 
                                                        fill=self.colors['switch'], 
                                                        outline='white', width=2)
                self.canvas.create_text(x, y, text=name, fill='black', font=('Arial', 10, 'bold'))
                
                # Порт-индикаторы
                for i, port in enumerate(['1', '2', '3', '4']):
                    port_x = x - 30 + i*20
                    port_y = y - 15
                    self.canvas.create_oval(port_x-3, port_y-3, port_x+3, port_y+3, 
                                            fill='green', outline='white')
            else:
                # Компьютеры
                rect_id = self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                                        fill=self.colors['idle'], 
                                                        outline='white', width=2)
                self.canvas.create_text(x, y, text=name, fill='white', font=('Arial', 10, 'bold'))
                
                # Детали компьютера (экран, системный блок)
                self.canvas.create_rectangle(x-25, y-15, x-5, y-5, fill='black', outline='gray')
                self.canvas.create_rectangle(x+5, y-15, x+25, y-5, fill='black', outline='gray')
            
            self.device_items[name] = rect_id
            
        # Добавляем статусы
        self.status_texts = {}
        for name, (x, y) in self.devices.items():
            if name != 'SWITCH':
                status_id = self.canvas.create_text(x, y+30, text="Ожидание", 
                                                     fill='white', font=('Arial', 8))
                self.status_texts[name] = status_id
        
        # Индикатор активности коммутатора
        self.switch_activity = self.canvas.create_text(250, 230, text="Активен: 0 пак.",
                                                        fill='white', font=('Arial', 8))
        
    def log_to_console(self, message, color='#00FF00'):
        """Добавляет сообщение в консоль"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        
    def clear_console(self):
        """Очищает консоль"""
        self.console.delete(1.0, tk.END)
        
    def start_simulation(self):
        """Запускает симуляцию"""
        if not self.is_running:
            self.is_running = True
            self.speed = int(self.speed_var.get())
            self.status_label.config(text="Симуляция запущена")
            self.log_to_console("Передача пакетов запущена", '#FFFF00')
            
            # Запускаем потоки
            self.packet_thread = threading.Thread(target=self.generate_packets, daemon=True)
            self.animation_thread = threading.Thread(target=self.animate_packets, daemon=True)
            
            self.packet_thread.start()
            self.animation_thread.start()
            
    def stop_simulation(self):
        """Останавливает симуляцию"""
        self.is_running = False
        self.status_label.config(text="Симуляция остановлена")
        self.log_to_console("Передача пакетов остановлена", '#FF0000')
        self.log_to_console(f"Всего передано пакетов: {self.packet_counter}")
        self.packet_count_label.config(text=str(self.packet_counter))
        
    def generate_packets(self):
        """Генерирует пакеты с заданной скоростью"""
        while self.is_running:
            try:
                # Случайный выбор отправителя и получателя
                sources = ['ПК1', 'ПК2', 'ПК3', 'ПК4']
                dests = ['ПК1', 'ПК2', 'ПК3', 'ПК4']
                
                source = random.choice(sources)
                destination = random.choice([d for d in dests if d != source])
                
                # Случайный размер пакета (50-500 байт)
                size = random.randint(50, 500)
                
                # Создаем пакет
                self.packet_counter += 1
                packet = Packet(self.packet_counter, source, destination, size)
                
                # Добавляем в очередь
                self.packets.append(packet)
                self.switch_buffer.append(packet)
                
                # Обновляем статус отправителя
                self.update_queue.put(('status', source, 'sending'))
                
                # Логируем
                self.update_queue.put(('log', f"Пакет #{packet.id}: {source} -> {destination}, Размер: {size} байт"))
                
                # Обновляем счетчик пакетов
                self.update_queue.put(('count', self.packet_counter))
                
                # Задержка перед следующим пакетом
                time.sleep(1.0 / self.speed)
                
            except Exception as e:
                print(f"Ошибка генерации пакета: {e}")
                
    def animate_packets(self):
        """Анимирует движение пакетов"""
        while self.is_running:
            try:
                for packet in self.packets[:]:
                    if packet.status == "created":
                        # Пакет идет к коммутатору
                        packet.position += 0.02
                        
                        if packet.position >= 1.0:
                            packet.status = "at_switch"
                            packet.position = 0.0
                            
                            # Обновляем статус коммутатора
                            self.update_queue.put(('switch_activity', len(self.switch_buffer)))
                            self.update_queue.put(('log', f"Пакет #{packet.id} достиг SWITCH"))
                            
                    elif packet.status == "at_switch":
                        # Задержка на коммутаторе
                        time.sleep(0.1)
                        
                        # Пакет идет к получателю
                        packet.status = "in_transit"
                        self.update_queue.put(('status', packet.destination, 'receiving'))
                        
                    elif packet.status == "in_transit":
                        packet.position += 0.02
                        
                        if packet.position >= 1.0:
                            packet.status = "delivered"
                            delay = packet.get_delay()
                            
                            # Убираем из буфера коммутатора
                            if packet in self.switch_buffer:
                                self.switch_buffer.remove(packet)
                            
                            # Логируем доставку
                            self.update_queue.put(('log', f"Пакет #{packet.id} доставлен на {packet.destination} (задержка: {delay} мс)"))
                            
                            # Обновляем статусы
                            self.update_queue.put(('status', packet.source, 'idle'))
                            self.update_queue.put(('status', packet.destination, 'idle'))
                            self.update_queue.put(('switch_activity', len(self.switch_buffer)))
                            
                            # Удаляем доставленный пакет
                            self.packets.remove(packet)
                            
                # Рисуем пакеты
                self.update_queue.put(('draw_packets', self.packets))
                
                time.sleep(0.05)  # 20 FPS
                
            except Exception as e:
                print(f"Ошибка анимации: {e}")
                
    def process_queue(self):
        """Обрабатывает очередь обновлений GUI"""
        try:
            while True:
                item = self.update_queue.get_nowait()
                
                if item[0] == 'log':
                    self.log_to_console(item[1])
                elif item[0] == 'status':
                    device, status = item[1], item[2]
                    self.update_device_status(device, status)
                elif item[0] == 'count':
                    self.packet_count_label.config(text=str(item[1]))
                elif item[0] == 'switch_activity':
                    self.canvas.itemconfig(self.switch_activity, text=f"Активен: {item[1]} пак.")
                elif item[0] == 'draw_packets':
                    self.draw_packets(item[1])
                    
        except queue.Empty:
            pass
            
        # Повторяем через 50 мс
        self.root.after(50, self.process_queue)
        
    def update_device_status(self, device, status):
        """Обновляет статус устройства"""
        colors = {
            'idle': '#808080',
            'sending': '#FFFF00',
            'receiving': '#FFA500'
        }
        
        # Обновляем цвет устройства
        if device in self.device_items:
            self.canvas.itemconfig(self.device_items[device], fill=colors.get(status, '#808080'))
            
        # Обновляем текст статуса
        if device in self.status_texts:
            status_text = {
                'idle': 'Ожидание',
                'sending': 'Отправка',
                'receiving': 'Прием'
            }.get(status, 'Ожидание')
            
            self.canvas.itemconfig(self.status_texts[device], text=status_text)
            
    def draw_packets(self, packets):
        """Рисует пакеты на канвасе"""
        # Удаляем старые пакеты
        self.canvas.delete("packet")
        
        for packet in packets:
            if packet.status == "created" or packet.status == "in_transit":
                # Определяем путь пакета
                if packet.status == "created":
                    start = self.devices[packet.source]
                    end = self.devices['SWITCH']
                else:  # in_transit
                    start = self.devices['SWITCH']
                    end = self.devices[packet.destination]
                
                # Интерполяция позиции
                x = start[0] + (end[0] - start[0]) * packet.position
                y = start[1] + (end[1] - start[1]) * packet.position
                
                # Рисуем пакет
                packet_id = self.canvas.create_oval(x-8, y-8, x+8, y+8, 
                                                      fill=packet.color, 
                                                      outline='white', 
                                                      width=2,
                                                      tags="packet")
                
                # Номер пакета
                self.canvas.create_text(x, y, text=str(packet.id), 
                                         fill='white', 
                                         font=('Arial', 8, 'bold'),
                                         tags="packet")
                
    def on_closing(self):
        """Обработчик закрытия окна"""
        self.is_running = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = NetworkTerminal(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()