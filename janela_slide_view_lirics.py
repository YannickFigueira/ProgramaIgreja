import platform
import tkinter as tk

class JanelaSlideViewLirics:
    def __init__(self, janela_slide, second):
        self.janela_slide_view_lirics = tk.Toplevel(janela_slide)
        self.janela_slide_view_lirics.geometry(f"{second.width}x{second.height}+{second.x}+{second.y}")
        self.janela_slide_view_lirics.attributes("-fullscreen", True)

        self.nome_janela = "janela-slide-lirics" # Identificador para o seu controlador
        # Maximiza a janela após abrir e remove barra de título
        if not platform.system() == "Windows":
            self.janela_slide_view_lirics.overrideredirect(True)
        else:
            janela_slide.focus_force()
            self.janela_slide_view_lirics.attributes("-topmost", True) # força ficar na frente

        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Controles ---
        self.controles['janela_slide_view_lirics'] = self.janela_slide_view_lirics

        self.lbl_titulo = tk.Label(self.controles['janela_slide_view_lirics'])
        self.lbl_titulo.pack(side="top", fill="x")
        self.controles['lbl_titulo'] = self.lbl_titulo

        self.lbl_texto = tk.Label(self.janela_slide_view_lirics)
        self.lbl_texto.pack(fill="both", expand=True)
        self.controles['lbl_texto'] = self.lbl_texto
