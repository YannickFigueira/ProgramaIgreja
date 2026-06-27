import tkinter as tk

import estilo


class JanelaSlide:
    def __init__(self, janela_principal):
        self.janela_slide = tk.Toplevel(janela_principal)
        self.janela_slide.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_slide.resizable(False, False)

        self.nome_janela = "janela-slide"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Variáveis ---

        # --- Controles ---
        self.controles['janela_slide'] = self.janela_slide

    def _criar_barra_menu(self):
        pass