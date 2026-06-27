import tkinter as tk
from tkinter import ttk

import estilo

class JanelaPrincipal:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.columnconfigure(1, weight=1)
        self.janela_principal.resizable(False, False)

        self.nome_janela = "janela-principal"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Variáveis ---
        # Config
        linha = 0
        link = 6
        espacox = link
        espacoy = link
        # Declaração
        self.lista_completa = []

        # --- Controles ---
        self.controles['janela_principal'] = self.janela_principal

        # Bíblia Sagrada Layout #
        ttk.Label(self.janela_principal, text="Bíblia Sagrada").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        linha += 1
        # ttk.Label(root, text="\u2012" * 300).grid(row=linha, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Separator(self.janela_principal, orient="horizontal").grid(row=linha, columnspan=6, sticky="ew", padx=espacox, pady=espacoy)
        linha += 1

        # Filtro de pastas
        ttk.Label(self.janela_principal, text="Filtro do Livro:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.filtro_livro_txt = ttk.Entry(self.janela_principal, width=50)
        self.filtro_livro_txt.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.filtro_livro_txt.focus_set()  # Define o foco inicial
        self.controles['filtro_livro_txt'] = self.filtro_livro_txt
        linha += 1

        # Combobox de pastas
        ttk.Label(self.janela_principal, text="Livro:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.pastas_cb = ttk.Combobox(self.janela_principal, takefocus=False, state="readonly")
        self.pastas_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.pastas_cb.bind("<<ComboboxSelected>>", self.atualizar_arquivos_biblia)
        self.controles['pastas_cb'] = self.pastas_cb
        linha += 1

    def _criar_barra_menu(self):
        # Criar barra de menu
        self.barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)
        # Menu Ajuda
        self.menu_ajuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.controles['menu_ajuda'] = self.menu_ajuda