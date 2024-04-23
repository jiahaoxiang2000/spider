from calendar import c
from email.mime import base
import tkinter as tk
from tkinter import simpledialog

import tkinter as tk

from antgst import fetch_data, get_auth_code, login, save_data

countryCode = {"India": "0091", "Nigeria": "00234"}
sms = {
    "market": "https://web.antgst.com/antgst/sms/marketing/sendRecordList",
    "otp": "https://web.antgst.com/antgst/sms/otpPremium/sendRecordList",
}


def submit():
    status_label.config(text="Running...")
    root.update()
    user = {}
    option = {}
    username = username_entry.get()
    password = password_entry.get()
    if username != "" or password != "":
        user = {"username": username, "password": password}
    country = country_list.get(country_list.curselection())
    if country != "ALL":
        option = {**option, "countryCode": countryCode[country]}
    page_size = page_size_entry.get()
    if page_size != "":
        option = {**option, "pageSize": page_size}
    sms_type = sms_list.get()
    print(user, option, sms_type)
    base_url = sms[sms_type]

    code, key = get_auth_code()
    token = login(code, key, user)
    response = fetch_data(token, option, base_url)
    save_data(response)
    status_label.config(text="Finished")
    root.update()


root = tk.Tk()

tk.Label(root, text="Username").grid(row=0)
tk.Label(root, text="Password").grid(row=1)
tk.Label(root, text="Data size").grid(row=2)

# Create the status label
status_label = tk.Label(root, text="")

scrollbar = tk.Scrollbar(root)
country_list = tk.Listbox(root, yscrollcommand=scrollbar.set)

country_list.insert(tk.END, "ALL")
for key in countryCode.keys():
    country_list.insert(tk.END, key)

sms_list = tk.Spinbox(root, values=list(sms.keys()))

country_list.selection_set(0)

scrollbar.config(command=country_list.yview)

username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")
page_size_entry = tk.Entry(root)

fetch_button = tk.Button(root, text="Fetch", command=submit)

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)
page_size_entry.grid(row=2, column=1)
sms_list.grid(row=4, column=1)
country_list.grid(row=5, column=0, sticky="nsew")
scrollbar.grid(row=5, column=1, sticky="ns")
status_label.grid(row=6, column=0, columnspan=2)
fetch_button.grid(row=7, column=0, columnspan=2)


if __name__ == "__main__":
    root.mainloop()
