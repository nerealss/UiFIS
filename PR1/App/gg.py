import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pymysql
from datetime import datetime
from tkinter import filedialog

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='expansion_proposals',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Подключение к БД успешно")
            self.create_table()
        except pymysql.Error as e:
            print(f"Ошибка подключения: {e}")
            messagebox.showerror("Ошибка БД", f"Не удалось подключиться к БД:\n{e}")
            self.connection = None
    
    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS proposals (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        department VARCHAR(100) NOT NULL,
                        proposal_text TEXT NOT NULL,
                        priority ENUM('Высокий', 'Средний', 'Низкий') DEFAULT 'Средний',
                        cost DECIMAL(10, 2),
                        justification TEXT,
                        implementation_date DATE,
                        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                
                cursor.execute("SELECT COUNT(*) as count FROM proposals")
                result = cursor.fetchone()
                if result['count'] == 0:
                    self.insert_test_data()
        except pymysql.Error as e:
            print(f"Ошибка создания таблицы: {e}")
    
    def insert_test_data(self):
        try:
            with self.connection.cursor() as cursor:
                test_data = [
                    ('Отдел продаж', 'Внедрение CRM системы', 'Высокий', 500000, 'Для автоматизации продаж и улучшения взаимодействия с клиентами', '2024-12-31'),
                    ('Бухгалтерия', 'Обновление 1С', 'Средний', 200000, 'Требуется обновление до последней версии для соответствия законодательству', '2024-10-15'),
                    ('IT отдел', 'Покупка серверного оборудования', 'Высокий', 1000000, 'Требуется для обработки возрастающего объема данных', '2024-11-30')
                ]
                for data in test_data:
                    cursor.execute("""
                        INSERT INTO proposals (department, proposal_text, priority, cost, justification, implementation_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, data)
                self.connection.commit()
        except pymysql.Error as e:
            print(f"Ошибка вставки тестовых данных: {e}")
    
    def get_all_proposals(self):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM proposals ORDER BY id")
                    return cursor.fetchall()
            except pymysql.Error as e:
                print(f"Ошибка получения данных: {e}")
                return []
        return []
    
    def get_proposal(self, proposal_id):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM proposals WHERE id = %s", (proposal_id,))
                    return cursor.fetchone()
            except pymysql.Error as e:
                print(f"Ошибка получения предложения: {e}")
                return None
        return None
    
    def add_proposal(self, data):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    query = """
                        INSERT INTO proposals (department, proposal_text, priority, cost, justification, implementation_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        data['department'], data['proposal_text'], data['priority'],
                        data['cost'], data['justification'], data['implementation_date']
                    ))
                    self.connection.commit()
                    return cursor.lastrowid
            except pymysql.Error as e:
                print(f"Ошибка добавления: {e}")
                messagebox.showerror("Ошибка", f"Не удалось добавить запись:\n{e}")
                return None
        return None
    
    def update_proposal(self, proposal_id, data):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    query = """
                        UPDATE proposals 
                        SET department=%s, proposal_text=%s, priority=%s,
                            cost=%s, justification=%s, implementation_date=%s
                        WHERE id=%s
                    """
                    cursor.execute(query, (
                        data['department'], data['proposal_text'], data['priority'],
                        data['cost'], data['justification'], data['implementation_date'], proposal_id
                    ))
                    self.connection.commit()
                    return True
            except pymysql.Error as e:
                print(f"Ошибка обновления: {e}")
                messagebox.showerror("Ошибка", f"Не удалось обновить запись:\n{e}")
                return False
        return False
    
    def delete_proposal(self, proposal_id):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM proposals WHERE id = %s", (proposal_id,))
                    self.connection.commit()
                    return True
            except pymysql.Error as e:
                print(f"Ошибка удаления: {e}")
                messagebox.showerror("Ошибка", f"Не удалось удалить запись:\n{e}")
                return False
        return False
    
    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

class AddProposalForm:
    def __init__(self, parent, db, callback, proposal_id=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Добавление нового предложения" if not proposal_id else "Редактирование предложения")
        self.window.geometry("500x550")
        self.window.resizable(False, False)
        
        self.db = db
        self.callback = callback
        self.proposal_id = proposal_id
        self.proposal_data = None
        
        if proposal_id:
            self.proposal_data = db.get_proposal(proposal_id)
        
        self.setup_ui()
        
        if self.proposal_data:
            self.fill_fields()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Подразделение:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.department_entry = ttk.Entry(main_frame, width=40)
        self.department_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Предложение:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.proposal_entry = ttk.Entry(main_frame, width=40)
        self.proposal_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Приоритет:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_combo = ttk.Combobox(main_frame, values=['Высокий', 'Средний', 'Низкий'], width=37)
        self.priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.priority_combo.set('Средний')
        
        ttk.Label(main_frame, text="Стоимость (₽):", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cost_entry = ttk.Entry(main_frame, width=40)
        self.cost_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Обоснование:", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.justification_text = scrolledtext.ScrolledText(main_frame, width=38, height=5)
        self.justification_text.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Срок реализации:", font=('Arial', 10)).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=40)
        self.date_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%d.%m.%Y'))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.save_proposal, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.window.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def fill_fields(self):
        if self.proposal_data:
            self.department_entry.insert(0, self.proposal_data['department'])
            self.proposal_entry.insert(0, self.proposal_data['proposal_text'])
            self.priority_combo.set(self.proposal_data['priority'])
            self.cost_entry.insert(0, str(int(self.proposal_data['cost'])) if self.proposal_data['cost'] else '')
            self.justification_text.insert('1.0', self.proposal_data['justification'] or '')
            if self.proposal_data['implementation_date']:
                date_obj = self.proposal_data['implementation_date']
                if isinstance(date_obj, datetime):
                    self.date_entry.delete(0, tk.END)
                    self.date_entry.insert(0, date_obj.strftime('%d.%m.%Y'))
    
    def save_proposal(self):
        if not self.department_entry.get().strip():
            messagebox.showwarning("Предупреждение", "Введите подразделение")
            return
        if not self.proposal_entry.get().strip():
            messagebox.showwarning("Предупреждение", "Введите предложение")
            return
        
        try:
            cost = float(self.cost_entry.get().replace(' ', '').replace('₽', '')) if self.cost_entry.get() else 0
        except ValueError:
            cost = 0
        
        date_str = self.date_entry.get().strip()
        mysql_date = None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                mysql_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Предупреждение", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
                return
        
        data = {
            'department': self.department_entry.get().strip(),
            'proposal_text': self.proposal_entry.get().strip(),
            'priority': self.priority_combo.get(),
            'cost': cost,
            'justification': self.justification_text.get('1.0', tk.END).strip(),
            'implementation_date': mysql_date
        }
        
        if self.proposal_id:
            if self.db.update_proposal(self.proposal_id, data):
                messagebox.showinfo("Успех", "Предложение обновлено")
                self.callback()
                self.window.destroy()
        else:
            if self.db.add_proposal(data):
                messagebox.showinfo("Успех", "Предложение добавлено")
                self.callback()
                self.window.destroy()

class DetailsForm:
    def __init__(self, parent, db, proposal_id, callback):
        self.window = tk.Toplevel(parent)
        self.window.title("ПОДРОБНАЯ ИНФОРМАЦИЯ О ПРЕДЛОЖЕНИИ")
        self.window.geometry("500x450")
        
        self.db = db
        self.proposal_id = proposal_id
        self.callback = callback
        self.proposal = db.get_proposal(proposal_id)
        
        if self.proposal:
            self.setup_ui()
        else:
            messagebox.showerror("Ошибка", "Предложение не найдено")
            self.window.destroy()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        cost_str = f"{int(self.proposal['cost']):,} ₽".replace(',', ' ') if self.proposal['cost'] else '0 ₽'
        date_str = self.proposal['implementation_date'].strftime('%d.%m.%Y') if self.proposal['implementation_date'] else 'Не указан'
        
        info_text = f"""
ID: {self.proposal['id']}
Подразделение: {self.proposal['department']}
Предложение: {self.proposal['proposal_text']}
Приоритет: {self.proposal['priority']}
Стоимость: {cost_str}
Срок реализации: {date_str}

ОБОСНОВАНИЕ:
{self.proposal['justification'] or 'Не указано'}
        """
        
        info_label = tk.Label(main_frame, text=info_text, justify=tk.LEFT, font=('Arial', 10))
        info_label.pack(pady=10, anchor=tk.W)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Редактировать", command=self.edit_proposal, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_proposal, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Закрыть", command=self.window.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def edit_proposal(self):
        self.window.destroy()
        AddProposalForm(self.window.master, self.db, self.callback, self.proposal_id)
    
    def delete_proposal(self):
        if messagebox.askyesno("Подтверждение", "Удалить это предложение?"):
            if self.db.delete_proposal(self.proposal_id):
                messagebox.showinfo("Успех", "Предложение удалено")
                self.callback()
                self.window.destroy()

class ReportForm:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Отчет по предложениям")
        self.window.geometry("700x600")
        
        self.db = db
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Отчет по предложениям", font=('Arial', 16, 'bold')).pack(pady=5)
        
        self.report_text = scrolledtext.ScrolledText(main_frame, width=80, height=25, wrap=tk.WORD, font=('Courier', 10))
        self.report_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Обновить", command=self.load_data, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Печать", command=self.open_print_dialog, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Закрыть", command=self.window.destroy, width=12).pack(side=tk.LEFT, padx=5)
    
    def load_data(self):
        self.report_text.delete('1.0', tk.END)
        
        proposals = self.db.get_all_proposals()
        
        if not proposals:
            self.report_text.insert(tk.END, "Нет данных для отображения")
            return
        
        total = len(proposals)
        high_priority = sum(1 for p in proposals if p['priority'] == 'Высокий')
        total_cost = sum(p['cost'] for p in proposals if p['cost'])
        
        total_cost_str = f"{int(total_cost):,} ₽".replace(',', ' ') if total_cost else '0 ₽'
        
        report = f"""
ОТЧЕТ ПО ПРЕДЛОЖЕНИЯМ О РАСШИРЕНИИ ИС
Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Всего предложений: {total}
Высокоприоритетных: {high_priority}
Общая стоимость: {total_cost_str}

{'='*70}

СПИСОК ПРЕДЛОЖЕНИЙ:

"""
        self.report_text.insert(tk.END, report)
        
        for prop in proposals:
            cost_str = f"{int(prop['cost']):,} ₽".replace(',', ' ') if prop['cost'] else '0 ₽'
            date_str = prop['implementation_date'].strftime('%d.%m.%Y') if prop['implementation_date'] else 'Не указан'
            
            item = f"""
[ID: {prop['id']}] {prop['department']}
Предложение: {prop['proposal_text']}
Приоритет: {prop['priority']} | Стоимость: {cost_str}
Срок: {date_str}
{'-'*50}
"""
            self.report_text.insert(tk.END, item)
    
    def open_print_dialog(self):
        PrintDialog(self.window, self.report_text)

class PrintDialog:
    def __init__(self, parent, report_text_widget):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Печать")
        self.dialog.geometry("450x450")
        self.dialog.resizable(False, False)
        
        self.report_text = report_text_widget
        self.setup_ui()
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Принтер", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0,5))
        
        printer_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        printer_frame.pack(fill=tk.X, pady=5)
        
        printer_header = ttk.Frame(printer_frame)
        printer_header.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(printer_header, text="Имя: Pantum M6500W-series", font=('Arial', 9)).pack(side=tk.LEFT)
        ttk.Button(printer_header, text="Свойства...", command=self.properties, width=10).pack(side=tk.RIGHT)
        
        ttk.Label(printer_frame, text="Состояние: Готов", font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(printer_frame, text="Тип: Pantum-M6500W-Series", font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(printer_frame, text="Место: USB001", font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=2)
        
        comment_frame = ttk.Frame(printer_frame)
        comment_frame.pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(comment_frame, text="Комментарий:", font=('Arial', 9)).pack(side=tk.LEFT)
        self.print_to_file = tk.BooleanVar()
        ttk.Checkbutton(comment_frame, text="Печать в файл", variable=self.print_to_file).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(main_frame, text="Диапазон печати", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10,5))
        
        self.print_range = tk.StringVar(value="all")
        range_frame = ttk.Frame(main_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(range_frame, text="Все", variable=self.print_range, value="all").pack(anchor=tk.W)
        
        pages_frame = ttk.Frame(range_frame)
        pages_frame.pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(pages_frame, text="Страницы с:", variable=self.print_range, value="pages").pack(side=tk.LEFT)
        self.from_entry = ttk.Entry(pages_frame, width=5)
        self.from_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(pages_frame, text="по:").pack(side=tk.LEFT)
        self.to_entry = ttk.Entry(pages_frame, width=5)
        self.to_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(range_frame, text="Выделенный фрагмент", variable=self.print_range, value="selection").pack(anchor=tk.W)
        
        ttk.Label(main_frame, text="Копии", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10,5))
        
        copies_frame = ttk.Frame(main_frame)
        copies_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(copies_frame, text="Число копий:").pack(side=tk.LEFT)
        self.copies_spinbox = ttk.Spinbox(copies_frame, from_=1, to=99, width=5)
        self.copies_spinbox.pack(side=tk.LEFT, padx=5)
        self.copies_spinbox.set(1)
        
        self.collate = tk.BooleanVar()
        ttk.Checkbutton(copies_frame, text="Разобрать по копиям", variable=self.collate).pack(side=tk.LEFT, padx=20)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="OK", command=self.print_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def properties(self):
        messagebox.showinfo("Свойства принтера", "Свойства принтера Pantum M6500W-series")
    
    def print_ok(self):
        if self.print_to_file.get():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        if self.print_range.get() == "selection":
                            try:
                                text = self.report_text.get(tk.SEL_FIRST, tk.SEL_LAST)
                            except tk.TclError:
                                text = self.report_text.get('1.0', tk.END)
                        else:
                            text = self.report_text.get('1.0', tk.END)
                        f.write(text)
                    messagebox.showinfo("Успех", f"Отчет сохранен в файл:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
            else:
                return
        else:
            messagebox.showinfo("Печать", f"Отчет отправлен на печать\nПринтер: Pantum M6500W-series\nКопий: {self.copies_spinbox.get()}")
        
        self.dialog.destroy()

class MainForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Формирование предложений о расширении информационной системы")
        self.root.geometry("900x400")
        
        self.db = Database()
        
        self.setup_ui()
        self.load_data()
        
        self.root.mainloop()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Формирование предложений о расширении информационной системы", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        columns = ('ID', 'Подразделение', 'Предложение', 'Приоритет', 'Стоимость')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Подразделение', text='Подразделение')
        self.tree.heading('Предложение', text='Предложение')
        self.tree.heading('Приоритет', text='Приоритет')
        self.tree.heading('Стоимость', text='Стоимость')
        
        self.tree.column('ID', width=50)
        self.tree.column('Подразделение', width=150)
        self.tree.column('Предложение', width=300)
        self.tree.column('Приоритет', width=100)
        self.tree.column('Стоимость', width=150)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Добавить предложение", command=self.add_proposal, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Просмотр деталей", command=self.view_proposal, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сформировать отчет", command=self.show_report, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Выход", command=self.root.quit, width=15).pack(side=tk.RIGHT, padx=5)
        
        self.tree.bind('<Double-Button-1>', lambda e: self.view_proposal())
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        proposals = self.db.get_all_proposals()
        
        for prop in proposals:
            cost_str = f"{int(prop['cost']):,} ₽".replace(',', ' ') if prop['cost'] else '0 ₽'
            self.tree.insert('', tk.END, values=(
                prop['id'],
                prop['department'],
                prop['proposal_text'],
                prop['priority'],
                cost_str
            ))
    
    def get_selected_id(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите запись")
            return None
        item = self.tree.item(selection[0])
        return item['values'][0]
    
    def add_proposal(self):
        AddProposalForm(self.root, self.db, self.load_data)
    
    def view_proposal(self):
        proposal_id = self.get_selected_id()
        if proposal_id:
            DetailsForm(self.root, self.db, proposal_id, self.load_data)
    
    def show_report(self):
        ReportForm(self.root, self.db)

if __name__ == "__main__":
    app = MainForm()