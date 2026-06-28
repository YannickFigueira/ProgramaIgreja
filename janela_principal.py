import os
import tkinter as tk
from tkinter import ttk

import dados
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
        self.controles['pastas_cb'] = self.pastas_cb
        linha += 1

        # Campo de filtro de arquivos
        ttk.Label(self.janela_principal, text="Filtro do Capítulo:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.filtro_capitulo_txt = ttk.Entry(self.janela_principal)
        self.filtro_capitulo_txt.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['filtro_capitulo_txt'] = self.filtro_capitulo_txt
        linha += 1

        # Combobox de arquivos
        ttk.Label(self.janela_principal, text="Capítulo:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.arquivo_cb = ttk.Combobox(self.janela_principal, takefocus=False, state="readonly")
        self.arquivo_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['arquivo_cb'] = self.arquivo_cb
        linha += 1

        # Combobox de versículos
        ttk.Label(self.janela_principal, text="Versículo:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.versiculo_cb = ttk.Combobox(self.janela_principal, takefocus=False, state="readonly")
        self.versiculo_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['versiculo_cb'] = self.versiculo_cb
        linha += 1

        # Botão de abrir
        self.abrir_biblia_btn = ttk.Button(self.janela_principal, text="Abrir Arquivo")
        self.abrir_biblia_btn.grid(row=linha, column=0, columnspan=2, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['abrir_biblia_btn'] = self.abrir_biblia_btn
        linha += 1

        # Separador
        ttk.Separator(self.janela_principal, orient="horizontal").grid(row=linha, columnspan=3, sticky="ew", padx=espacox, pady=espacoy)
        linha += 1

        # Fim da Bíblia Sagrada layout #
        # Harpa Cristã Layout #
        ttk.Label(self.janela_principal, text="Harpa Cristã").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        linha += 1

        ttk.Separator(self.janela_principal, orient="horizontal").grid(row=linha, columnspan=3, sticky="ew", padx=espacox, pady=espacoy)
        linha += 1

        # Campo de filtro
        ttk.Label(self.janela_principal, text="Filtro do Hino:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.filtro_harpa_txt = ttk.Entry(self.janela_principal)
        self.filtro_harpa_txt.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['filtro_harpa_txt'] = self.filtro_harpa_txt
        linha += 1

        # Combobox de arquivos
        ttk.Label(self.janela_principal, text="Hino:").grid(row=linha, column=0, padx=espacox, pady=espacoy, sticky="w")
        self.arquivo_harpa_cb = ttk.Combobox(self.janela_principal, takefocus=False, state="readonly")
        self.arquivo_harpa_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['arquivo_harpa_cb'] = self.arquivo_harpa_cb
        linha += 1

        # Botão de abrir
        self.abrir_harpa_btn = ttk.Button(self.janela_principal, text="Abrir Arquivo")
        self.abrir_harpa_btn.grid(row=linha, column=0, columnspan=2, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['abrir_harpa_btn'] = self.abrir_harpa_btn
        linha += 1

        # Linha vertical
        ttk.Separator(self.janela_principal, orient="vertical").grid(row=0, column=2, rowspan=linha, sticky="ns", padx=espacox, pady=espacoy)

        # --- Painel lateral direito --- Área de busca ---
        linha_lateral = 0
        ttk.Label(self.janela_principal, text="Busca").grid(row=linha_lateral, column=3, padx=espacox, pady=espacoy, sticky="w")
        linha_lateral += 2

        # Combobox de pasta
        ttk.Label(self.janela_principal, text="Pasta de busca:").grid(row=linha_lateral, column=3, padx=espacox, pady=espacoy, sticky="w")
        self.buscar_texto_cb = ttk.Combobox(self.janela_principal, takefocus=False, state="readonly")
        self.buscar_texto_cb.grid(row=linha_lateral, column=4, padx=espacox, pady=espacoy, sticky="ew")
        self.buscar_texto_cb["values"] = ["Bíblia", "Harpa"]
        self.buscar_texto_cb.current(0)
        self.controles['buscar_texto_cb'] = self.buscar_texto_cb
        linha_lateral += 1

        ttk.Label(self.janela_principal, text="Buscar:").grid(row=linha_lateral, column=3, padx=espacox, pady=espacoy, sticky="w")
        self.buscar_texto_txt = ttk.Entry(self.janela_principal, width=50)
        self.buscar_texto_txt.grid(row=linha_lateral, column=4, padx=espacox, pady=espacoy, sticky="we")
        self.controles['buscar_texto_txt'] = self.buscar_texto_txt
        linha_lateral += 1

        # Botão de buscar
        self.buscar_texto_btn = ttk.Button(self.janela_principal, text="Buscar")
        self.buscar_texto_btn.grid(row=linha_lateral, column=3, columnspan=2, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['buscar_texto_btn'] = self.buscar_texto_btn
        linha_lateral += 1

        # Área de texto, resultado da busca
        # 1. Cria a barra de rolagem
        self.scrollbar_lateral = ttk.Scrollbar(self.janela_principal)
        self.scrollbar_fundo = ttk.Scrollbar(self.janela_principal, orient="horizontal")

        self.scrollbar_lateral.grid(row=linha_lateral, rowspan=10, column=4, sticky="ens", pady=(espacoy, 20), padx=(0, espacox))
        self.scrollbar_fundo.grid(row=13, column=3, columnspan=2, sticky="ews", padx=(espacox, 20), pady=(0, espacoy))

        self.text_area = tk.Text(self.janela_principal, width=10, height=10, wrap="none")
        self.text_area.grid(row=linha_lateral, rowspan=10, column=3, columnspan=2, padx=(espacox, 20), pady=(espacoy, 20), sticky="ewns")

        # 3. Vincula os dois componentes
        self.text_area.config(yscrollcommand=self.scrollbar_lateral.set)
        self.text_area.config(xscrollcommand=self.scrollbar_fundo.set)
        self.scrollbar_lateral.config(command=self.text_area.yview)
        self.scrollbar_fundo.config(command=self.text_area.xview)
        self.controles['text_area'] = self.text_area

    def _criar_barra_menu(self):
        # Criar barra de menu
        self.barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)
        # Menu Ajuda
        self.menu_ajuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.controles['menu_ajuda'] = self.menu_ajuda