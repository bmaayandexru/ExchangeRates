
import pprint
from tkinter import *
from tkinter import ttk, messagebox
import requests

# Словарь всех валют с кодами и полными названиями
all_currencies = {
    # Криптовалюты
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Coin',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOGE': 'Dogecoin',
    'AVAX': 'Avalanche',
    'DOT': 'Polkadot',
    'MATIC': 'Polygon',
    # Фиатные валюты
    'USDT': 'Tether',
    'BUSD': 'Binance USD',
    'EUR': 'Euro',
    'RUB': 'Russian Ruble',
    'TRY': 'Turkish Lira',
    'GBP': 'British Pound'
}

# Функция для обновления полных названий
def update_names(event=None):
    base_code = base_combobox.get()
    target_code = target_combobox.get()

    base_name.config(text=all_currencies.get(base_code, ''))
    target_name.config(text=all_currencies.get(target_code, ''))


def exchange():
    base = base_combobox.get()
    target = target_combobox.get()

    if not base or not target:
        messagebox.showerror("Ошибка", "Выберите обе валюты!")
        return

    if base == target:
        messagebox.showerror("Ошибка", "Выбраны одинаковые валюты!")
        return

    try:
        response = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={base}{target}",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            # Красивый вывод ответа в консоль
            # print("\nПолный ответ от API:")
            # pprint.pprint(data, indent=2, width=40)
            rate = float(data['price'])
            result = f"1 {base} = {rate:.8f} {target}"
            full_result = (f"1 {base} ({all_currencies[base]})\n"
                           f"= {rate:.8f} {target} ({all_currencies[target]})")
            result_label.config(text=result)
            messagebox.showinfo("Курс обмена", full_result)
        else:
            # Попробуем обратную пару, если прямая не работает
            try:
                response = requests.get(
                    f"https://api.binance.com/api/v3/ticker/price?symbol={target}{base}",
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    rate = 1 / float(data['price'])
                    result = f"1 {base} = {rate:.8f} {target}"
                    full_result = (f"1 {base} ({all_currencies[base]})\n"
                                   f"= {rate:.8f} {target} ({all_currencies[target]})")
                    result_label.config(text=result)
                    messagebox.showinfo("Курс обмена", full_result)
                else:
                    raise Exception(f"Ошибка API: {response.status_code}")
            except:
                raise Exception(f"Пара {base}{target} не найдена")

    except Exception as e:
        error = f"Ошибка: {str(e)}"
        result_label.config(text=error, fg="red")
        messagebox.showerror("Ошибка", error)

# Создаем главное окно
root = Tk()
root.title("Конвертер валют")
root.geometry("500x300")

# Фрейм для базовой валюты
base_frame = Frame(root)
base_frame.pack(pady=10)

Label(base_frame, text="Базовая валюта:").pack(side=LEFT)
base_combobox = ttk.Combobox(base_frame, values=list(all_currencies.keys()))
base_combobox.pack(side=LEFT, padx=5)
base_combobox.set('BTC')
base_name = Label(base_frame, text=all_currencies['BTC'])
base_name.pack(side=LEFT)

# Фрейм для целевой валюты
target_frame = Frame(root)
target_frame.pack(pady=10)

Label(target_frame, text="Целевая валюта:").pack(side=LEFT)
target_combobox = ttk.Combobox(target_frame, values=list(all_currencies.keys()))
target_combobox.pack(side=LEFT, padx=5)
target_combobox.set('USDT')
target_name = Label(target_frame, text=all_currencies['USDT'])
target_name.pack(side=LEFT)

# Метка для результата
result_label = Label(root, text="Выберите валюты и нажмите 'Получить курс'",
                             fg="blue", font=('Arial', 12))
result_label.pack(pady=20)


# Привязка событий
base_combobox.bind("<<ComboboxSelected>>", update_names)
target_combobox.bind("<<ComboboxSelected>>", update_names)

# Кнопка
Button(
    root,
    text="Получить курс",
    command=exchange,
    bg="#4CAF50",
    fg="white",
    font=('Arial', 12),
    padx=20,
    pady=5
).pack(pady=10)

root.mainloop()