import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

def redesenhar_nuvens(e):
    print(e)
    largura_tela =  e.width
    altura_tela = e.height
    canvas.create_rectangle(0, 0, largura_tela, altura_tela, fill='light blue')
    for n in range(12):
        nx = random.randrange(0, largura_tela)
        ny = random.randrange(0, altura_tela)
        desenhar_nuvem(nx, ny)

def abrir_tela_sessao():
    # Esconde o conteúdo atual
    centro.pack_forget()
    
    # Novo frame com campos da sessão
    tela_sessao = tk.Frame(janela, bg="#f0f0f0")
    tela_sessao.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(tela_sessao, text="Nova Sessão", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(tela_sessao, text="Tempo de Estudo (min):", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_estudo = tk.Entry(tela_sessao)
    entry_estudo.grid(row=1, column=1, padx=5)

    tk.Label(tela_sessao, text="Tempo de Pausa (min):", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_pausa = tk.Entry(tela_sessao)
    entry_pausa.grid(row=2, column=1, padx=5)

    tk.Button(tela_sessao, text="Iniciar", font=("Arial", 12), width=15).grid(row=3, column=0, columnspan=2, pady=15)


janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("1380x750+500+160")
janela.configure(background="light blue")

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

print(largura_tela, altura_tela)

# Imagem de fundo
image = Image.open("FocusFluir.png")
image = image.resize((largura_tela, altura_tela), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(janela, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image

# Frame centralizado
centro = tk.Frame(janela, bg='', bd=0)
centro.place(relx=0.5, rely=0.5, anchor="center")

# Botão: Iniciar Sessão
botao_iniciar = tk.Button(centro, text="Iniciar Sessão", font=("Arial", 15), width=20, height=2, command=abrir_tela_sessao)
botao_iniciar.grid(row=0, column=0, pady=(0,0))  # espaçamento abaixo

# Botão: Playlists
botao_playlist = tk.Button(centro, text="Playlists", font=("Arial", 15), width=20, height=2)
botao_playlist.grid(row=1, column=0, pady=(10,0))

janela.mainloop()