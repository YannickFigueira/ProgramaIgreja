import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class JanelaMusica:
    def __init__(self, janela_principal):
        self.janela_musica = ctk.CTkToplevel(janela_principal)
        self.janela_musica.withdraw()
        self.janela_musica.title("Músicas Gospel")
        self.janela_musica.resizable(False, False)

        self.nome_janela = "janela-musica"
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

        self.janela_musica.update_idletasks()
        self.janela_musica.deiconify()

    def _criar_layout(self):
        linha = 0
        link = 6
        espacox = link
        espacoy = link
        # --- Controles ---
        self.controles['janela_musica'] = self.janela_musica

        # Filtro das músicas
        ctk.CTkLabel(self.janela_musica, text="Filtro da Música:").grid(row=linha, column=0, padx=espacox, pady=espacoy,
                                                                       sticky="w")
        self.filtro_musica_txt = ctk.CTkEntry(self.janela_musica, width=300)
        self.filtro_musica_txt.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.filtro_musica_txt.focus_set()  # Define o foco inicial
        self.controles['filtro_musica_txt'] = self.filtro_musica_txt
        linha += 1

        # Combobox de pastas
        ctk.CTkLabel(self.janela_musica, text="Música:").grid(row=linha, column=0, padx=espacox, pady=espacoy,
                                                             sticky="w")
        self.musica_cb = ctk.CTkOptionMenu(self.janela_musica)
        self.musica_cb.grid(row=linha, column=1, padx=espacox, pady=espacoy, sticky="ew")
        self.musica_cb._canvas.configure(takefocus=False)
        self.controles['musica_cb'] = self.musica_cb
        linha += 1

        # Botão de abrir
        self.abrir_musica_btn = ctk.CTkButton(self.janela_musica, text="Iniciar slide")
        self.abrir_musica_btn.grid(row=linha, column=0, columnspan=2, padx=espacox, pady=espacoy, sticky="ew")
        self.controles['abrir_musica_btn'] = self.abrir_musica_btn
        linha += 1

    def _criar_barra_menu(self):
        # Criar barra de menu
        self.barra_menu = tk.Menu(self.janela_musica)
        self.janela_musica.config(menu=self.barra_menu)
        # Menu Arquivos
        self.menu_arquivo =tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.controles['menu_arquivo'] = self.menu_arquivo
