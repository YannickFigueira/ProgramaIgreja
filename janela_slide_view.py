import platform
import tkinter as tk

from tkinterweb import HtmlFrame


class JanelaSlideView:
    def __init__(self, janela_slide, second):
        self.janela_slide_view = tk.Toplevel(janela_slide)
        self.janela_slide_view.geometry(f"{second.width}x{second.height}+{second.x}+{second.y}")
        self.janela_slide_view.attributes("-fullscreen", True)

        self.nome_janela = "janela-slide-view"  # Identificador para o seu controlador
        # Maximiza a janela após abrir e remove barra de título
        if not platform.system() == "Windows":
            self.janela_slide_view.overrideredirect(True)
        else:
            janela_slide.focus_force()
            self.janela_slide_view.attributes("-topmost", True)  # força ficar na frente

        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Controles ---
        self.frame_html = HtmlFrame(self.janela_slide_view)
        # frame_html.grid(row=0, column=0, pady=30)
        self.frame_html.pack(expand=True, fill="both")
        self.frame_html.propagate(False)  # impede que o frame se ajuste ao conteúdo
        self.controles['frame_html'] = self.frame_html
        