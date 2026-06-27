import tkinter as tk

from screeninfo import get_monitors

import estilo


class JanelaSlide:
    def __init__(self, janela_principal):
        self.janela_slide = tk.Toplevel(janela_principal)
        self.janela_slide.title("Slide")

        self.nome_janela = "janela-slide"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Variáveis ---
        # --- Inicialização ---
        # Identifica a quantidade de monitores
        monitors = get_monitors()

        if len(monitors) == 2:
            second = monitors[1]
        else:
            second = monitors[0]
        first = monitors[0]

        # Cria o label
        medida_letra = 16

        largura = first.width / 2
        altura = first.height / 2

        borda_texto = int(largura * 0.1)
        largura_texto = largura

        # label
        espace_largura = int(largura / 2 / 5)
        espace_altura = 10

        # --- Controles ---
        self.controles['janela_slide'] = self.janela_slide
        self.janela_slide.rowconfigure(2, weight=1)
        self.janela_slide.configure(bg=estilo.FUNDO_COR)  # SeaGreen
        self.janela_slide.attributes("-fullscreen", True)

        self.lbl_slide_atual = tk.Label(self.janela_slide)
        self.lbl_slide_atual.grid(row=0, column=0)
        self.controles['lbl_slide_atual'] = self.lbl_slide_atual

    def _criar_barra_menu(self):
        pass