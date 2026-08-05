import tkinter as tk
from tkinter import ttk


class JanelaMusica:
    def __init__(self, janela_principal):
        self.janela_musica = tk.Toplevel(janela_principal)
        self.janela_musica.title("Músicas Gospel")
        self.janela_musica.resizable(False, False)

        self.nome_janela = "janela-musica"
        self.controles = {}

        self.criar_layout()
        self.criar_barra_menu()

    def criar_layout(self):
        linha = 0
        link = 6
        espacox = link
        espacoy = link

        # Filtro das músicas
        ttk.Label(self.janela_musica, text="Filtro do Livro:").grid(row=linha, column=0, padx=espacox, pady=espacoy,
                                                                       sticky="w")
        self.filtro_musica_txt = ttk.Entry(self.janela_musica, width=50)
        self.filtro_musica_txt.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.filtro_musica_txt.focus_set()  # Define o foco inicial
        self.controles['filtro_musica_txt'] = self.filtro_musica_txt
        linha += 1



    def criar_barra_menu(self):
        pass
