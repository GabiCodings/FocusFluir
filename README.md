
# FocusFluir

**FocusFluir** é um aplicativo desktop desenvolvido em **Python** que combina **técnicas de produtividade (Pomodoro)** com **playlists relaxantes** para ajudar estudantes a manterem o foco nos estudos.  
Este repositório corresponde ao **Projeto Integrador** do curso **Técnico em Desenvolvimento de Sistemas – Senac Tech**.

## ✨ Funcionalidades

- Criação de sessões de estudo com contagem regressiva (Pomodoro).  
- Configuração de tempo em minutos e segundos (ex.: `2.30` ⇒ 2 min 30 s).  
- Intervalos de pausa automáticos após cada ciclo.  
- Tela de menu com atalho para gerenciamento de playlists (em construção).  
- Imagem de fundo redimensionável para diferentes resoluções.

## 🔧 Tecnologias utilizadas

| Camada | Tecnologia |
| ------ | ---------- |
| Linguagem | **Python 3** |
| Interface gráfica | **Tkinter** |
| Banco de dados local | **SQLite 3** |
| Manipulação de imagens | **Pillow (PIL)** |

> **Observação:** o repositório é 100 % Python segundo o _GitHub Linguist_.

## 🚀 Como executar

1. **Clone** o repositório  
   ```bash
   git clone https://github.com/GabiCodings/FocusFluir.git
   cd FocusFluir
   ```

2. **Crie um ambiente virtual** (opcional, mas recomendado)  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**  
   ```bash
   pip install pillow
   ```

4. **Execute o aplicativo**  
   ```bash
   python FocusFluir.py
   ```

## 📚 Estrutura de pastas

```
FocusFluir/
├── FocusFluir.py       # Código principal da interface
├── BancoFocusFluir.py  # Script de criação do banco SQLite
├── focusfluir.db       # Banco de dados gerado em tempo de execução
├── FocusFluir.png      # Imagem de fundo padrão
└── README.md
```

## 👩‍💻 Autor

Projeto mantido por **Gabriela Schumacher** ([@GabiCodings](https://github.com/GabiCodings)) – aluna do Senac Tech.

---

> Sinta‑se à vontade para abrir **issues** ou **pull requests** com sugestões de melhoria!
