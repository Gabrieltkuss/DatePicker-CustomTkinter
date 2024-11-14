import tkinter as tk
import customtkinter as ctk
from CTkDatePicker import CTkDatePicker #LIB IMPORT
# from datepicker import CTkDatePicker #DIRECT IMPORT

def main():
    root = ctk.CTk()
    root.geometry("400x300")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    date_picker = CTkDatePicker(root)
    date_picker.pack(pady=20)

    def print_date():
        print(f"Selected Date: {date_picker.get_date()}")

    btn = ctk.CTkButton(root, text="Print Date", command=print_date)
    btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()