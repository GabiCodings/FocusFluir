import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from BancoFocusFluir import criar_sessao, salvar_progresso

contando = False

def abrir_tela_sessao():
    centro.pack_forget()
    
    tela_sessao = tk.Frame(janela, bg="#f0f0f0")
    tela_sessao.pack(expand=True)

    tk.Label(tela_sessao, text="Nova Sessão", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

    frame_inputs = tk.Frame(tela_sessao, bg="#f0f0f0")
    frame_inputs.pack()

    tk.Label(frame_inputs, text="Tempo de Estudo (min.seg):", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
    entry_estudo = tk.Entry(frame_inputs, font=("Arial", 14))
    entry_estudo.grid(row=0, column=1, padx=10)

    tk.Label(frame_inputs, text="Tempo de Pausa (min.seg):", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
    entry_pausa = tk.Entry(frame_inputs, font=("Arial", 14))
    entry_pausa.grid(row=1, column=1, padx=10)

    def validar_e_iniciar():
        estudo = entry_estudo.get().strip()
        pausa = entry_pausa.get().strip()

        try:
            
            partes_estudo = estudo.split(".")
            min_estudo = int(partes_estudo[0])
            seg_estudo = int(partes_estudo[1]) if len(partes_estudo) > 1 else 0
            estudo_total = min_estudo * 60 + seg_estudo

            
            partes_pausa = pausa.split(".")
            min_pausa = int(partes_pausa[0])
            seg_pausa = int(partes_pausa[1]) if len(partes_pausa) > 1 else 0
            pausa_total = min_pausa * 60 + seg_pausa

            if estudo_total <= 0 or pausa_total <= 0:
                raise ValueError

        except:
            messagebox.showerror("Erro", "Informe os tempos no formato minutos.segundos (ex: 2.30)")
            return

        tela_sessao.destroy()
        iniciar_cronometro(estudo_total, pausa_total)

    tk.Button(tela_sessao, text="Iniciar", font=("Arial", 13), width=15, command=validar_e_iniciar).pack(pady=20)

def iniciar_cronometro(estudo_seg, pausa_seg):
    frame_cronometro = tk.Frame(janela, bg="#f0f0f0")
    frame_cronometro.pack(expand=True)

    label_titulo = tk.Label(frame_cronometro, text="Tempo de Estudo", font=("Arial", 20, "bold"), bg="#f0f0f0")
    label_titulo.pack(pady=20)

    label_timer = tk.Label(frame_cronometro, text="", font=("Arial", 40), bg="#f0f0f0")
    label_timer.pack(pady=10)

    botao_terminar = tk.Button(frame_cronometro, text="Terminar Sessão", font=("Arial", 13), width=15,
                                command=lambda: voltar_para_tela_inicial(frame_cronometro))
    botao_terminar.pack(pady=20)

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
            estudo_seg = estudo_seg_inicial
            pausa_seg = pausa_seg_inicial

        frame_cronometro.after(1000, loop_pomodoro)

    global contando
    contando = True
    estudo_seg_inicial = estudo_seg
    pausa_seg_inicial = pausa_seg
    loop_pomodoro()

def voltar_para_tela_inicial(frame_atual):
    global contando
    contando = False
    frame_atual.destroy()
    centro.pack(expand=True)


janela = tk.Tk()
janela.title("FocusFluir")
janela.geometry("1380x750+500+160")

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()


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


centro = tk.Frame(janela, bg='', bd=0)
centro.pack(expand=True)

botao_iniciar = tk.Button(centro, text="Iniciar Sessão", font=("Arial", 13), width=18, height=2, command=abrir_tela_sessao)
botao_iniciar.pack(pady=(0, 15))

botao_playlist = tk.Button(centro, text="Playlists", font=("Arial", 13), width=18, height=2)
botao_playlist.pack()

janela.mainloop()
