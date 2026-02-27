import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from datetime import datetime

class ElectronicDictionary:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Электронный словарь")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        
        self.yandex_api_key = ""  
        
        self.setup_ui()
        self.setup_bindings()
        
        self.root.mainloop()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Электронный словарь", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)
        
        input_frame = ttk.LabelFrame(main_frame, text="Поиск слова", padding="15")
        input_frame.pack(fill=tk.X, pady=10)
        
        search_frame = ttk.Frame(input_frame)
        search_frame.pack(fill=tk.X)
        
        self.word_entry = ttk.Entry(search_frame, font=('Arial', 14), width=40)
        self.word_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.search_button = ttk.Button(search_frame, text="Найти", 
                                       command=self.search_word, width=15)
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(search_frame, text="Очистить", 
                                      command=self.clear_all, width=15)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.language_label = ttk.Label(input_frame, text="Определён язык: -", 
                                       font=('Arial', 10))
        self.language_label.pack(anchor=tk.W, pady=5)
        
        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=('Arial', 11),
                                  height=20, width=70)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Готов к работе", 
                                     font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(status_frame, text="", font=('Arial', 9))
        self.time_label.pack(side=tk.RIGHT)
        
        self.update_time()
    
    def setup_bindings(self):
        self.word_entry.bind('<Return>', lambda e: self.search_word())
        self.word_entry.bind('<KeyRelease>', self.detect_language)
    
    def detect_language(self, event=None):
        word = self.word_entry.get().strip()
        if not word:
            self.language_label.config(text="Определён язык: -")
            return
        
        if word and word[0].isalpha():
            if word[0].isascii():
                lang = "Английский"
            else:
                lang = "Русский"
            self.language_label.config(text=f"Определён язык: {lang}")
        else:
            self.language_label.config(text="Определён язык: -")
    
    def search_word(self):
        word = self.word_entry.get().strip()
        if not word:
            messagebox.showwarning("Предупреждение", "Введите слово для поиска")
            return
        
        self.search_button.config(state=tk.DISABLED)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', "Поиск...\n")
        self.status_label.config(text="Выполняется запрос...")
        
        thread = threading.Thread(target=self.search_word_thread, args=(word,))
        thread.daemon = True
        thread.start()
    
    def search_word_thread(self, word):
        try:
            if word and word[0].isalpha():
                if word[0].isascii():
                    self.search_english(word)
                else:
                    self.search_russian(word)
            else:
                self.root.after(0, self.show_error, "Не удалось определить язык слова")
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def search_english(self, word):
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, self.display_english_result, data, word)
            elif response.status_code == 404:
                self.root.after(0, self.show_error, f"Слово '{word}' не найдено в словаре")
            else:
                self.root.after(0, self.show_error, f"Ошибка API: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.root.after(0, self.show_error, f"Ошибка сети: {str(e)}")
    
    def search_russian(self, word):
        try:
            # Проверяем, есть ли ключ
            if not self.yandex_api_key or self.yandex_api_key.startswith("dict.1.1.2025"):
                self.root.after(0, self.show_error, "Необходимо указать ключ Yandex Dictionary API\n\nПолучите ключ на https://yandex.ru/dev/dictionary/")
                return
            
            url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
            params = {
                "key": self.yandex_api_key,
                "lang": "ru-ru",
                "text": word,
                "ui": "ru"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, self.display_russian_result, data, word)
            else:
                self.root.after(0, self.show_error, f"Ошибка Yandex API: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.root.after(0, self.show_error, f"Ошибка сети: {str(e)}")
    
    def display_english_result(self, data, word):
        self.result_text.delete('1.0', tk.END)
        
        result = f"{'='*60}\n"
        result += f"СЛОВО: {word.upper()}\n"
        result += f"{'='*60}\n\n"
        
        for entry in data:
            if "phonetic" in entry and entry["phonetic"]:
                result += f"Транскрипция: {entry['phonetic']}\n\n"
            
            if "meanings" in entry:
                for meaning in entry["meanings"]:
                    part_of_speech = meaning.get("partOfSpeech", "Не указано")
                    result += f"📌 {part_of_speech.upper()}\n"
                    result += f"{'-'*40}\n"
                    
                    if "definitions" in meaning:
                        for i, definition in enumerate(meaning["definitions"], 1):
                            result += f"{i}. {definition.get('definition', 'Нет определения')}\n"
                            
                            if "example" in definition and definition["example"]:
                                result += f"   Пример: {definition['example']}\n"
                            
                            if "synonyms" in definition and definition["synonyms"]:
                                synonyms = definition["synonyms"][:3]
                                if synonyms:
                                    result += f"   Синонимы: {', '.join(synonyms)}\n"
                            
                            result += "\n"
            
            result += f"{'='*60}\n\n"
        
        self.result_text.insert('1.0', result)
        self.status_label.config(text=f"Найдено определений: {len(data)}")
        self.update_status(word)
    
    def display_russian_result(self, data, word):
        self.result_text.delete('1.0', tk.END)
        
        result = f"{'='*60}\n"
        result += f"СЛОВО: {word.upper()}\n"
        result += f"{'='*60}\n\n"
        
        if "def" in data and data["def"]:
            for definition in data["def"]:
                if "pos" in definition:
                    result += f"📌 {definition['pos'].upper()}\n"
                if "ts" in definition:
                    result += f"Транскрипция: [{definition['ts']}]\n"
                result += f"{'-'*40}\n"
                
                if "tr" in definition:
                    for i, translation in enumerate(definition["tr"], 1):
                        result += f"{i}. {translation.get('text', 'Нет перевода')}\n"
                        
                        if "pos" in translation:
                            result += f"   Часть речи: {translation['pos']}\n"
                        
                        if "syn" in translation and translation["syn"]:
                            synonyms = [s.get('text', '') for s in translation["syn"][:3]]
                            result += f"   Синонимы: {', '.join(synonyms)}\n"
                        
                        if "mean" in translation and translation["mean"]:
                            meanings = [m.get('text', '') for m in translation["mean"][:2]]
                            result += f"   Значения: {', '.join(meanings)}\n"
                        
                        result += "\n"
        else:
            result += "Определение не найдено\n"
        
        self.result_text.insert('1.0', result)
        self.status_label.config(text="Результат получен")
        self.update_status(word)
    
    def show_error(self, message):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', f"ОШИБКА:\n{message}\n\n")
        self.status_label.config(text="Ошибка")
        self.search_button.config(state=tk.NORMAL)
        messagebox.showerror("Ошибка", message)
    
    def update_status(self, word=""):
        current_time = datetime.now().strftime("%H:%M:%S")
        if word:
            self.time_label.config(text=f"Последний поиск: {word} в {current_time}")
        else:
            self.time_label.config(text="")
        self.search_button.config(state=tk.NORMAL)
    
    def update_time(self):
        if not hasattr(self, 'time_label'):
            return
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        if not self.time_label.cget("text").startswith("Последний поиск"):
            self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def clear_all(self):
        self.word_entry.delete(0, tk.END)
        self.result_text.delete('1.0', tk.END)
        self.language_label.config(text="Определён язык: -")
        self.status_label.config(text="Готов к работе")
        self.time_label.config(text="")
        self.search_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = ElectronicDictionary()