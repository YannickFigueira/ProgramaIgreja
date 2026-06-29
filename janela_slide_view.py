import platform
import tkinter as tk
from tkinter import ttk

from tkinterweb import HtmlFrame


class JanelaSlideView:
    def __init__(self, janela_slide, second):
        self.janela_slide_view = tk.Toplevel(janela_slide, background="black")
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
        self.frame_html.pack(expand=True, fill="both")
        self.frame_html.propagate(False)  # impede que o frame se ajuste ao conteúdo
        self.controles['frame_html'] = self.frame_html

        canvas = tk.Canvas(self.janela_slide_view, width=100, height=100)
        canvas.pack(anchor="se", side="bottom", ipadx=40, ipady=40)

        # Carregue sua imagem aqui (ex: formato GIF ou PNG)
        # bg_image = tk.PhotoImage(file="seu_fundo.png")
        # canvas.create_image(0, 0, image=bg_image, anchor="nw")

        # Desenhando o texto direto no Canvas (ele fica com fundo transparente nativo)
        canvas.create_text(30, 25, text="FIM", fill="black", font=("Arial", 25))

        #self.lbl_fim = ttk.Label(self.frame_html, text="FIM", background="white", foreground="black", font=("Arial", 20, "bold"))
        #self.lbl_fim.pack(anchor="se", side="bottom", ipadx=40, ipady=40)
        