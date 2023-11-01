import re
import tkinter as tk
from tkinter import messagebox
from user import User
import csv
'''1a@2b@3c@ admin'''
'''4d@5e@6f@ user44'''
def save_users_to_file(users):
    with open("database.csv", 'w', newline='') as csvfile:
        fieldnames = ['username', 'password', 'role', 'login_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(vars(user))

# Загрузим пользователей из CSV файла
users = []
with open("database.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user = User(row['username'], row['password'], row['role'], row['login_count'])
        users.append(user)

def login_check():
    username = username_entry.get()
    found_user = None
    for user in users:
        if user.username == username:
            found_user = user
            break

    if found_user:
        # Сохраним пользователя, чтобы использовать его в функции login
        login_check.user = found_user
        password_label.pack()
        password_entry.pack()
        login_button2.pack()
    else:
        messagebox.showerror("Ошибка", "Неправильный логин")

def login():
    if 'login_check' not in globals() or not hasattr(login_check, 'user'):
        messagebox.showerror("Ошибка", "Сначала введите логин")
        return

    user = login_check.user
    entered_password = password_entry.get()

    if user.password == matrix_shuffle(entered_password):
        user.login_count = int(user.login_count) + 1
        save_users_to_file(users)
        username_entry.delete('0','end')
        password_entry.delete('0','end')
        password_label.pack_forget()
        password_entry.pack_forget()
        login_button2.pack_forget()
        open_panel(user)
    else:
        messagebox.showerror("Ошибка", "Неправильный пароль")
        username_entry.delete('0','end')
        password_entry.delete('0','end')
        password_label.pack_forget()
        password_entry.pack_forget()
        login_button2.pack_forget()

def open_panel(user):
    if user.role == "admin":
        open_admin_panel()
    else:
        open_user_panel()

def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Панель администратора")
    
    user_listbox = tk.Listbox(admin_window)
    for user in users:
        user_info = f"{user.username} (Входов: {user.login_count} {user.password})"
        user_listbox.insert(tk.END, user_info)
    
    user_listbox.pack()
    
    def delete_user():
        selected_user = user_listbox.get(user_listbox.curselection())
        selected_user = selected_user.split(" ")[0]
        for user in users:
            if user.username == selected_user:
                users.remove(user)
                user_listbox.delete(tk.ACTIVE)
                save_users_to_file(users)
                break
    
    delete_button = tk.Button(admin_window, text="Удалить пользователя", command=delete_user)
    delete_button.pack()

    def open_registration_window():
        registration_window = tk.Toplevel(admin_window)
        registration_window.title("Регистрация нового пользователя")
        
        new_username_label = tk.Label(registration_window, text="Имя пользователя:")
        new_username_label.pack()
        new_username_entry = tk.Entry(registration_window)
        new_username_entry.pack()
        
        new_password_label = tk.Label(registration_window, text="Пароль:")
        new_password_label.pack()
        new_password_entry = tk.Entry(registration_window, show="*")
        new_password_entry.pack()

        def is_valid_password(password):
            return re.match(r'^\d[a-zA-Z]@\d[a-zA-Z]@\d[a-zA-Z]@$', password)
        
        def register_new_user():
            new_username = new_username_entry.get()
            new_password = new_password_entry.get()
            new_logincount = 0
            if not new_username or not new_password:
                messagebox.showerror("Ошибка", "Имя пользователя и пароль не могут быть пустыми")
                return
            
            if not is_valid_password(new_password):
                messagebox.showerror("Ошибка", "Пароль должен быть вида 1a@2b@3c@")
                return
            
            for user in users:
                if user.username == new_username:
                    messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
                    return
                
            new_password = matrix_shuffle(new_password)
            new_user = User(new_username, new_password, "user", new_logincount)
            users.append(new_user)
            user_listbox.insert(tk.END, user_info)
            messagebox.showinfo("Успешно", "Пользователь зарегистрирован")

            with open("database.csv", 'a', newline='') as csvfile:
                fieldnames = ['username','password','role','login_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(vars(new_user))

            registration_window.destroy()
        
        register_button = tk.Button(registration_window, text="Зарегистрировать", command=register_new_user)
        register_button.pack()
    
    register_button = tk.Button(admin_window, text="Зарегистрировать нового пользователя", command=open_registration_window)
    register_button.pack()

def open_user_panel():
    user_window = tk.Toplevel(root)
    user_window.title("Панель пользователя")
    welcome_label = tk.Label(user_window, text="Добро пожаловать, пользователь!")
    welcome_label.pack()

def matrix_shuffle(input_string):
    if len(input_string) == 9:
        return ''.join(input_string[i] for i in [6, 1, 2, 7, 3, 5, 8, 4, 0])
    else: return input_string

root = tk.Tk()
root.title("Система учетных записей")
root.geometry("400x300")

username_label = tk.Label(root, text="Имя пользователя:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_entry = tk.Entry(root, show="*")

login_button = tk.Button(root, text="Ввод логина", command=login_check)
login_button.pack()

login_button2 = tk.Button(root, text="Ввод пароля", command=login)
password_label.pack_forget()
password_entry.pack_forget()
login_button2.pack_forget()

root.mainloop()
