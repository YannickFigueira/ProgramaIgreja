import math
import os
import shutil
import sys
import tkinter as tk
import unicodedata
from datetime import datetime
from tkinter import messagebox, filedialog

from screeninfo import get_monitors

import dados, estilo, verificarversao
from arquivo_log import ler_pasta_log, abrir_logs, gerar_arquivo_log, registrar_log, abrir_pasta
from janela_logs import JanelaLogs

from janela_slide import JanelaSlide
from janela_slide_view import JanelaSlideView
from janela_musica import JanelaMusica
from janela_slide_view_lirics import JanelaSlideViewLirics

# Variáveis globais
janela_logs_aberta = False

# --- Comandos do Menu da Janela Principal ---
def visitar_site():
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
                                            f"Deseja visitar a página\n"
                                            f"Desenvolvedor YannickFigueira\n"
                                            f"chronostimeinchain@gmail.com")
    if resposta:
        verificarversao.webbrowser.open(pagina)

# --- Comandos gerais ---
def justificar_texto(texto_slide_view, tamanho_letra_slide):
        # 1. Criamos o Frame HTML
        # frame_html = HtmlFrame(janela_nova)

        # 2. Seu texto com HTML e CSS para justificar em ambos os lados e centralizar
        largura_slide = "91%"
        tamanho_fonte = f"{tamanho_letra_slide}px"

        codigo_html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <body style="background-color: black; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="
                color: white; 
                font-family: Arial, sans-serif; 
                font-size: {tamanho_fonte}; 
                font-weight: bold; 
                /*text-align: justify; /* JUSTIFICA AMBOS OS LADOS */
                text-align: center;
                margin: auto;
                padding-top: 60px;
                max-width: {largura_slide};
                width: 100%;
                line-height: 1.1;
            ">
                {texto_slide_view.replace('\n', '<br>').upper()}

            </div>
        </body>
        </html>
        """

        return codigo_html

def identificar_proporcao(width, height):
    relacao = width / height
    tela16_9 = int(height *.086)
    tela4_3 = int(height *.074)
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

def identificar_monitor():
    # Identifica a quantidade de monitores
    monitors = get_monitors()

    first = None

    for m in monitors:
        # 1. Tenta obter o atributo is_primary com segurança
        is_primary = getattr(m, 'is_primary', False)

        # 2. Se não existir, verifica se a posição é a origem (0, 0)
        if is_primary or (m.x == 0 and m.y == 0):
            first = m
            break

    # Fallback caso nada seja identificado
    if not first and monitors:
        first = monitors[0]

    # Identifica o monitor secundário
    #second = None
    if len(monitors) > 1:
        outros = [m for m in monitors if m != first]
        second = outros[0] if outros else monitors[1]
    else:
        second = first

    return first, second

def remover_acentos(filtro_texto):
    """Remove acentos e caracteres especiais do texto."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', filtro_texto)
        if unicodedata.category(c) != 'Mn'
    )


