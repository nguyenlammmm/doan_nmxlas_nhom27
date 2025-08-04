import tkinter as tk
from tkinter import simpledialog

def ask_name_popup():
    root = tk.Tk()
    root.withdraw()
    user_name = simpledialog.askstring("Đăng ký người mới", "Nhập tên người mới:")
    root.destroy()
    return user_name
