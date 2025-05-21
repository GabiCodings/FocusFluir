import tkinter as tk
from tkinter import messagebox
import random

def desenhar_nuvem(x, y):
    cor = 'white'
    
    canvas.create_oval(x,  y, x+60, y+40, fill=cor, outline=cor)
    canvas.create_oval(x+30, y-20, x+90, y+30, fill=cor, outline=cor)
    canvas.create_oval(x+60, y, x+120, y+40, fill=cor, outline=cor)
    canvas.create_oval(x+30, y+10, x+90, y+50, fill=cor, outline=cor)



def redesenhar_nuvens(e):
    print(e)
    largura_tela =  e.width
    altura_tela = e.height
    canvas.create_rectangle(0,0,largura_tela,altura_tela,fill='light blue')
    for n in range(10):
        nx = random.randrange(0,largura_tela)
        ny = random.randrange(0,altura_tela)
        desenhar_nuvem(nx, ny)


janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("950x650+500+160")
janela.configure(background="light blue")


largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

print(largura_tela, altura_tela)

canvas = tk.Canvas(janela, width=largura_tela, height=altura_tela, bg='light blue', highlightthickness=0)
canvas.pack()
janela.bind("<Configure>", redesenhar_nuvens)


janela.mainloop()