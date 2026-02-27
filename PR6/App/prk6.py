import tkinter as tk
from tkinter import ttk
import math
import colorsys

class Planet:
    """Класс, представляющий планету Солнечной системы"""
    def __init__(self, name, orbit_radius, speed, size, color, start_angle, description=""):
        self.name = name
        self.orbit_radius = orbit_radius  # относительный радиус орбиты
        self.speed = speed                 # базовая скорость вращения
        self.size = size                   # базовый размер
        self.color = color                  # цвет
        self.angle = math.radians(start_angle)  # текущий угол в радианах
        self.description = description
        self.x = 0
        self.y = 0
        
    def update_position(self, center_x, center_y, zoom):
        """Обновляет позицию планеты на основе угла"""
        display_radius = self.orbit_radius * 50 * zoom  # масштабированный радиус
        self.x = center_x + display_radius * math.cos(self.angle)
        self.y = center_y + display_radius * math.sin(self.angle)
        
    def update_angle(self, speed_multiplier):
        """Обновляет угол планеты"""
        self.angle += self.speed * speed_multiplier

class SolarSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Солнечная система - Интерактивная модель")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Параметры анимации
        self.is_paused = False
        self.speed_multiplier = 1.0
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        
        # Центр системы
        self.center_x = 500
        self.center_y = 350
        
        # Цвета планет
        self.planet_colors = {
            'Меркурий': '#808080',  # серый
            'Венера': '#FFA500',     # оранжевый
            'Земля': '#4169E1',      # королевский синий
            'Марс': '#FF4500',       # оранжево-красный
            'Юпитер': '#D2B48C',     # светло-коричневый
            'Сатурн': '#F4A460',     # песочный
            'Уран': '#40E0D0',       # бирюзовый
            'Нептун': '#000080'      # темно-синий
        }
        
        # Инициализация планет
        self.initialize_planets()
        
        # Настройка интерфейса
        self.setup_ui()
        
        # Запуск анимации
        self.animate()
        
    def initialize_planets(self):
        """Инициализация данных о планетах"""
        self.planets = [
            Planet("Меркурий", 1.0, 0.05, 5, self.planet_colors['Меркурий'], 0,
                   "Самая близкая к Солнцу планета. Температура: от -173°C до +427°C"),
            Planet("Венера", 1.5, 0.03, 7, self.planet_colors['Венера'], 30,
                   "Самая горячая планета. Атмосфера из углекислого газа, давление в 92 раза выше земного"),
            Planet("Земля", 2.0, 0.02, 8, self.planet_colors['Земля'], 60,
                   "Наш дом. Единственная известная планета с жизнью. 70% поверхности покрыто водой"),
            Planet("Марс", 2.5, 0.018, 6, self.planet_colors['Марс'], 90,
                   "Красная планета. Здесь находится самый высокий вулкан в Солнечной системе - Олимп"),
            Planet("Юпитер", 3.2, 0.008, 20, self.planet_colors['Юпитер'], 120,
                   "Крупнейшая планета. Имеет Большое красное пятно - гигантский шторм"),
            Planet("Сатурн", 3.9, 0.006, 17, self.planet_colors['Сатурн'], 150,
                   "Обладает самыми красивыми кольцами. Плотность меньше воды"),
            Planet("Уран", 4.5, 0.004, 12, self.planet_colors['Уран'], 180,
                   "Ледяной гигант. Вращается 'на боку', наклон оси 98 градусов"),
            Planet("Нептун", 5.1, 0.003, 12, self.planet_colors['Нептун'], 210,
                   "Самая дальняя планета. Самые сильные ветры в системе до 2100 км/ч")
        ]
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Верхняя панель управления
        control_frame = ttk.Frame(self.root, padding="5")
        control_frame.pack(fill=tk.X)
        
        # Кнопки управления
        self.pause_btn = ttk.Button(control_frame, text="⏸️ Пауза", command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="⟲ Сброс", command=self.reset_angles).pack(side=tk.LEFT, padx=5)
        
        # Скорость анимации
        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=(20,5))
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(control_frame, from_=0.2, to=3.0, variable=self.speed_var,
                                 orient=tk.HORIZONTAL, length=100, command=self.change_speed)
        speed_scale.pack(side=tk.LEFT, padx=5)
        self.speed_label = ttk.Label(control_frame, text="1.0x")
        self.speed_label.pack(side=tk.LEFT)
        
        # Масштаб
        ttk.Label(control_frame, text="Масштаб:").pack(side=tk.LEFT, padx=(20,5))
        self.zoom_var = tk.DoubleVar(value=1.0)
        zoom_scale = ttk.Scale(control_frame, from_=0.5, to=2.5, variable=self.zoom_var,
                                orient=tk.HORIZONTAL, length=100, command=self.change_zoom)
        zoom_scale.pack(side=tk.LEFT, padx=5)
        self.zoom_label = ttk.Label(control_frame, text="100%")
        self.zoom_label.pack(side=tk.LEFT)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(self.root, text="Информация о планете", padding="5")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_text = tk.StringVar(value="Наведите курсор на планету для получения информации")
        ttk.Label(info_frame, textvariable=self.info_text, font=('Arial', 9)).pack()
        
        # Основной холст для рисования
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Привязка событий
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_click)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Солнечная система | Планеты: 8 | Солнце: желтый карлик G2V")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def toggle_pause(self):
        """Пауза/возобновление анимации"""
        self.is_paused = not self.is_paused
        self.pause_btn.config(text="▶️ Старт" if self.is_paused else "⏸️ Пауза")
        
    def reset_angles(self):
        """Сброс углов планет к начальным значениям"""
        start_angles = [0, 30, 60, 90, 120, 150, 180, 210]
        for planet, angle in zip(self.planets, start_angles):
            planet.angle = math.radians(angle)
            
    def change_speed(self, value):
        """Изменение скорости анимации"""
        self.speed_multiplier = float(value)
        self.speed_label.config(text=f"{self.speed_multiplier:.1f}x")
        
    def change_zoom(self, value):
        """Изменение масштаба"""
        self.zoom = float(value)
        self.zoom_label.config(text=f"{int(self.zoom*100)}%")
        self.canvas.delete("all")
        
    def on_resize(self, event):
        """Обработка изменения размера окна"""
        self.center_x = event.width // 2
        self.center_y = event.height // 2
        
    def on_mousewheel(self, event):
        """Масштабирование колесиком мыши"""
        if event.delta > 0:
            self.zoom = min(self.zoom + 0.1, self.max_zoom)
        else:
            self.zoom = max(self.zoom - 0.1, self.min_zoom)
            
        self.zoom_var.set(self.zoom)
        self.zoom_label.config(text=f"{int(self.zoom*100)}%")
        
    def on_mouse_move(self, event):
        """Отображение информации при наведении на планету"""
        x, y = event.x, event.y
        
        # Проверяем, находится ли курсор над планетой
        for planet in self.planets:
            # Обновляем позиции планет для текущего кадра
            planet.update_position(self.center_x, self.center_y, self.zoom)
            
            # Рассчитываем расстояние до планеты
            distance = math.sqrt((x - planet.x)**2 + (y - planet.y)**2)
            planet_size = planet.size * self.zoom
            
            if distance < planet_size + 5:  # +5 для удобства наведения
                self.info_text.set(f"{planet.name}: {planet.description}")
                return
                
        self.info_text.set("Наведите курсор на планету для получения информации")
        
    def on_click(self, event):
        """Обработка клика по планете"""
        x, y = event.x, event.y
        
        for planet in self.planets:
            planet.update_position(self.center_x, self.center_y, self.zoom)
            distance = math.sqrt((x - planet.x)**2 + (y - planet.y)**2)
            
            if distance < planet.size * self.zoom:
                # Показываем подробную информацию
                self.show_planet_details(planet)
                break
                
    def show_planet_details(self, planet):
        """Показывает детальную информацию о планете"""
        details = f"""
        🌍 {planet.name}
        
        📏 Относительный радиус орбиты: {planet.orbit_radius}
        ⚡ Скорость вращения: {planet.speed:.3f} рад/кадр
        📐 Размер: {planet.size} px
        🎨 Цвет: {planet.color}
        
        ℹ️ {planet.description}
        """
        
        # Создаем всплывающее окно
        popup = tk.Toplevel(self.root)
        popup.title(f"Информация о планете {planet.name}")
        popup.geometry("300x250")
        
        text_widget = tk.Text(popup, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, details)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(popup, text="Закрыть", command=popup.destroy).pack(pady=5)
        
    def draw_stars(self):
        """Рисует звезды на заднем фоне"""
        # Создаем звезды, если их нет
        if not hasattr(self, 'stars'):
            self.stars = []
            import random
            for _ in range(200):
                x = random.randint(0, self.canvas.winfo_width())
                y = random.randint(0, self.canvas.winfo_height())
                size = random.randint(1, 3)
                brightness = random.randint(100, 255)
                color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
                self.stars.append((x, y, size, color))
        
        # Рисуем звезды
        for x, y, size, color in self.stars:
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')
            
    def draw_orbit(self, planet):
        """Рисует орбиту планеты"""
        orbit_radius = planet.orbit_radius * 50 * self.zoom
        
        # Создаем эллипс (орбиту)
        x1 = self.center_x - orbit_radius
        y1 = self.center_y - orbit_radius
        x2 = self.center_x + orbit_radius
        y2 = self.center_y + orbit_radius
        
        # Затемненный цвет для орбиты
        color = '#333333'
        self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=1)
        
    def draw_sun(self):
        """Рисует Солнце"""
        sun_size = 40 * self.zoom
        
        # Градиент для Солнца
        for i in range(5):
            offset = i * 2
            alpha = 255 - i * 40
            if alpha < 0:
                alpha = 0
            color = f'#FFD700'  # золотой
        
        # Основной круг Солнца
        x1 = self.center_x - sun_size
        y1 = self.center_y - sun_size
        x2 = self.center_x + sun_size
        y2 = self.center_y + sun_size
        
        # Сияние
        self.canvas.create_oval(x1-10, y1-10, x2+10, y2+10, 
                                 fill='#FFA500', outline='', stipple='gray50')
        
        # Солнце
        self.canvas.create_oval(x1, y1, x2, y2, 
                                 fill='#FFD700', outline='#FF8C00', width=2)
        
        # Блик
        self.canvas.create_oval(self.center_x-5, self.center_y-5, 
                                 self.center_x+5, self.center_y+5, 
                                 fill='white', outline='')
        
        # Текст "СОЛНЦЕ"
        self.canvas.create_text(self.center_x, self.center_y + sun_size + 20,
                                 text="СОЛНЦЕ", fill='white', font=('Arial', 10, 'bold'))
        
    def draw_planet(self, planet):
        """Рисует планету"""
        planet_size = planet.size * self.zoom
        
        # Ограничиваем размер
        if planet_size < 2:
            planet_size = 2
        if planet_size > 40:
            planet_size = 40
            
        x1 = planet.x - planet_size
        y1 = planet.y - planet_size
        x2 = planet.x + planet_size
        y2 = planet.y + planet_size
        
        # Тень
        self.canvas.create_oval(x1+2, y1+2, x2+2, y2+2, fill='#222222', outline='')
        
        # Планета
        self.canvas.create_oval(x1, y1, x2, y2, fill=planet.color, outline='white', width=1)
        
        # Для Сатурна рисуем кольца
        if planet.name == "Сатурн":
            ring_width = planet_size * 1.5
            ring_height = planet_size * 0.3
            self.canvas.create_oval(planet.x - ring_width, planet.y - ring_height,
                                     planet.x + ring_width, planet.y + ring_height,
                                     outline='#D2B48C', width=2)
        
        # Название планеты
        if self.zoom > 1.2:  # Показываем названия только при достаточном масштабе
            self.canvas.create_text(planet.x, planet.y - planet_size - 10,
                                     text=planet.name, fill='white', font=('Arial', 8))
        
    def animate(self):
        """Основной цикл анимации"""
        if not self.is_paused:
            # Обновляем углы планет
            for planet in self.planets:
                planet.update_angle(self.speed_multiplier)
                
        # Очищаем холст
        self.canvas.delete("all")
        
        # Рисуем звезды
        self.draw_stars()
        
        # Рисуем орбиты (от дальних к ближним)
        for planet in reversed(self.planets):
            self.draw_orbit(planet)
            
        # Рисуем Солнце
        self.draw_sun()
        
        # Обновляем и рисуем планеты
        for planet in self.planets:
            planet.update_position(self.center_x, self.center_y, self.zoom)
            self.draw_planet(planet)
            
        # Обновляем статус
        if not self.is_paused:
            self.status_var.set(f"Солнечная система | Скорость: {self.speed_multiplier:.1f}x | "
                                 f"Масштаб: {int(self.zoom*100)}% | Планет: 8")
        
        # Следующий кадр
        self.root.after(20, self.animate)  # ~50 FPS

def main():
    root = tk.Tk()
    app = SolarSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()