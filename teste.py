import tkinter as tk
from PIL import Image, ImageTk
import random

def desenhar_nuvem(x, y):
    pass  # Se quiser ativar as nuvens depois, coloque o código aqui

def redesenhar_nuvens(e):
    print(e)
    largura_tela = e.width
    altura_tela = e.height
    canvas.create_rectangle(0, 0, largura_tela, altura_tela, fill='light blue')
    for n in range(12):
        nx = random.randrange(0, largura_tela)
        ny = random.randrange(0, altura_tela)
        desenhar_nuvem(nx, ny)

janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("1380x750+500+160")
janela.configure(background="light blue")

# Tela do computador
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# Imagem de fundo
image = Image.open("FocusFluir.png")
image = image.resize((largura_tela, altura_tela), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(janela, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image  # Evita garbage collection

# Frame centralizado para os elementos
frame_central = tk.Frame(janela, bg='', bd=0)
frame_central.place(relx=0.5, rely=0.5, anchor="center")  # centro da janela

# E-mail
label_email = tk.Label(frame_central, text="E-mail:", font=("Arial", 12))
label_email.grid(row=0, column=0, padx=10, pady=10)

entry_email = tk.Entry(frame_central, font=("Arial", 12), width=25)
entry_email.grid(row=0, column=1, padx=10, pady=10)

# Senha
label_senha = tk.Label(frame_central, text="Senha:", font=("Arial", 12))
label_senha.grid(row=1, column=0, padx=10, pady=10)

entry_senha = tk.Entry(frame_central, show="*", font=("Arial", 12), width=25)
entry_senha.grid(row=1, column=1, padx=10, pady=10)

# Botão
botao_login = tk.Button(frame_central, text="Entrar", font=("Arial", 12))
botao_login.grid(row=2, column=0, columnspan=2, pady=20)

janela.mainloop()