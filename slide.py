import tkinter as tk

#from pkg_resources import non_empty_lines
#from tkinter import ttk
from screeninfo import get_monitors
#from tkinter import messagebox
#import  os

def iniciar_slide(janela, texto):

    # identificar resolução
    def identificar_proporcao(larguraw, alturah):
        proporcao = larguraw / alturah
        if abs(proporcao - 4 / 3) < 0.05:
            return 19
        elif abs(proporcao - 16 / 9) < 0.05:
            return 15
        else:
            return 19

    # Janela principal
    monitors = get_monitors()
    first = monitors[0]

    janela_slide = tk.Toplevel(janela)
    janela_slide.title("Slide")
    #janela_slide.geometry("300x200")  # tamanho da janela (opcional)
    janela_slide.geometry(f"{first.width}x{first.height}+{first.x}+{first.y}")
    #janela_slide.geometry(f"{1366}x{768}+{first.x}+{first.y}")

    #janela.selecionar_slide("inicial")

    # Cria o label

    largura = first.width / 2
    #largura = 1366 / 2
    altura = first.height / 2
    #altura = 768 / 2

    """lbl_slide_visual = tk.Label(
        janela_slide,
        text=texto,
        bg="black",  # fundo preto
        fg="white"  # letras brancas
    )"""

    #ttk.Label(janela_slide, text=texto, bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    #ttk.Separator(janela_slide, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    # Posiciona o label com tamanho fixo de 100x100 pixels


    #lbl_slide_visual.config(width=largura, height=altura)
    #lbl_slide_visual.grid(row=0, column=0, padx=5, pady=5)
    #lbl_slide_visual.place(x=50, y=50, width=largura, height=altura)

    # label
    #print(largura, "Inicial")
    espace_largura = int(largura / 2 / 5)
    #print(espace_largura)
    espacea_altura = 10

    frame_pricipal = tk.Frame(janela_slide, width=largura, height=altura)
    frame_pricipal.grid(row=0, column=0, padx=espace_largura, pady=espacea_altura)
    frame_pricipal.propagate(False)  # impede que o frame se ajuste ao conteúdo

    frame_preview = tk.Frame(janela_slide, width=largura / 2, height=altura / 2)
    frame_preview.grid(row=0, column=1, padx=espace_largura, pady=espacea_altura, sticky="n")
    #frame_preview.place(x=largura + 5, y=5, anchor="n")
    frame_preview.propagate(False)

    #print(altura)
    #qtd_quebras = texto[1].count("\n") + 1
    #print(qtd_quebras)  # saída: 3
    tamanho_letra = int(altura / identificar_proporcao(first.width, first.height))

    lbl_slide_visual = tk.Label(frame_pricipal, text=texto[1], bg="black", fg="white", font=("Arial", tamanho_letra, "bold"))
    lbl_slide_visual.pack(fill="both", expand=True)

    lbl_slide_preview = tk.Label(frame_preview, text=texto[2], bg="black", fg="white", font=("Arial", int(tamanho_letra / 2), "bold"))
    lbl_slide_preview.pack(fill="both", expand=True)
    #lbl_slide_preview.place(relx=0, rely=0, anchor="n")

    # Segunda tela
    # Segunda janela
    def abrir_janela_harpa():
        global label
        #titulo = int(self.filtro_harpa_txt.get()) - 1
        #print(titulo)
        #monitors = get_monitors()

        # Exemplo: pegar segunda tela
        second = monitors[1]

        janela_nova = tk.Toplevel(janela_slide)
        janela_nova.title("Segunda Tela")
        janela_nova.geometry(f"{second.width}x{second.height}+{second.x}+{second.y}")

        #print(identificar_proporcao(second.width, second.height))

        # Maximiza a janela após abrir e remove barra de título
        janela_nova.overrideredirect(True)
        janela_nova.attributes("-fullscreen", True)

        tamanho_letra_slide = int(second.height / identificar_proporcao(second.width, second.height))

        label = tk.Label(
            janela_nova,
            # text="Deus prometeu com certeza\nChuvas de graça mandar\nEle nos dá fortaleza\nE ricas bênçãos sem par",
            text=texto[1],
            font=("Arial", tamanho_letra_slide, "bold"),
            fg="white",  # cor do texto
            bg="black",  # cor do fundo
            anchor="center"
        )
        label.pack(expand=True, fill="both")

        #atualizar_texto()

        #label.bind("<Right>", atualizar_texto)
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
        # janela_slide.after(2000, atualizar_texto)  # chama de novo em 2 segundos

    #label.bind("<Right>", atualizar_texto)

    # Função para fechar ao precionar ESC
    def fechar(event=None):
        janela_slide.destroy()

    # Bind somente nesta janela (evitar bind_all)
    janela_slide.bind("<Escape>", fechar)
    janela_slide.protocol("WM_DELETE_WINDOW", fechar)
    #janela_slide.bind("<Right>", atualizar_texto(0))
    janela_slide.bind("<Right>", lambda e: atualizar_texto(0, e))
    janela_slide.bind("<Left>", lambda e: atualizar_texto(1, e))

    #self.abrir_harpa_btn.bind("<Key>",
     #                         lambda e: self.acao_enter_harpa(e) if e.keysym in ("Return", "KP_Enter") else None)

    #print(identificar_proporcao(largura, altura))
    #print("Próximo")

    janela_slide.mainloop()
