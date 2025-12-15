import tkinter as tk
from screeninfo import get_monitors

def iniciar_slide(janela, texto):

    # identificar resolução
    def identificar_proporcao(larguraw, alturah):
        proporcao = larguraw / alturah
        if abs(proporcao - 4 / 3) < 0.05:
            return 25
        elif abs(proporcao - 16 / 9) < 0.05:
            return 21
        else:
            return 25

    # Janela principal
    monitors = get_monitors()
    first = monitors[0]

    janela_slide = tk.Toplevel(janela)
    janela_slide.title("Slide")
    janela_slide.geometry(f"{first.width}x{first.height}+{first.x}+{first.y}")

    # Cria o label

    largura = first.width / 2
    altura = first.height / 2

    # label
    espace_largura = int(largura / 2 / 5)
    espacea_altura = 10

    frame_pricipal = tk.Frame(janela_slide, width=largura, height=altura)
    frame_pricipal.grid(row=0, column=0, padx=espace_largura, pady=espacea_altura)
    frame_pricipal.propagate(False)  # impede que o frame se ajuste ao conteúdo

    frame_preview = tk.Frame(janela_slide, width=largura / 2, height=altura / 2)
    frame_preview.grid(row=0, column=1, padx=espace_largura, pady=espacea_altura, sticky="n")
    frame_preview.propagate(False)

    tamanho_letra = int(altura / identificar_proporcao(first.width, first.height))

    lbl_slide_visual = tk.Label(frame_pricipal, text=texto[1], bg="black", fg="white", font=("Arial", tamanho_letra, "bold"))
    lbl_slide_visual.pack(fill="both", expand=True)

    lbl_slide_preview = tk.Label(frame_preview, text=texto[2], bg="black", fg="white", font=("Arial", int(tamanho_letra / 2), "bold"))
    lbl_slide_preview.pack(fill="both", expand=True)

    # Segunda tela
    # Segunda janela
    def abrir_janela_harpa():
        global label

        # Exemplo: pegar segunda tela
        second = monitors[1]

        janela_nova = tk.Toplevel(janela_slide)
        janela_nova.title("Segunda Tela")
        janela_nova.geometry(f"{second.width}x{second.height}+{second.x}+{second.y}")

        # Maximiza a janela após abrir e remove barra de título
        janela_nova.overrideredirect(True)
        janela_nova.attributes("-fullscreen", True)

        tamanho_letra_slide = int(second.height / identificar_proporcao(second.width, second.height))

        label = tk.Label(
            janela_nova,
            text=texto[1],
            font=("Arial", tamanho_letra_slide, "bold"),
            fg="white",  # cor do texto
            bg="black",  # cor do fundo
            anchor="center"
        )
        label.pack(expand=True, fill="both")
        # Fim da janela slide

    abrir_janela_harpa()

    index = 1

    def atualizar_texto(valor, event=None):
        nonlocal index

        if valor == 0:
            index = (index + 1) % len(texto)  # avança e volta ao início
        else:
            index = (index - 1) % len(texto)

        label.config(text=texto[index])
        lbl_slide_visual.config(text=texto[index])
        if (index + 1) < len(texto):
            lbl_slide_preview.config(text=texto[index + 1])
        else:
            lbl_slide_preview.config(text="")

        if index == 0:
            fechar()

    # Função para fechar ao precionar ESC
    def fechar(event=None):
        janela_slide.destroy()

    # Bind somente nesta janela (evitar bind_all)
    janela_slide.bind("<Escape>", fechar)
    janela_slide.protocol("WM_DELETE_WINDOW", fechar)
    janela_slide.bind("<Right>", lambda e: atualizar_texto(0, e))
    janela_slide.bind("<Left>", lambda e: atualizar_texto(1, e))

    janela_slide.mainloop()
