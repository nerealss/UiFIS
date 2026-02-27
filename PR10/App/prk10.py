import tkinter as tk
from tkinter import ttk, messagebox
import random

class Question:
    """Класс для хранения информации о вопросе теста"""
    def __init__(self, text, options, correct_index, explanation=""):
        self.text = text               # Текст вопроса
        self.options = options          # Список вариантов ответа
        self.correct_index = correct_index  # Индекс правильного ответа (0-3)
        self.explanation = explanation  # Пояснение к ответу

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай стандарт - Тестирующая программа")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        # Настройка стилей
        self.setup_styles()
        
        # Переменные для тестирования
        self.questions = []
        self.current_question = 0
        self.correct_answers = 0
        self.selected_answer = tk.IntVar(value=-1)
        
        # Инициализация вопросов
        self.initialize_questions()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка первого вопроса
        self.load_question()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Question.TLabel", font=("Arial", 12))
        style.configure("Result.TLabel", font=("Arial", 11))
        style.configure("Next.TButton", font=("Arial", 11, "bold"))
        
    def initialize_questions(self):
        """Инициализация списка вопросов о стандартах"""
        self.questions = [
            Question(
                "Какой стандарт определяет представление чисел с плавающей точкой в компьютерах?",
                [
                    "ISO 9001",
                    "IEEE 754",
                    "ASCII",
                    "Unicode"
                ],
                1,  # Правильный ответ: IEEE 754 (индекс 1)
                "IEEE 754 - стандарт IEEE для двоичной арифметики с плавающей точкой, используемый в большинстве процессоров."
            ),
            Question(
                "Какой стандарт описывает требования к системе менеджмента качества?",
                [
                    "IEEE 802.11",
                    "ASCII",
                    "ISO 9001",
                    "Unicode"
                ],
                2,  # Правильный ответ: ISO 9001 (индекс 2)
                "ISO 9001 - международный стандарт по управлению качеством, определяющий требования к системе менеджмента качества."
            ),
            Question(
                "Какой стандарт кодирования символов включает в себя символы всех письменностей мира?",
                [
                    "ASCII",
                    "Unicode",
                    "IEEE 754",
                    "ISO 9001"
                ],
                1,  # Правильный ответ: Unicode (индекс 1)
                "Unicode - стандарт кодирования символов, включающий знаки почти всех письменностей мира."
            ),
            Question(
                "Какой стандарт является основой для беспроводной связи Wi-Fi?",
                [
                    "IEEE 802.11",
                    "IEEE 754",
                    "ISO 9001",
                    "ASCII"
                ],
                0,  # Правильный ответ: IEEE 802.11 (индекс 0)
                "IEEE 802.11 - семейство стандартов для беспроводных локальных сетей (Wi-Fi)."
            ),
            Question(
                "Какой стандарт кодирования символов использовался в первых компьютерах и до сих пор применяется для английского алфавита?",
                [
                    "Unicode",
                    "ISO 9001",
                    "IEEE 754",
                    "ASCII"
                ],
                3,  # Правильный ответ: ASCII (индекс 3)
                "ASCII (American Standard Code for Information Interchange) - стандарт для кодирования латинского алфавита, цифр и специальных символов."
            ),
            Question(
                "Какой стандарт определяет формат обмена данными между различными системами?",
                [
                    "XML",
                    "IEEE 754",
                    "ISO 9001",
                    "ASCII"
                ],
                0,  # Правильный ответ: XML (индекс 0)
                "XML (eXtensible Markup Language) - стандарт для создания документов с структурированными данными."
            ),
            Question(
                "Какой стандарт описывает язык разметки гипертекста для создания веб-страниц?",
                [
                    "HTTP",
                    "HTML",
                    "FTP",
                    "SMTP"
                ],
                1,  # Правильный ответ: HTML (индекс 1)
                "HTML (HyperText Markup Language) - стандартный язык разметки документов во Всемирной паутине."
            ),
            Question(
                "Какой стандарт определяет протокол передачи гипертекста?",
                [
                    "FTP",
                    "SMTP",
                    "HTTP",
                    "TCP/IP"
                ],
                2,  # Правильный ответ: HTTP (индекс 2)
                "HTTP (HyperText Transfer Protocol) - протокол прикладного уровня передачи данных в сети."
            ),
            Question(
                "Какой стандарт используется для сжатия изображений с потерями?",
                [
                    "PNG",
                    "GIF",
                    "JPEG",
                    "BMP"
                ],
                2,  # Правильный ответ: JPEG (индекс 2)
                "JPEG (Joint Photographic Experts Group) - стандарт сжатия изображений с потерями."
            ),
            Question(
                "Какой стандарт определяет формат электронной почты?",
                [
                    "POP3",
                    "IMAP",
                    "SMTP",
                    "Все вышеперечисленные"
                ],
                3,  # Правильный ответ: Все вышеперечисленные (индекс 3)
                "Для работы электронной почты используются несколько стандартов: SMTP для отправки, POP3/IMAP для получения."
            )
        ]
        
        # Перемешиваем вопросы и берем первые 5
        random.shuffle(self.questions)
        self.questions = self.questions[:5]
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Заголовок
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="📚 ТЕСТ: Угадай стандарт", 
                                 style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                    text="Проверьте свои знания о стандартах в области ИТ",
                                    font=("Arial", 10))
        subtitle_label.pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Информационная панель сверху
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Номер вопроса
        self.question_num_label = ttk.Label(info_frame, text="Вопрос 1 из 5",
                                             font=("Arial", 11, "bold"))
        self.question_num_label.pack(side=tk.LEFT)
        
        # Счетчик правильных ответов
        self.score_label = ttk.Label(info_frame, text="Правильных: 0",
                                      font=("Arial", 11))
        self.score_label.pack(side=tk.RIGHT)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(main_frame, length=500, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0, 20))
        self.progress['maximum'] = len(self.questions)
        self.progress['value'] = 0
        
        # Рамка для вопроса
        question_frame = ttk.LabelFrame(main_frame, text="Вопрос", padding=15)
        question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Текст вопроса
        self.question_text = tk.Text(question_frame, height=3, wrap=tk.WORD,
                                      font=("Arial", 12), bg='#f0f0f0', relief=tk.FLAT)
        self.question_text.pack(fill=tk.X, pady=(0, 15))
        self.question_text.config(state=tk.DISABLED)
        
        # Варианты ответов (RadioButton)
        self.radio_frame = ttk.Frame(question_frame)
        self.radio_frame.pack(fill=tk.BOTH, expand=True)
        
        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(
                self.radio_frame,
                text=f"Вариант {i+1}",
                variable=self.selected_answer,
                value=i,
                command=self.on_answer_select
            )
            rb.pack(anchor=tk.W, pady=5)
            self.radio_buttons.append(rb)
        
        # Рамка для результата и кнопки
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Область отображения результата текущего ответа
        self.result_label = ttk.Label(bottom_frame, text="",
                                       font=("Arial", 10), foreground="blue")
        self.result_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка "Далее"
        self.next_btn = ttk.Button(bottom_frame, text="Далее →", 
                                    command=self.next_question,
                                    style="Next.TButton", state=tk.DISABLED)
        self.next_btn.pack(side=tk.RIGHT)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Выберите вариант ответа")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_question(self):
        """Загрузка текущего вопроса"""
        question = self.questions[self.current_question]
        
        # Обновляем текст вопроса
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, question.text)
        self.question_text.config(state=tk.DISABLED)
        
        # Обновляем варианты ответов
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=question.options[i])
        
        # Сбрасываем выбор
        self.selected_answer.set(-1)
        self.result_label.config(text="")
        self.next_btn.config(state=tk.DISABLED)
        
        # Обновляем номер вопроса
        self.question_num_label.config(
            text=f"Вопрос {self.current_question + 1} из {len(self.questions)}"
        )
        
        # Обновляем прогресс
        self.progress['value'] = self.current_question
        
        self.status_var.set("Выберите вариант ответа")
        
    def on_answer_select(self):
        """Обработка выбора ответа"""
        if self.selected_answer.get() != -1:
            self.next_btn.config(state=tk.NORMAL)
            self.status_var.set("Нажмите 'Далее' для продолжения")
            
            # Проверяем правильность ответа (предварительно)
            question = self.questions[self.current_question]
            selected = self.selected_answer.get()
            
            if selected == question.correct_index:
                self.result_label.config(text="✓ Правильно!", foreground="green")
            else:
                self.result_label.config(text="✗ Неправильно", foreground="red")
    
    def next_question(self):
        """Переход к следующему вопросу"""
        # Проверяем правильность ответа
        question = self.questions[self.current_question]
        selected = self.selected_answer.get()
        
        if selected == question.correct_index:
            self.correct_answers += 1
            # Показываем пояснение
            self.show_explanation(question, correct=True)
        else:
            # Показываем пояснение с правильным ответом
            self.show_explanation(question, correct=False)
        
        # Обновляем счетчик
        self.score_label.config(text=f"Правильных: {self.correct_answers}")
        
        # Переходим к следующему вопросу
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            # Загружаем следующий вопрос
            self.root.after(2000, self.load_question)  # Задержка 2 секунды
        else:
            # Тест завершен
            self.progress['value'] = len(self.questions)
            self.root.after(2000, self.show_results)  # Показываем результаты через 2 секунды
    
    def show_explanation(self, question, correct):
        """Показывает пояснение к ответу"""
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        
        if correct:
            self.question_text.insert(tk.END, f"✓ Правильно!\n\n")
        else:
            correct_answer = question.options[question.correct_index]
            self.question_text.insert(tk.END, f"✗ Неправильно. Правильный ответ: {correct_answer}\n\n")
        
        self.question_text.insert(tk.END, question.explanation)
        self.question_text.config(state=tk.DISABLED)
        
        # Отключаем радио-кнопки и кнопку далее на время показа пояснения
        for rb in self.radio_buttons:
            rb.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        
        # Включаем обратно через 2 секунды
        self.root.after(2000, self.enable_controls)
    
    def enable_controls(self):
        """Включает элементы управления после показа пояснения"""
        for rb in self.radio_buttons:
            rb.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.NORMAL)
    
    def show_results(self):
        """Отображение итоговых результатов в отдельном окне"""
        # Рассчитываем процент
        total_questions = len(self.questions)
        percentage = (self.correct_answers / total_questions) * 100
        
        # Создаем новое окно для результатов
        result_window = tk.Toplevel(self.root)
        result_window.title("Результат теста")
        result_window.geometry("400x300")
        result_window.resizable(False, False)
        
        # Делаем окно модальным
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Центрируем окно относительно главного
        result_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (300 // 2)
        result_window.geometry(f"+{x}+{y}")
        
        # Заголовок
        title_label = ttk.Label(result_window, text="РЕЗУЛЬТАТ ТЕСТА", 
                                 font=("Arial", 14, "bold"))
        title_label.pack(pady=20)
        
        # Основной контейнер
        main_frame = ttk.Frame(result_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Результат
        result_text = f"Тест завершен!\n\n"
        result_text += f"Правильных ответов: {self.correct_answers} из {total_questions}\n"
        result_text += f"Процент: {percentage:.1f}%\n\n"
        
        # Оценка
        if percentage == 100:
            result_text += "Оценка: ОТЛИЧНО!\nВы эксперт в стандартах!"
        elif percentage >= 80:
            result_text += "Оценка: ХОРОШО\nНеплохой результат!"
        elif percentage >= 60:
            result_text += "Оценка: УДОВЛЕТВОРИТЕЛЬНО\nСтоит повторить материал"
        else:
            result_text += "Оценка: НЕУДОВЛЕТВОРИТЕЛЬНО\nРекомендуем пройти тест заново"
        
        # Отображаем результат
        result_label = ttk.Label(main_frame, text=result_text, 
                                  font=("Arial", 11), justify=tk.CENTER)
        result_label.pack(pady=20)
        
        # Вопрос о повторном прохождении
        question_label = ttk.Label(main_frame, text="Хотите пройти тест заново?",
                                    font=("Arial", 11))
        question_label.pack(pady=10)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def restart_quiz():
            result_window.destroy()
            self.restart_quiz()
        
        def close_app():
            result_window.destroy()
            self.root.quit()
        
        yes_btn = ttk.Button(button_frame, text="Да", width=10,
                              command=restart_quiz)
        yes_btn.pack(side=tk.LEFT, padx=10)
        
        no_btn = ttk.Button(button_frame, text="Нет", width=10,
                             command=close_app)
        no_btn.pack(side=tk.LEFT, padx=10)
        
        # Обновляем статус
        self.status_var.set(f"Тест завершен. Результат: {self.correct_answers}/{total_questions} ({percentage:.1f}%)")
    
    def restart_quiz(self):
        """Перезапуск теста"""
        # Сбрасываем параметры
        self.current_question = 0
        self.correct_answers = 0
        self.selected_answer.set(-1)
        
        # Перемешиваем и берем новые 5 вопросов
        random.shuffle(self.questions)
        self.questions = self.questions[:5]
        
        # Обновляем UI
        self.score_label.config(text="Правильных: 0")
        self.progress['maximum'] = len(self.questions)
        self.progress['value'] = 0
        
        # Включаем радио-кнопки
        for rb in self.radio_buttons:
            rb.config(state=tk.NORMAL)
        
        # Загружаем первый вопрос
        self.load_question()
        
        self.status_var.set("Тест начат заново. Удачи!")

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()