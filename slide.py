import math
import tkinter as tk
import platform

from screeninfo import get_monitors
from datetime import datetime

from tkinterweb import HtmlFrame

import funcionalidades

def iniciar_slide(janela, texto, identificacao, verso):
    texto_verificado = ""
    if identificacao == 0:
        ajuste = 1
        if not len(texto) == (verso + 1):
            texto_verificado = texto[verso + 1]

    else:
        ajuste = 0
        if not len(texto) == (verso + 1):
            texto_verificado = texto[verso + 1]

    # Janela principal
    monitors = get_monitors()

    if len(monitors) == 2:
        second = monitors[1] ## testes original 1
    else:
        second = monitors[0]
    first = monitors[0]

    fundo_cor = "#2E8B57"

    janela_slide = tk.Toplevel(janela)
    janela_slide.title("Slide")
    janela_slide.rowconfigure(2, weight=1)
    janela_slide.configure(bg=fundo_cor) #SeaGreen
    janela_slide.attributes("-fullscreen", True)

    # Cria o label
    medida_letra = 16

    largura = first.width / 2
    altura = first.height / 2

    borda_texto = int(largura * 0.1)
    largura_texto = largura

    # label
    espace_largura = int(largura / 2 / 5)
    espace_altura = 10

    lbl_slide_atual = tk.Label(janela_slide, text=f"{verso + ajuste} / {len(texto) - identificacao}", bg=fundo_cor, font=("Arial", 20, "bold"))
    lbl_slide_atual.grid(row=0, column=0)

    frame_principal = tk.Frame(janela_slide, width=largura, height=altura)
    frame_principal.grid(row=1, column=0, padx=espace_largura, pady=espace_altura)
    frame_principal.propagate(False)  # impede que o frame se ajuste ao conteúdo

    frame_preview = tk.Frame(janela_slide, width=largura / 2, height=altura / 2)
    frame_preview.grid(row=1, column=1, padx=espace_largura, pady=espace_altura, sticky="n")
    frame_preview.propagate(False)

    frame_rodape = tk.Frame(janela_slide, width=largura, height=altura)
    frame_rodape.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="s")

    # Criar o Label para mostrar a hora
    label_relogio = tk.Label(frame_rodape, text="", bg=fundo_cor, font=("Helvetica", 50))
    label_relogio.pack(side="bottom")

    tamanho_letra = int(altura / medida_letra)

    def identificar_proporcao():

        relacao = second.width / second.height

        tela16_9 = int(second.height *.086)
        tela4_3 = int(second.height *.074)

        if abs(relacao - (16 / 9)) < 0.05:
            return tela16_9
        elif abs(relacao - (4 / 3)) < 0.05:
            return tela4_3
        elif abs(relacao - (16 / 10)) < 0.05:
            return tela16_9
        elif relacao > 2.0:
            return tela16_9
        else:
            return tela16_9

    tamanho_letra_slide = identificar_proporcao()

    lbl_slide_visual = tk.Label(frame_principal, text=texto[verso], bg="black", fg="white", font=("Arial", tamanho_letra, "bold"),
                                wraplength=largura_texto - borda_texto)
    lbl_slide_visual.pack(fill="both", expand=True)

    lbl_slide_preview = tk.Label(frame_preview, text=texto_verificado, bg="black", fg="white", font=("Arial", int(tamanho_letra / 2),
                                                                                                     "bold"), wraplength=largura_texto / 2 - borda_texto)
    lbl_slide_preview.pack(fill="both", expand=True)

    # Segunda tela
    # Segunda janela
    def abrir_janela_slide():
        global label

        # Exemplo: pegar segunda tela

        #largura_texto_slide = int(second.width * 0.91)

        janela_nova = tk.Toplevel(janela_slide)
        janela_nova.title("Segunda Tela")
        janela_nova.geometry(f"{second.width}x{second.height}+{second.x}+{second.y}")

        # Maximiza a janela após abrir e remove barra de título
        if not platform.system() == "Windows":
            janela_nova.overrideredirect(True)
        else:
            janela_slide.focus_force()
            janela_nova.attributes("-topmost", True)  # força ficar na frente

        janela_nova.attributes("-fullscreen", True)



        frame_html = HtmlFrame(janela_nova)
        codigo_html = funcionalidades.justificar_texto(texto[verso], tamanho_letra_slide)
        frame_html.load_html(codigo_html)
        #frame_html.grid(row=0, column=0, pady=30)
        frame_html.pack(expand=True, fill="both")
        frame_html.propagate(False)  # impede que o frame se ajuste ao conteúdo
        '''
        label = tk.Label(
            janela_nova,
            text=texto[verso],
            font=("Arial", tamanho_letra_slide, "bold"),
            fg="white",  # cor do texto
            bg="black",  # cor do fundo
            #anchor="center",
            justify="center",
            wraplength=largura_texto_slide
        )
        label.pack(expand=True, fill="both")
        # Fim da janela slide
        '''

        return frame_html

    frame_html = abrir_janela_slide()

    index = verso
    if identificacao == 0:
        ajuste = 1
    else:
        ajuste = 0

    def atualizar_texto(valor, event=None):
        nonlocal index

        if valor == 0:
            index = (index + 1) % len(texto)  # avança e volta ao início
        else:
            index = (index - 1) % len(texto)

        lbl_slide_atual.config(text=f"{index + ajuste} / {len(texto) - identificacao}")
        # label.config(text=texto[index])

        codigo_html = funcionalidades.justificar_texto(texto[index], tamanho_letra_slide)
        frame_html.load_html(codigo_html)
        frame_html.pack(expand=True, fill="both")
        frame_html.propagate(False)  # impede que o frame se ajuste ao conteúdo

        lbl_slide_visual.config(text=texto[index])
        if (index + 1) < len(texto):
            lbl_slide_preview.config(text=texto[index + 1])
        else:
            lbl_slide_preview.config(text="")

        print(f"index: {index}")
        print(f"texto: {len(texto)}")
        if index == len(texto) - 1:
            print("FIM")
            fechar()

        if index == 0 and identificacao == 1:
            fechar()

    # Função para fechar ao precionar ESC
    def fechar(event=None):
        janela_slide.destroy()

    def atualizar_hora():
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        label_relogio.config(text=hora_formatada)
        janela_slide.after(1000, atualizar_hora)  # chama a função novamente após 1000 ms (1 segundo)

    atualizar_hora()

    # Bind somente nesta janela (evitar bind_all)
    janela_slide.bind("<Escape>", fechar)
    janela_slide.protocol("WM_DELETE_WINDOW", fechar)
    janela_slide.bind("<Right>", lambda e: atualizar_texto(0, e))
    janela_slide.bind("<Left>", lambda e: atualizar_texto(1, e))

    janela_slide.mainloop()
