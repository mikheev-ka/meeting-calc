import tkinter as tk
from tkinter import messagebox, ttk

class MeetingCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор длительности совещания")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Настройка стиля
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Accent.TButton', font=('Arial', 10, 'bold'),
                             foreground='white', background='#0078d7',
                             bordercolor='#0078d7', focuscolor='none')
        self.style.map('Accent.TButton',
                       background=[('active', '#005a9e')])

        self.total_var = tk.StringVar()
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        self.create_widgets()
        self.root.bind('<Return>', lambda event: self.calculate())

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="Калькулятор длительности совещания",
                                 font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Фрейм для полей ввода
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        # Поле "Накопленное время"
        ttk.Label(input_frame, text="Накопленное время (ЧЧ:ММ):",
                  font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=(0, 2))
        total_entry = ttk.Entry(input_frame, textvariable=self.total_var,
                                width=15, font=('Arial', 11))
        total_entry.grid(row=1, column=0, padx=5, pady=(0, 10))
        total_entry.focus()

        # Поле "Время начала"
        ttk.Label(input_frame, text="Время начала (ЧЧ:ММ):",
                  font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=(0, 2))
        start_entry = ttk.Entry(input_frame, textvariable=self.start_var,
                                width=15, font=('Arial', 11))
        start_entry.grid(row=3, column=0, padx=5, pady=(0, 10))

        # Поле "Время окончания"
        ttk.Label(input_frame, text="Время окончания (ЧЧ:ММ):",
                  font=('Arial', 10)).grid(row=4, column=0, sticky='w', pady=(0, 2))
        end_entry = ttk.Entry(input_frame, textvariable=self.end_var,
                              width=15, font=('Arial', 11))
        end_entry.grid(row=5, column=0, padx=5, pady=(0, 10))

        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)

        calc_btn = ttk.Button(button_frame, text="Рассчитать",
                              command=self.calculate, style='Accent.TButton')
        calc_btn.grid(row=0, column=0, padx=10)

        reset_btn = ttk.Button(button_frame, text="Сбросить",
                               command=self.reset_fields)
        reset_btn.grid(row=0, column=1, padx=10)

        # Фрейм для результата
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Текстовое поле с увеличенным шрифтом
        self.result_text = tk.Text(
            result_frame, height=9, width=70, wrap='word',
            font=('Arial', 12),        # ← увеличенный шрифт
            relief='solid', borderwidth=1,
            highlightthickness=1, highlightcolor='#ccc',
            bg='white'
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Запрещаем редактирование, но оставляем выделение и копирование
        self.result_text.bind('<Key>', self.block_key)
        self.result_text.bind('<Button-3>', self.show_context_menu)

        # Контекстное меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=self.copy_text)

    def block_key(self, event):
        if event.state & 0x4:  # Ctrl
            if event.keysym in ('c', 'C', 'a', 'A'):
                return
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            return
        return 'break'

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        try:
            selected = self.result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected = self.result_text.get(1.0, tk.END).strip()
        if selected:
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.root.update()

    def reset_fields(self):
        self.total_var.set("")
        self.start_var.set("")
        self.end_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.root.focus_set()

    def validate_time(self, time_str, field_name):
        parts = time_str.split(':')
        if len(parts) != 2:
            raise ValueError(f"{field_name} должно быть в формате ЧЧ:ММ")
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
        except ValueError:
            raise ValueError(f"{field_name} должно содержать только цифры")
        if hours < 0 or minutes < 0 or minutes >= 60:
            raise ValueError(f"{field_name} содержит некорректные минуты")
        if field_name != "Накопленное время":
            if not (0 <= hours <= 23):
                raise ValueError(f"{field_name} часы должны быть от 0 до 23")
        return hours, minutes

    def calculate(self):
        try:
            total_str = self.total_var.get().strip()
            start_str = self.start_var.get().strip()
            end_str = self.end_var.get().strip()

            if not total_str or not start_str or not end_str:
                raise ValueError("Заполните все поля")

            total_h, total_m = self.validate_time(total_str, "Накопленное время")
            start_h, start_m = self.validate_time(start_str, "Время начала")
            end_h, end_m = self.validate_time(end_str, "Время окончания")

            start_total = start_h * 60 + start_m
            end_total = end_h * 60 + end_m

            if end_total < start_total:
                duration = (1440 - start_total) + end_total
            else:
                duration = end_total - start_total

            meeting_h = duration // 60
            meeting_m = duration % 60

            total_accumulated = total_h * 60 + total_m + duration
            final_h = total_accumulated // 60
            final_m = total_accumulated % 60

            result = (
                f"Старое накопленное время: {total_h} ч {total_m} мин\n"
                f"Начало совещания: {start_str}\n"
                f"Конец совещания: {end_str}\n"
                f"Длительность совещания: {meeting_h} ч {meeting_m} мин\n"
                f"Новое накопленное время: {final_h} ч {final_m} мин"
            )

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Неожиданная ошибка", f"Произошла ошибка:\n{e}")

def main():
    root = tk.Tk()
    app = MeetingCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()