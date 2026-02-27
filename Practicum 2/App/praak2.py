import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy

class FieldOfMiracles:
    def __init__(self, root):
        self.root = root
        self.root.title("ПОЛЕ ЧУДЕС")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Переменные игры
        self.original_word = ""
        self.scrambled_letters = []
        self.selected_letters = []
        self.button_letters = []
        self.history_stack = []  # Для отмены действий
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Привязка событий
        self.setup_bindings()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Header.TLabel", font=("Arial", 11, "bold"))
        style.configure("Letter.TButton", font=("Arial", 14, "bold"), width=3)
        style.configure("Action.TButton", font=("Arial", 11))
        
    def setup_ui(self):
        """Создание пользовательского интерфейса в соответствии с макетом"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="ПОЛЕ ЧУДЕС", 
                                 style="Title.TLabel")
        title_label.pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Рамка для ввода слова
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Введите слово для угадывания:", 
                  font=("Arial", 11)).pack(anchor=tk.W)
        
        input_row = ttk.Frame(input_frame)
        input_row.pack(fill=tk.X, pady=5)
        
        self.word_entry = ttk.Entry(input_row, font=("Arial", 12), width=25)
        self.word_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.word_entry.focus()
        
        self.start_btn = ttk.Button(input_row, text="Начать", 
                                     command=self.start_game,
                                     style="Action.TButton")
        self.start_btn.pack(side=tk.LEFT)
        
        # Рамка для перепутанных букв
        scrambled_frame = ttk.LabelFrame(main_frame, text="Перепутанные буквы:", padding=10)
        scrambled_frame.pack(fill=tk.X, pady=10)
        
        self.scrambled_container = ttk.Frame(scrambled_frame)
        self.scrambled_container.pack()
        
        # Рамка для собранного слова
        selected_frame = ttk.LabelFrame(main_frame, text="Соберите слово (нажимайте кнопки в правильном порядке):", padding=10)
        selected_frame.pack(fill=tk.X, pady=10)
        
        self.selected_container = ttk.Frame(selected_frame)
        self.selected_container.pack()
        
        # Рамка для кнопок действий
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=15)
        
        self.check_btn = ttk.Button(action_frame, text="Проверить", 
                                     command=self.check_word,
                                     style="Action.TButton", state=tk.DISABLED)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        self.new_game_btn = ttk.Button(action_frame, text="Новая игра", 
                                        command=self.new_game,
                                        style="Action.TButton")
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Рамка для результата
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.X, pady=10)
        
        self.result_label = ttk.Label(self.result_frame, text="", 
                                        font=("Arial", 12, "bold"))
        self.result_label.pack()
        
        # Статус бар (скрытый, но оставим для отладки)
        self.status_var = tk.StringVar(value="Введите слово и нажмите 'Начать'")
        
    def setup_bindings(self):
        """Настройка привязок событий"""
        self.root.bind('<Return>', lambda e: self.start_game())
        self.word_entry.bind('<KeyRelease>', self.on_word_entry_change)
        
    def on_word_entry_change(self, event=None):
        """Обработка изменения поля ввода"""
        word = self.word_entry.get().strip()
        if word and all(c.isalpha() for c in word):
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.start_btn.config(state=tk.DISABLED)
    
    def scramble_word(self, word):
        """Перемешивает буквы в слове"""
        letters = list(word.upper())
        random.shuffle(letters)
        return letters
    
    def start_game(self):
        """Начинает новую игру с введенным словом"""
        word = self.word_entry.get().strip()
        
        if not word:
            messagebox.showwarning("Предупреждение", "Введите слово для игры!")
            return
        
        if not all(c.isalpha() for c in word):
            messagebox.showwarning("Предупреждение", "Слово должно содержать только буквы!")
            return
        
        if len(word) < 2:
            messagebox.showwarning("Предупреждение", "Слово должно содержать хотя бы 2 буквы!")
            return
        
        # Сохраняем оригинальное слово
        self.original_word = word.upper()
        
        # Перемешиваем буквы
        self.scrambled_letters = self.scramble_word(word)
        self.selected_letters = []
        self.history_stack = []
        
        # Очищаем поле ввода и блокируем его
        self.word_entry.delete(0, tk.END)
        self.word_entry.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        
        # Обновляем отображение
        self.update_display()
        
        # Активируем кнопки
        self.check_btn.config(state=tk.NORMAL)
        
    def update_display(self):
        """Обновляет отображение игры"""
        # Очищаем контейнеры
        for widget in self.scrambled_container.winfo_children():
            widget.destroy()
        
        for widget in self.selected_container.winfo_children():
            widget.destroy()
        
        # Создаем кнопки для перепутанных букв
        self.button_letters = []
        for i, letter in enumerate(self.scrambled_letters):
            btn = tk.Button(self.scrambled_container, text=letter, 
                            font=("Arial", 14, "bold"), 
                            width=3, height=1,
                            bg='#f0f0f0', relief=tk.RAISED,
                            command=lambda idx=i: self.select_letter(idx))
            btn.grid(row=0, column=i, padx=2, pady=5)
            self.button_letters.append(btn)
        
        # Создаем метки для собранного слова
        self.selected_labels = []
        for i in range(len(self.original_word)):
            if i < len(self.selected_letters):
                letter = self.selected_letters[i]
                fg_color = "black"
            else:
                letter = "?"
                fg_color = "gray"
            
            label = tk.Label(self.selected_container, text=letter, 
                             font=("Arial", 16, "bold"), width=2,
                             fg=fg_color, bg='#f0f0f0', relief=tk.RIDGE)
            label.grid(row=0, column=i, padx=2, pady=5)
            self.selected_labels.append(label)
        
        # Очищаем результат
        self.result_label.config(text="")
    
    def select_letter(self, index):
        """Выбирает букву для добавления в слово"""
        if len(self.selected_letters) >= len(self.original_word):
            return
        
        # Сохраняем состояние для отмены (но пока не используем)
        self.history_stack.append({
            'selected': copy.copy(self.selected_letters),
            'scrambled': copy.copy(self.scrambled_letters),
            'index': index
        })
        
        # Добавляем букву
        letter = self.scrambled_letters.pop(index)
        self.selected_letters.append(letter)
        
        # Обновляем отображение
        self.update_display()
    
    def check_word(self):
        """Проверяет собранное слово"""
        if len(self.selected_letters) != len(self.original_word):
            messagebox.showwarning("Предупреждение", "Соберите слово полностью!")
            return
        
        assembled_word = ''.join(self.selected_letters)
        
        # Очищаем предыдущий результат
        self.result_label.config(text="")
        
        if assembled_word == self.original_word:
            # Правильный ответ - добавляем отдельную метку с поздравлением
            result_text = "Поздравляем! Вы правильно собрали слово!"
            self.result_label.config(text=result_text, foreground="green")
            
            # Блокируем кнопки с буквами
            for btn in self.button_letters:
                btn.config(state=tk.DISABLED)
        else:
            # Неправильный ответ
            result_text = f"Неверно! Правильное слово: {self.original_word}"
            self.result_label.config(text=result_text, foreground="red")
    
    def new_game(self):
        """Начинает новую игру"""
        # Сбрасываем все переменные
        self.original_word = ""
        self.scrambled_letters = []
        self.selected_letters = []
        self.button_letters = []
        self.history_stack = []
        
        # Разблокируем поле ввода
        self.word_entry.config(state=tk.NORMAL)
        self.word_entry.delete(0, tk.END)
        self.start_btn.config(state=tk.NORMAL)
        
        # Блокируем кнопку проверки
        self.check_btn.config(state=tk.DISABLED)
        
        # Очищаем контейнеры
        for widget in self.scrambled_container.winfo_children():
            widget.destroy()
        
        for widget in self.selected_container.winfo_children():
            widget.destroy()
        
        # Очищаем результат
        self.result_label.config(text="")
        
        self.word_entry.focus()

def main():
    root = tk.Tk()
    app = FieldOfMiracles(root)
    root.mainloop()

if __name__ == "__main__":
    main()