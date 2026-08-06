import tkinter as tk
from tkinter import ttk


class JanelaMusica:
    def __init__(self, janela_principal):
        self.janela_musica = tk.Toplevel(janela_principal)
        self.janela_musica.title("Músicas Gospel")
        self.janela_musica.resizable(False, False)

        self.nome_janela = "janela-musica"
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
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

        # Combobox de pastas
        ttk.Label(self.janela_musica, text="Música:").grid(row=linha, column=0, padx=espacox, pady=espacoy,
                                                             sticky="w")
        self.pasta_cb = ttk.Combobox(self.janela_musica, takefocus=False, state="readonly")
        self.pasta_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['pasta_cb'] = self.pasta_cb
        linha += 1

        # Botão de abrir
        self.abrir_biblia_btn = ttk.Button(self.janela_musica, text="Iniciar slide")
        self.abrir_biblia_btn.grid(row=linha, column=0, columnspan=2, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['abrir_biblia_btn'] = self.abrir_biblia_btn
        linha += 1

    def _criar_barra_menu(self):
        # Criar barra de menu
        self.barra_menu = tk.Menu(self.janela_musica)
        self.janela_musica.config(menu=self.barra_menu)
        # Menu Arquivos
        self.menu_arquivo =tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.controles['menu_arquivo'] = self.menu_arquivo
