import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

contando = False

def abrir_tela_sessao():
    centro.pack_forget()
    
    tela_sessao = tk.Frame(janela, bg="#f0f0f0")
    tela_sessao.pack(expand=True)

    tk.Label(tela_sessao, text="Nova Sessão", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

    frame_inputs = tk.Frame(tela_sessao, bg="#f0f0f0")
    frame_inputs.pack()

    tk.Label(frame_inputs, text="Tempo de Estudo (min):", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
    entry_estudo = tk.Entry(frame_inputs, font=("Arial", 14))
    entry_estudo.grid(row=0, column=1, padx=10)

    tk.Label(frame_inputs, text="Tempo de Pausa (min):", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
    entry_pausa = tk.Entry(frame_inputs, font=("Arial", 14))
    entry_pausa.grid(row=1, column=1, padx=10)

    def validar_e_iniciar():
        estudo = entry_estudo.get()
        pausa = entry_pausa.get()
        if not estudo.isdigit() or not pausa.isdigit():
            messagebox.showerror("Erro", "Informe apenas números.")
            return
        tela_sessao.destroy()
        iniciar_cronometro(int(estudo), int(pausa))

    tk.Button(tela_sessao, text="Iniciar", font=("Arial", 13), width=15, command=validar_e_iniciar).pack(pady=20)

def iniciar_cronometro(estudo_min, pausa_min):
    frame_cronometro = tk.Frame(janela, bg="#f0f0f0")
    frame_cronometro.pack(expand=True)

    label_titulo = tk.Label(frame_cronometro, text="Tempo de Estudo", font=("Arial", 20, "bold"), bg="#f0f0f0")
    label_titulo.pack(pady=20)

    label_timer = tk.Label(frame_cronometro, text="", font=("Arial", 40), bg="#f0f0f0")
    label_timer.pack(pady=10)

    botao_terminar = tk.Button(frame_cronometro, text="Terminar Sessão", font=("Arial", 13), width=15,
                                command=lambda: voltar_para_tela_inicial(frame_cronometro))
    botao_terminar.pack(pady=20)

    estudo_seg = estudo_min * 60
    pausa_seg = pausa_min * 60

    def loop_pomodoro():
        nonlocal estudo_seg, pausa_seg
        if not contando:
            return

        if estudo_seg > 0:
            label_titulo.config(text="Tempo de Estudo")
            minutos = estudo_seg // 60
            segundos = estudo_seg % 60
            label_timer.config(text=f"{minutos:02}:{segundos:02}")
            estudo_seg -= 1
        elif pausa_seg > 0:
            label_titulo.config(text="Tempo de Pausa")
            minutos = pausa_seg // 60
            segundos = pausa_seg % 60
            label_timer.config(text=f"{minutos:02}:{segundos:02}")
            pausa_seg -= 1
        else:
            estudo_seg = estudo_min * 60
            pausa_seg = pausa_min * 60

        frame_cronometro.after(1000, loop_pomodoro)

    global contando
    contando = True
    loop_pomodoro()

def voltar_para_tela_inicial(frame_atual):
    global contando
    contando = False
    frame_atual.destroy()
    centro.pack(expand=True)

# ----- JANELA PRINCIPAL -----
janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("1380x750+500+160")

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# IMAGEM DE FUNDO (carregada uma vez, fixa)
try:
    if os.path.exists("FocusFluir.png"):
        imagem_fundo = Image.open("FocusFluir.png")
        imagem_fundo = imagem_fundo.resize((largura_tela, altura_tela), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem_fundo)

        fundo = tk.Label(janela, image=imagem_tk)
        fundo.place(x=0, y=0, relwidth=1, relheight=1)
        fundo.image = imagem_tk
except Exception as e:
    print("Erro ao carregar imagem:", e)

# ----- TELA INICIAL -----
centro = tk.Frame(janela, bg='', bd=0)
centro.pack(expand=True)

botao_iniciar = tk.Button(centro, text="Iniciar Sessão", font=("Arial", 13), width=18, height=2, command=abrir_tela_sessao)
botao_iniciar.pack(pady=(0, 15))

botao_playlist = tk.Button(centro, text="Playlists", font=("Arial", 13), width=18, height=2)
botao_playlist.pack()

janela.mainloop()
