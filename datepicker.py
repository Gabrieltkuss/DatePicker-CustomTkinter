import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import calendar

#PARA IMPORTAÇÃO DIRETA
class CTkDatePicker(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.calendar_button = ctk.CTkButton(self, text="▼", width=30, command=self.open_calendar)  # Ajuste a largura aqui
        self.calendar_button.grid(row=0, column=1, sticky="ew", padx=0, pady=5)  # Ajuste o padx para 0

        self.popup = None
        self.selected_date = None
        self.date_format = "%d/%m/%Y %H:%M"
        self.allow_manual_input = True

    def set_date_format(self, date_format):
        self.date_format = date_format

    def open_calendar(self):
        if self.popup is not None:
            self.popup.destroy()
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Date")
        self.popup.geometry("+%d+%d" % (self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()))
        self.popup.resizable(False, False)

        self.popup.after(500, lambda: self.popup.focus())

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.build_calendar()
        self.build_time_selector()

    def build_calendar(self):
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.destroy()

        self.calendar_frame = ctk.CTkFrame(self.popup)
        self.calendar_frame.grid(row=0, column=0, columnspan=7)

        month_name = self.get_month_name(self.current_month) + " " + str(self.current_year)
        month_label = ctk.CTkLabel(self.calendar_frame, text=month_name)
        month_label.grid(row=0, column=1, columnspan=5)

        prev_month_button = ctk.CTkButton(self.calendar_frame, text="<", width=5, command=self.prev_month)
        prev_month_button.grid(row=0, column=0)

        next_month_button = ctk.CTkButton(self.calendar_frame, text=">", width=5, command=self.next_month)
        next_month_button.grid(row=0, column=6)

        days_pt_br = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for i, day in enumerate(days_pt_br):
            lbl = ctk.CTkLabel(self.calendar_frame, text=day)
            lbl.grid(row=1, column=i)

        today = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_date = datetime.now()

        month_days = calendar.monthrange(self.current_year, self.current_month)[1]
        start_day = calendar.monthrange(self.current_year, self.current_month)[0]
        start_day = (start_day + 1) % 7  # Ajustando para começar na segunda-feira

        day = 1
        for week in range(2, 8):
            for day_col in range(7):
                if week == 2 and day_col < start_day:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                elif day > month_days:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                else:
                    day_date = datetime(self.current_year, self.current_month, day)
                    if day_date > current_date:
                        btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=3, command=lambda day=day: self.select_date(day), fg_color="#505050", state="disabled")  # Desabilitar dias futuros
                    else:
                        if (day == today and self.current_month == current_month and self.current_year == current_year):
                            btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=3, command=lambda day=day: self.select_date(day), fg_color="darkblue")
                        else:
                            btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=3, command=lambda day=day: self.select_date(day), fg_color="transparent")
                    btn.grid(row=week, column=day_col)
                    day += 1

    def build_time_selector(self):
        def on_mouse_wheel(event, spinbox, var, step=1):
            try:
                if event.delta > 0:  # Scroll para cima
                    new_value = var.get() + step
                else:  # Scroll para baixo
                    new_value = var.get() - step

                # Limita o valor dentro do intervalo permitido
                if spinbox == hour_spinbox:
                    if 0 <= new_value <= 23:
                        var.set(new_value)
                elif spinbox == minute_spinbox:
                    if 0 <= new_value <= 59:
                        var.set(new_value)
            except ValueError:
                var.set(0)

        time_frame = ctk.CTkFrame(self.popup)
        time_frame.grid(row=8, column=0, columnspan=7, pady=10)

        hour_label = ctk.CTkLabel(time_frame, text="Hora:")
        hour_label.grid(row=0, column=0, padx=5)

        self.hour_var = tk.IntVar(value=datetime.now().hour)
        hour_spinbox = tk.Spinbox(
            time_frame,
            bg="#3e3e42",
            fg="#56ff5d",
            from_=0,
            to=23,
            textvariable=self.hour_var,
            width=4,
            font=("Helvetica", 14),
            # format="%02.0f"
        )
        hour_spinbox.grid(row=0, column=1, padx=5, pady=5)
        hour_spinbox.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, hour_spinbox, self.hour_var))

        minute_label = ctk.CTkLabel(time_frame, text="Minuto:")
        minute_label.grid(row=0, column=2, padx=5)

        self.minute_var = tk.IntVar(value=datetime.now().minute)
        minute_spinbox = tk.Spinbox(
            time_frame,
            bg="#3e3e42",
            fg="#56ff5d",
            from_=0,
            to=59,
            textvariable=self.minute_var,
            width=4,
            font=("Helvetica", 14),
            # format="%02.0f"
        )
        minute_spinbox.grid(row=0, column=3, padx=5, pady=5)
        minute_spinbox.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, minute_spinbox, self.minute_var))

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def select_date(self, day):
        current_datetime = datetime.now()

        # Cria a data selecionada com o horário atual
        selected_datetime = datetime(self.current_year, self.current_month, day, self.hour_var.get(), self.minute_var.get())

        # Verifica se a data selecionada é maior que a data atual
        if selected_datetime > current_datetime:
            # Se for maior, exibe uma mensagem e retorna sem fazer nada
            print("Não é possível selecionar uma data e hora no futuro.")
            return

        self.date_entry.configure(state='normal')

        # Garantindo que o dia, mês, hora e minuto tenham sempre dois dígitos
        formatted_day = f"{day:02d}"
        formatted_month = f"{self.current_month:02d}"
        formatted_hour = f"{self.hour_var.get():02d}"
        formatted_minute = f"{self.minute_var.get():02d}"

        # Inserindo a data formatada no campo de entrada
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, f"{formatted_day}/{formatted_month}/{self.current_year} {formatted_hour}:{formatted_minute}")

        if not self.allow_manual_input:
            self.date_entry.configure(state='disabled')
        self.popup.destroy()
        self.popup = None


    def get_month_name(self, month_num):
        months_pt_br = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        return months_pt_br[month_num - 1]

    def get_date(self):
        return self.date_entry.get()
    
    def set_allow_manual_input(self, value):
        self.allow_manual_input = value
        if not value:
            self.date_entry.configure(state='disabled')
        else:
            self.date_entry.configure(state='normal')
