import tkinter as tk

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

        # --- Controles ---
        self.controles['janela_slide'] = self.janela_slide
        self.janela_slide.rowconfigure(2, weight=1)
        self.janela_slide.configure(bg=estilo.FUNDO_COR)  # SeaGreen
        self.janela_slide.attributes("-fullscreen", True)

        self.lbl_slide_atual = tk.Label(self.janela_slide)
        self.lbl_slide_atual.grid(row=0, column=0)
        self.controles['lbl_slide_atual'] = self.lbl_slide_atual

        # Frames da janela
        self.frame_principal = tk.Frame(self.janela_slide)
        self.frame_principal.grid(row=1, column=0)
        self.frame_principal.propagate(False)  # impede que o frame se ajuste ao conteúdo
        self.controles['frame_principal'] = self.frame_principal

        self.frame_preview = tk.Frame(self.janela_slide)
        self.frame_preview.grid(row=1, column=1)
        self.frame_preview.propagate(False)
        self.controles['frame_preview'] = self.frame_preview

        self.frame_rodape = tk.Frame(self.janela_slide)
        self.frame_rodape.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="s")
        self.controles['frame_rodape'] = self.frame_rodape

        # Criar o Label para mostrar a hora
        self.label_relogio = tk.Label(self.frame_rodape, text="", bg=estilo.FUNDO_COR, font=("Helvetica", 50))
        self.label_relogio.pack(side="bottom")
        self.controles['label_relogio'] = self.label_relogio

        self.lbl_slide_visual = tk.Label(self.frame_principal)
        self.lbl_slide_visual.pack(fill="both", expand=True)
        self.controles['lbl_slide_visual'] = self.lbl_slide_visual

        self.lbl_slide_preview = tk.Label(self.frame_preview)
        self.lbl_slide_preview.pack(fill="both", expand=True)
        self.controles['lbl_slide_preview'] = self.lbl_slide_preview

    def _criar_barra_menu(self):
        pass