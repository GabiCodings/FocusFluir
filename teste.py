import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Formulário de Cadastro")
janela.geometry("400x250")



label_nome = tk.Label(janela, text="Nome:", font=("Arial", 12))
label_nome.grid(row=0, column=0, sticky="e", padx=10, pady=10)


janela.mainloop()