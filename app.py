from calendar import c
import tkinter as tk
from tkinter import simpledialog

import tkinter as tk

from antgst import fetch_data, get_auth_code, login, save_data

countryCode = {"India": "0091", "Nigeria": "00234"}


def submit():
    status_label.config(text="Running...")
    root.update()
    user = {}
    option = {}
    username = username_entry.get()
    password = password_entry.get()
    if username != "" or password != "":
        user = {"username": username, "password": password}
    country = listbox.get(listbox.curselection())
    if country != "ALL":
        option = {**option, "countryCode": countryCode[country]}
    page_size = page_size_entry.get()
    if page_size != "":
        option = {**option, "pageSize": page_size}
    print(user, option)
    code, key = get_auth_code()
    token = login(code, key, user)
    response = fetch_data(token, option)
    save_data(response)
    status_label.config(text="Finished")
    root.update()


root = tk.Tk()

tk.Label(root, text="Username").grid(row=0)
tk.Label(root, text="Password").grid(row=1)
tk.Label(root, text="Data size").grid(row=2)
tk.Label(root, text="Country").grid(row=3)

# Create the status label
status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=2)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=4, column=1, sticky="ns")

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)

listbox.insert(tk.END, "ALL")
for key in countryCode.keys():
    listbox.insert(tk.END, key)

listbox.selection_set(0)
listbox.grid(row=4, column=0, sticky="nsew")

scrollbar.config(command=listbox.yview)

username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")
page_size_entry = tk.Entry(root)


username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)
page_size_entry.grid(row=2, column=1)


fetch_button = tk.Button(root, text="Fetch", command=submit)
fetch_button.grid(row=6, column=0, columnspan=2)


if __name__ == "__main__":
    root.mainloop()
