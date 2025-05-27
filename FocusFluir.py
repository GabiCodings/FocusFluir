import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

def redesenhar_nuvens(e):
    print(e)
    largura_tela =  e.width
    altura_tela = e.height
    canvas.create_rectangle(0,0,largura_tela,altura_tela,fill='light blue')
    for n in range(12):
        nx = random.randrange(0,largura_tela)
        ny = random.randrange(0,altura_tela)
        desenhar_nuvem(nx, ny)



janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("1380x750+500+160")
janela.configure(background="light blue")


largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

print(largura_tela, altura_tela)


image = Image.open("FocusFluir.png")
image = image.resize((largura_tela, altura_tela), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(janela, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image

centro = tk.Frame(janela, bg='',bd=0)
centro.place(relx=0.5, rely=0.5, anchor="center")
#canvas = tk.Canvas(janela, width=largura_tela, height=altura_tela, bg='light blue', highlightthickness=0)
#canvas.grid(0,0)
#janela.bind("<Configure>", redesenhar_nuvens)

botao_login = tk.Button(centro, text="Entrar", font=("Arial", 15), width=15, height=2)
botao_login.grid(row=1, column=0, columnspan=2, pady=1)

janela.mainloop()