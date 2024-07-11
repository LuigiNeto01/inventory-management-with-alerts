import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import json
import os

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.wind_wid = 1000
        self.wind_hei = 800

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.position_x = (self.screen_width - self.wind_wid) // 2
        self.position_y = (self.screen_height - self.wind_hei) // 2

        self.root.geometry(f"{self.wind_wid}x{self.wind_hei}+{self.position_x}+{self.position_y}")
        self.root.configure(bg="white")
        self.root.title('Gestão de estoque')

        self.config_file = 'config.json'
        self.popup_duration = self.load_config()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.tab_gestao = ttk.Frame(self.notebook)
        self.tab_configuracao = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_gestao, text="Gestão")
        self.notebook.add(self.tab_configuracao, text="Configuração")

        self.tree = ttk.Treeview(self.tab_gestao, columns=("Nome", "Quantidade"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.pack(expand=True, fill="both")

        self.notebook.select(self.tab_gestao)

        self.previous_data = {}

        self.create_config_tab()

        self.check_data_periodically()

    def db_connect(self):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="estoque"
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def fetch_data(self):
        conexao = self.db_connect()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, quantidade FROM estoque_prod")
            rows = cursor.fetchall()
            conexao.close()
            return rows
        else:
            return []

    def show_data(self):
        for row in self.fetch_data():
            self.tree.insert("", "end", values=row)

    def check_data_periodically(self):
        new_data = self.fetch_data()
        new_data_dict = {row[0]: int(row[1]) for row in new_data}

        if self.previous_data:
            for nome, quantidade in new_data_dict.items():
                if nome in self.previous_data:
                    if quantidade != self.previous_data[nome]:
                        if int(quantidade) > self.previous_data[nome]:
                            self.show_popup(f"O item '{nome}' teve um aumento de quantidade: {int(quantidade) - self.previous_data[nome]}")
                        else:
                            self.show_popup(f"O item '{nome}' teve uma diminuição de quantidade: {self.previous_data[nome] - int(quantidade)}")
                else:
                    self.show_popup(f"Novo item adicionado: {nome} com quantidade {int(quantidade)}")

            for nome in self.previous_data:
                if nome not in new_data_dict:
                    self.show_popup(f"O item '{nome}' foi removido do estoque")

        self.previous_data = new_data_dict

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.show_data()

        self.root.after(5000, self.check_data_periodically)

    def show_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title('Alerta de estoque')
        label = tk.Label(popup, text=message, padx=20, pady=20)
        label.pack()
        self.root.after(self.popup_duration * 1000, popup.destroy)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config.get('popup_duration', 3)
        else:
            return 3

    def save_config(self):
        config = {'popup_duration': self.popup_duration}
        with open(self.config_file, 'w') as file:
            json.dump(config, file)

    def create_config_tab(self):
        duration_label = tk.Label(self.tab_configuracao, text="Duração do Pop-up (segundos):")
        duration_label.pack(pady=10)

        self.duration_entry = tk.Entry(self.tab_configuracao)
        self.duration_entry.pack(pady=10)
        self.duration_entry.insert(0, str(self.popup_duration))

        save_button = tk.Button(self.tab_configuracao, text="Salvar Configuração", command=self.update_config)
        save_button.pack(pady=10)

    def update_config(self):
        try:
            self.popup_duration = int(self.duration_entry.get())
            self.save_config()
            messagebox.showinfo("Configuração", "Configuração salva com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos")

root = tk.Tk()
app = EstoqueApp(root)
root.mainloop()
