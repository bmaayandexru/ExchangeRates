import requests
import json
from tkinter import *
from tkinter import messagebox as mb


def exchange():
    return

root = Tk()
root.title("Курсы обмена валют")
root.geometry("400x200+400+400")

Label(text="Введите код валюты").pack(padx=10, pady=10)

entry = Entry()
entry.pack(padx=10, pady=10)

Button(text="Получить курс обмена к доллару", command=exchange).pack(padx=10, pady=10)

root.mainloop()