class Funcoes:
    def __init__(self, view):
        self.view = view
        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "janela-slide":
                self._vincular_janela_slide()
            elif view.nome_janela == "janela-slide-view":
                self._vincular_janela_slide_view()
            elif view.nome_janela == "janela-musica":
                self._vincular_janela_musica()
            elif view.nome_janela == "janela-slide-lirics":
                self._vincular_janela_slide_view_lirics()
            elif view.nome_janela == "logs":
                self._vincular_logs()

    def _vincular_janela_principal(self):
        # --- Inicialização ---
        # Só executa a lógica do Mutex se estiver rodando no Windows
        if os.name == 'nt':
            # noinspection PyBroadException
            try:
                import ctypes
                # Cria o Mutex único para o Inno Setup detectar
                # noinspection PyUnresolvedReferences
                mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MeuProgramaIgrejaMutexUnico")
                # 183 é o código para ERROR_ALREADY_EXISTS (programa já aberto)
                # noinspection PyUnresolvedReferences
                if ctypes.windll.kernel32.GetLastError() == 183:
                    sys.exit(0)
            except AttributeError:
                # Prevenção caso o ambiente mude abruptamente
                pass
            except Exception:
                pass

        self.atualizar_pastas_biblia()
        self.atualizar_versiculos()
        self.carregar_arquivos_harpa()

        # --- Controles da Janela Principal ---
        self.view.controles['filtro_livro_txt'].bind("<KeyRelease>", self.atualizar_pastas_biblia)
        self.view.controles['pastas_cb'].bind("<<ComboboxSelected>>", self.atualizar_arquivos_biblia)
        self.view.controles['filtro_capitulo_txt'].bind("<KeyRelease>", self.atualizar_arquivos_biblia)
        self.view.controles['arquivo_cb'].bind("<<ComboboxSelected>>", self.atualizar_versiculos)
        self.view.controles['abrir_biblia_btn'].configure(command=lambda: self.abrir_janela_slide("biblia", self.view.controles['janela_principal']))
        # Captura especificamente o Enter
        self.view.controles['filtro_capitulo_txt'].bind("<Key>", lambda e: self.acao_enter(e, "biblia", self.view.controles['janela_principal']))
        self.view.controles['abrir_biblia_btn'].bind("<Key>", lambda e: self.acao_enter(e, "biblia", self.view.controles['janela_principal']))
        # Captura qualquer tecla liberada
        self.view.controles['filtro_harpa_txt'].bind("<KeyRelease>", self.filtrar_lista_harpa)
        self.view.controles['abrir_harpa_btn'].configure(command=lambda: self.abrir_janela_slide("harpa", self.view.controles['janela_principal']))
        #self.view.controles['abrir_harpa_btn'].configure(
        #    command=lambda: self.abrir_slide_lirics())
        # Captura especificamente o Enter
        self.view.controles['filtro_harpa_txt'].bind("<Key>", lambda e: self.acao_enter(e, "harpa", self.view.controles['janela_principal']))
        self.view.controles['abrir_harpa_btn'].bind("<Key>", lambda e: self.acao_enter(e, "harpa", self.view.controles['janela_principal']))
        #self.view.controles['abrir_harpa_btn'].bind("<Key>", lambda e: self.abrir_slide_lirics())
        self.view.controles['buscar_texto_btn'].configure(command=lambda: self.localizar_arquivo())
        self.view.controles['buscar_texto_txt'].bind("<Key>", lambda e: self.acao_enter(e, "localizar", self.view.controles['janela_principal']))

        # --- Menu da Janela Principal ---
        self.view.controles['menu_arquivo'].add_command(label="Músicas",
                                                        command=lambda: self.abrir_janela_musica())
        self.view.controles['menu_arquivo'].add_command(label="Logs",
                                                        command=lambda: self.abrir_janela_logs())
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                    command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão",
                                    command=lambda: abrir_logs(self.view))
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                                    command=lambda: visitar_site())
        self.view.controles['menu_ajuda'].add_command(label="Sair", command=self.view.controles['janela_principal'].quit)

    def _vincular_janela_slide(self):
        # Bind somente nesta janela (evitar bind_all)
        self.view.controles['janela_slide'].bind("<Escape>",lambda _: self.fechar('janela_slide'))
        self.view.controles['janela_slide'].protocol("WM_DELETE_WINDOW", lambda: self.fechar('janela_slide'))

    def _vincular_janela_slide_view(self):
        pass

    def _vincular_janela_slide_view_lirics(self):
        pass

    def _vincular_janela_musica(self):
        # --- Inicialização ---
        if os.listdir(estilo.musicas_dir):
            self.carregar_arquivos_musicas()
        # --- Menu da janela musicas ---
        self.view.controles['menu_arquivo'].add_command(label="Adicionar Música",
                                                        command=lambda: self.selecionar_arquivo(self.view.controles['janela_musica']))
        self.view.controles['menu_arquivo'].add_command(label="Abrir pasta das músicas",
                                                        command=lambda: abrir_pasta(self.view))
        # Captura qualquer tecla
        self.view.controles['filtro_musica_txt'].bind("<KeyRelease>", self.filtrar_lista_musicas)
        self.view.controles['abrir_musica_btn'].configure(command=lambda: self.abrir_janela_slide("musica", self.view.controles['janela_musica']))


    def _vincular_logs(self):
        # --- Inicialização da janela logs ---
        arquivos_log = ler_pasta_log()
        texto_log = "\n".join([f"{item}" for item in arquivos_log])

        # --- Controles da Janlea Logs ---
        self.view.controles['janela_logs'].protocol("WM_DELETE_WINDOW",
                                                         lambda: self.fechar_janelas('janela_logs'))

        self.view.controles['lbl_logs'].configure(text=texto_log)
        # 1. Atualiza as opções do ComboBox
        self.view.controles['cmb_selecao'].configure(values=arquivos_log)

        # 2. Define o valor selecionado usando o funcao .set()
        if arquivos_log:
            self.view.controles['cmb_selecao'].set(arquivos_log[0])
        self.view.controles['btn_abrir_logs'].configure(command=lambda: abrir_logs(self.view))

    # --- Inicialização das janelas ---
    # --- Iniciar janela slide ---
    def abrir_janela_slide(self, slide, janela):
        global inicio, total, texto, verso

        match slide:
            case "biblia":
                pasta_selecionada = self.view.controles['pastas_cb'].get()
                arquivo_selecionado = self.view.controles['arquivo_cb'].get()
                pasta_caminho_new = os.path.join(dados.biblia_dir, pasta_selecionada, arquivo_selecionado)
                texto = dados.carregar_texto(pasta_caminho_new + ".txt", dados.biblia_dir)
                # Limpa os campos de filtro
                self.view.controles['filtro_livro_txt'].delete(0, tk.END)
                self.view.controles['filtro_capitulo_txt'].delete(0, tk.END)
                # Transfere o foco para o campo de filtro de pastas
                self.view.controles['filtro_livro_txt'].focus_set()
                inicio = self.view.controles['versiculo_cb'].cget("values").index(
                    self.view.controles['versiculo_cb'].get()) + 1
                print(inicio)
                total = len(texto)
                verso = self.view.controles['versiculo_cb'].cget("values").index(
                    self.view.controles['versiculo_cb'].get())
            case "harpa":
                if self.view.controles['filtro_harpa_txt'].get() != "":
                    self.view.controles['filtro_harpa_txt'].delete(0, tk.END)  # Limpa o campo do texto
                    arquivo = self.view.controles['arquivo_harpa_cb'].get()

                    if arquivo:
                        caminho = os.path.join(dados.harpa_dir, arquivo)
                        texto = dados.carregar_texto(caminho + ".txt", dados.harpa_dir)
                        self.carregar_arquivos_harpa()
                        inicio = 1
                        total = len(texto) - 1
                        verso = 1
                    else:
                        messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")
                        return
                else:
                    messagebox.showwarning("Aviso", "Digite o número ou nome do hino!")
                    return
            case "musica":
                self.view.controles['filtro_musica_txt'].delete(0, tk.END)
                arquivo = self.view.controles['musica_cb'].get()

                if arquivo:
                    caminho = os.path.join(estilo.musicas_dir, arquivo)
                    texto = dados.carregar_texto(caminho + ".txt", estilo.musicas_dir)
                    self.carregar_arquivos_musicas()
                    inicio = 1
                    total = len(texto) - 1
                    verso = 1
                else:
                    messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")

        # 1. Cria a parte visual
        visual = JanelaSlide(janela)

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        # --- Inicialização ---
        # Identifica a quantidade de monitores
        first, second = identificar_monitor()

        logica.view.controles['janela_slide'].bind("<Right>", lambda _: atualizar_texto(0))
        logica.view.controles['janela_slide'].bind("<Left>", lambda _: atualizar_texto(1))
        logica.atualizar_hora()

        # Cria o label
        medida_letra = 16

        largura = first.width / 2
        altura = first.height / 2

        borda_texto = int(largura * 0.1)
        largura_texto = largura

        # label
        espace_largura = int(largura / 2 / 5)
        espace_altura = 10
        tamanho_letra = int(altura / medida_letra)

        texto_verificado = ""
        if not len(texto) == verso + 1:
            texto_verificado = texto[verso + 1]

        # Funções da janela slide
        logica.view.controles['lbl_slide_atual'].config(
            text=f"{inicio} / {total}", bg=estilo.FUNDO_COR, font=("Arial", 20, "bold"))
        # --- Configuração dos Frames ---
        logica.view.controles['frame_principal'].config(width=largura, height=altura)
        logica.view.controles['frame_principal'].grid(padx=espace_largura, pady=espace_altura)
        logica.view.controles['frame_preview'].config(width=largura / 2, height=altura / 2)
        logica.view.controles['frame_preview'].grid(padx=espace_largura, pady=espace_altura, sticky="n")
        logica.view.controles['frame_rodape'].config(width=largura, height=altura)

        # --- Controles ---
        logica.view.controles['lbl_slide_visual'].config(
            text=texto[verso], bg="black", fg="white", font=("Arial", tamanho_letra, "bold"),
            wraplength=largura_texto - borda_texto)
        logica.view.controles['lbl_slide_preview'].config(
            text=texto_verificado, bg="black", fg="white", font=("Arial", int(tamanho_letra / 2), "bold"),
            wraplength=largura_texto / 2 - borda_texto)

        tamanho_letra_slide = identificar_proporcao(second.width, second.height)

        match slide:
            case "biblia":
                logica.abrir_janela_slide_view(second, tamanho_letra_slide)
            case _:
                view = logica.abrir_slide_lirics(f"{texto[0].replace("\n", " - ")} - 1 / {total} ", texto[1])

        index = verso
        index_contador = inicio
        encerrar = inicio

        def atualizar_texto(valor_atualizar):
            nonlocal index, encerrar, index_contador

            if valor_atualizar == 0:
                index = (index + 1) % len(texto)  # avança e volta ao início
                encerrar += 1
                index_contador += 1
            else:
                index = (index - 1) % len(texto)
                encerrar -= 1
                index_contador -= 1

            logica.view.controles['lbl_slide_atual'].config(text=f"{index_contador} / {total}")
            # label.config(text=texto[index])

            logica.view.controles['lbl_slide_visual'].config(text=texto[index])

            if (index + 1) < len(texto):
                logica.view.controles['lbl_slide_preview'].config(text=texto[index + 1])
            else:
                logica.view.controles['lbl_slide_preview'].config(text="")

            match slide:
                case "biblia":
                    codigo_html = justificar_texto(texto[index], tamanho_letra_slide)
                    frame_html.load_html(codigo_html)

                    if encerrar < 1 or encerrar > len(texto):
                        logica.fechar('janela_slide')
                case _:
                    view.controles['lbl_titulo'].config(
                        text=f"{texto[0].replace("\n", " - ")} - {index} / {total} ")
                    view.controles['lbl_texto'].config(text=texto[index].upper())

                    if encerrar < 1 or encerrar > (len(texto) - 1):
                        logica.fechar('janela_slide')

    # --- Abrir janela slide view ---
    def abrir_janela_slide_view(self, second, tamanho_letra_slide):
        # --- Variável ---
        global frame_html

        # 1. Cria a parte visual
        visual_slide = JanelaSlideView(self.view.controles['janela_slide'], second)

        # 2. Cria a lógica e passa a visão para ela controlar
        logica_slide = Funcoes(visual_slide)

        codigo_html = justificar_texto(texto[verso], tamanho_letra_slide)
        logica_slide.view.controles['frame_html'].load_html(codigo_html)
        frame_html = logica_slide.view.controles['frame_html']

    # --- Abrir janela slide lirics ---
    def abrir_slide_lirics(self, titulo, texto_slide):
        # --- Inicialização ---
        first, second = identificar_monitor()

        largura = second.width / 2

        borda_texto = int(largura * 0.1)

        # 1. Cria a parte visual
        visual = JanelaSlideViewLirics(self.view.controles['janela_slide'], second)

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        logica.view.controles['lbl_titulo'].config(
            #text="Hino - 250 1/5",
            text=f"{titulo}",
            bg="black",
            fg="white",
            font=("Arial", 20, "bold")
        )
        logica.view.controles['lbl_titulo'].pack(pady=(50,0))

        logica.view.controles['janela_slide_view_lirics'].config(bg="black")
        logica.view.controles['lbl_texto'].config(text=texto_slide.upper())

        logica.view.controles['lbl_texto'].config(
            anchor="n",
            bg="black",
            fg="white",
            font=("Arial", int(second.height * 0.064), "bold"),
            wraplength=second.width - borda_texto)
        logica.view.controles['lbl_texto'].pack(pady=(0,0))

        return logica.view

    # --- Abrir janela música
    def abrir_janela_musica(self):
        # 1. Cria a parte visual
        visual_musica = JanelaMusica(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica_slide = Funcoes(visual_musica)

    # --- Abrir janela de logs ---
    def abrir_janela_logs(self):
        global janela_logs_aberta
        # 1. Cria a parte visual
        visual = JanelaLogs(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        janela_logs_aberta = True
        logica.view.controles['janela_logs'].wait_window()
        janela_logs_aberta = False

    # --- Comandos da Janela Principal ---
    def atualizar_pastas_biblia(self, event=None):
        filtrar_texto = self.view.controles['filtro_livro_txt'].get().lower()
        filtrado = [f for f in estilo.TODAS_PASTAS if filtrar_texto in f.lower()]
        self.view.controles['pastas_cb'].configure(values=filtrado)

        if filtrado:
            self.view.controles['pastas_cb'].set(filtrado[0])
            self.atualizar_arquivos_biblia()

    def atualizar_arquivos_biblia(self, event=None):
        selecionar_pasta = self.view.controles['pastas_cb'].get()
        texto_filtrado = self.view.controles['filtro_capitulo_txt'].get().lower()
        pasta_caminho = str(os.path.join(dados.biblia_dir, selecionar_pasta))

        if os.path.isdir(pasta_caminho):
            arquivos = [f for f in os.listdir(pasta_caminho) if os.path.isfile(os.path.join(pasta_caminho, f))]
            arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
            arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            if texto_filtrado:
                arquivos = [f for f in arquivos if texto_filtrado in f.lower()]
                arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            if arquivos_sem_ext != "":
                self.view.controles['arquivo_cb'].configure(values=arquivos_sem_ext)

            if arquivos:
                self.view.controles['arquivo_cb'].set(arquivos_sem_ext[0])

        self.atualizar_versiculos()

    def atualizar_versiculos(self, event=None):
        caminho = os.path.join(dados.biblia_dir, self.view.controles['pastas_cb'].get(), self.view.controles['arquivo_cb'].get())
        contar = dados.carregar_texto(caminho + ".txt", dados.biblia_dir)

        # Gera "Versículo 1,Versículo 2,Versículo 3..." direto pela quantidade de itens
        versiculo = ",".join([f"Versículo {i}" for i in range(1, len(contar) + 1)])

        self.view.controles['versiculo_cb'].configure(values=versiculo.split(","))
        versiculo_valores = self.view.controles['versiculo_cb'].cget('values')
        self.view.controles['versiculo_cb'].set(versiculo_valores[0])

    def atualizar_hora(self):
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        self.view.controles['label_relogio'].config(text=hora_formatada)
        self.view.controles['janela_slide'].after(1000, self.atualizar_hora)  # chama a função novamente após 1000 ms (1 segundo)

    def fechar(self, nome):
        self.view.controles[nome].destroy()

    def acao_enter(self, event, slide, janela):
        if event.keysym in ("Return", "KP_Enter"):
            if slide == "localizar":
                self.localizar_arquivo()
            else:
                self.abrir_janela_slide(slide, janela)

    def filtrar_lista_harpa(self, event=None):
        texto_harpa = self.view.controles['filtro_harpa_txt'].get().lower()
        filtrados = [f for f in estilo.LISTA_COMPLETA if texto_harpa in f.lower()]
        self.view.controles['arquivo_harpa_cb'].configure(values=filtrados)

        if filtrados:
            self.view.controles['arquivo_harpa_cb'].set(filtrados[0])

    def filtrar_lista_musicas(self, event=None):
        texto_musicas = self.view.controles['filtro_musica_txt'].get().lower()
        filtrados = [f for f in estilo.LISTA_MUSICAS if texto_musicas in f.lower()]
        self.view.controles['musica_cb'].configure(values=filtrados)
        if filtrados:
            self.view.controles['musica_cb'].set(filtrados[0])

    def carregar_arquivos_harpa(self):
        arquivos = os.listdir(dados.harpa_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(dados.harpa_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower()) # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        estilo.LISTA_COMPLETA = arquivos_sem_ext
        self.view.controles['arquivo_harpa_cb'].configure(values=arquivos_sem_ext)

        if arquivos:
            self.view.controles['arquivo_harpa_cb'].set(arquivos_sem_ext[0])

    def selecionar_arquivo(self, janela):
        messagebox.showinfo("Aviso", "Selecione o arquivo de texto .txt", parent=janela)
        arquivo = filedialog.askopenfilename(parent=janela, title="Selecione um arquivo de texto",
                                             filetypes=[("Arquivos de texto", "*.txt"),
                                                        ("Todos os arquivos", "*.*")])
        if arquivo:
            shutil.copy(arquivo, estilo.musicas_dir)
            self.carregar_arquivos_musicas()

    def carregar_arquivos_musicas(self):
        arquivos = os.listdir(estilo.musicas_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(estilo.musicas_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        estilo.LISTA_MUSICAS = arquivos_sem_ext
        self.view.controles['musica_cb'].configure(values=arquivos_sem_ext)
        self.view.controles['musica_cb'].set(arquivos_sem_ext[0])

    def localizar_arquivo(self):
        busca = self.view.controles['buscar_texto_cb'].get()
        if busca == "Bíblia":
            pasta_raiz = dados.biblia_dir
        elif busca == "Harpa":
            pasta_raiz = dados.harpa_dir
        else:
            pasta_raiz = estilo.musicas_dir

        # Normaliza e converte para minúsculas o termo pesquisado
        termo_busca = remover_acentos(self.view.controles['buscar_texto_txt'].get().lower())

        resultado = ""
        for raiz, pastas, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.endswith('.txt'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    try:
                        # Divisão de caminho multiplataforma
                        nome_arquivo = os.path.basename(caminho_completo)

                        with open(caminho_completo, 'r', encoding='utf-8') as f:
                            for numero_linha, linha in enumerate(f, 1):
                                # Normaliza a linha do arquivo para ignorar acentos e maiúsculas
                                linha_normalizada = remover_acentos(linha.lower())

                                if termo_busca in linha_normalizada:
                                    resultado += f" {nome_arquivo} -> Verso {math.ceil(numero_linha / 3)} -> {linha.strip()}\n"
                    except Exception as e:
                        caminho_erro = gerar_arquivo_log()
                        registrar_log(caminho_erro, f"Erro ao ler o arquivo {caminho_completo}: {e}")

        self.view.controles['text_area'].delete("1.0", tk.END)
        self.view.controles['text_area'].insert("1.0", resultado.replace(".txt", ""))

    def fechar_janelas(self, janela):
        global janela_logs_aberta

        match janela:
            case 'janela_principal':
                if janela_logs_aberta:
                    return
        try:
            self.view.controles[f'{janela}'].destroy()
        except Exception:
            pass

    def abrir_pasta_musica(self):
        pass