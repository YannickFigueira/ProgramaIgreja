import tkinter as tk

import estilo


class JanelaPrincipal:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(False, False)

        self.nome_janela = "novo-programa"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Variáveis ---

        # --- Controles ---
        self.controles['janela_principal'] = self.janela_principal

    def _criar_barra_menu(self):
        pass