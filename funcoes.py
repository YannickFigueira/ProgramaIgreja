import logging
import os
import platform
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from screeninfo import get_monitors

import dados, estilo, verificarversao

from janela_slide import JanelaSlide
from janela_slide_view import JanelaSlideView

# --- Registro de erros ---
arquivo_erro = estilo.ARQUIVO_ERRO
home_dir = os.path.expanduser('~')
if platform.system() == 'Linux':
    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/{arquivo_erro}",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

elif platform.system() == 'Windows':
    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename=f"c:/temp/{arquivo_erro}",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")
# --- Inicialização geral ---
# Identifica a quantidade de monitores
monitors = get_monitors()

if len(monitors) == 2:
    second = monitors[1]
else:
    second = monitors[0]
first = monitors[0]

# --- Comandos do Menu da Janela Principal ---
def visitar_site():
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"Programa Igreja {estilo.VERSION}\n"
                                            f"Deseja visitar a página\n"
                                            f"Desenvolvedor YannickFigueira\n"
                                            f"chronostimeinchain@gmail.com")
    if resposta:
        verificarversao.webbrowser.open(pagina)

def abrir_logs():
    home_dir = os.path.expanduser('~')
    if platform.system() == "Windows":
        arquivo = f"C:\\temp\\{estilo.ARQUIVO_ERRO}"
        subprocess.run(["notepad", arquivo])
    elif platform.system() == "Linux":
        arquivo = f"{home_dir}/log/{estilo.ARQUIVO_ERRO}"
        subprocess.run(["xdg-open", arquivo])  # ou "gedit"
    else:
        print("Sistema não suportado")

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
                text-align: justify; /* JUSTIFICA AMBOS OS LADOS */
                margin: auto;
                padding-top: 40px;
                max-width: {largura_slide};
                width: 100%;
                line-height: 1.1;
            ">
                {texto_slide_view.replace('\n', '<br>')}

            </div>
        </body>
        </html>
        """

        return codigo_html

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
        self.view.controles['abrir_biblia_btn'].config(command=lambda: self.abrir_janela_slide(0))
        # Captura especificamente o Enter
        self.view.controles['filtro_capitulo_txt'].bind("<Key>", lambda e: self.acao_enter(e, 0))
        self.view.controles['abrir_biblia_btn'].bind("<Key>", lambda e: self.acao_enter(e, 0))
        # Captura qualquer tecla liberada
        self.view.controles['filtro_harpa_txt'].bind("<KeyRelease>", self.filtrar_lista)
        self.view.controles['abrir_harpa_btn'].config(command=lambda: self.abrir_janela_slide(1))
        # Captura especificamente o Enter
        self.view.controles['filtro_harpa_txt'].bind("<Key>", lambda e: self.acao_enter(e, 1))
        self.view.controles['abrir_harpa_btn'].bind("<Key>", lambda e: self.acao_enter(e, 1))

        # --- Menu da Janela Principal ---
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                    command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão",
                                    command=lambda: abrir_logs())
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                                    command=lambda: visitar_site())
        self.view.controles['menu_ajuda'].add_command(label="Sair", command=self.view.controles['janela_principal'].quit)

    def _vincular_janela_slide(self):
        # Bind somente nesta janela (evitar bind_all)
        self.view.controles['janela_slide'].bind("<Escape>",lambda _: self.fechar('janela_slide'))
        self.view.controles['janela_slide'].protocol("WM_DELETE_WINDOW", lambda: self.fechar('janela_slide'))

    def _vincular_janela_slide_view(self):
        pass

    # --- Comandos da Janela Principal ---

    def atualizar_pastas_biblia(self, event=None):
        filtrar_texto = self.view.controles['filtro_livro_txt'].get().lower()
        filtrado = [f for f in estilo.TODAS_PASTAS if filtrar_texto in f.lower()]
        self.view.controles['pastas_cb']["values"] = filtrado

        if filtrado:
            self.view.controles['pastas_cb'].current(0)
            self.atualizar_arquivos_biblia()


    def atualizar_arquivos_biblia(self, event=None):
        selecionar_pasta = self.view.controles['pastas_cb'].get()
        texto_filtrado = self.view.controles['filtro_capitulo_txt'].get().lower()
        pasta_caminho = os.path.join(dados.biblia_dir, selecionar_pasta)

        if os.path.isdir(pasta_caminho):
            arquivos = [f for f in os.listdir(pasta_caminho) if os.path.isfile(os.path.join(pasta_caminho, f))]
            arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
            arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            if texto_filtrado:
                arquivos = [f for f in arquivos if texto_filtrado in f.lower()]
                arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            if arquivos_sem_ext != "":
                self.view.controles['arquivo_cb']["values"] = arquivos_sem_ext
            else:
                self.view.controles['arquivo_cb']["values"] = arquivos

            if arquivos:
                self.view.controles['arquivo_cb'].current(0)

        self.atualizar_versiculos()

    def atualizar_versiculos(self, event=None):
        caminho = os.path.join(dados.biblia_dir, self.view.controles['pastas_cb'].get(), self.view.controles['arquivo_cb'].get())
        contar = dados.carregar_texto(caminho + ".txt", dados.biblia_dir)
        versiculo = "Versículo 1"
        index = 2

        for contagem in contar:
            if index <= len(contar):
                versiculo = versiculo + ",Versículo " + str(index)
                index += 1

        versiculos = versiculo.split(",")
        self.view.controles['versiculo_cb']["values"] = versiculos
        self.view.controles['versiculo_cb'].current(0)

    def atualizar_hora(self):
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        self.view.controles['label_relogio'].config(text=hora_formatada)
        self.view.controles['janela_slide'].after(1000, self.atualizar_hora)  # chama a função novamente após 1000 ms (1 segundo)

    def fechar(self, nome):
        self.view.controles[nome].destroy()

    def acao_enter(self, event, valor):
        if event.keysym in ("Return", "KP_Enter"):
            match valor:
                case 0:
                    self.abrir_janela_slide(valor)
                case 1:
                    self.abrir_janela_slide(valor)

    def filtrar_lista(self, event=None):
        texto_harpa = self.view.controles['filtro_harpa_txt'].get().lower()
        filtrados = [f for f in estilo.LISTA_COMPLETA if texto_harpa in f.lower()]
        self.view.controles['arquivo_harpa_cb']["values"] = filtrados

        if filtrados:
            self.view.controles['arquivo_harpa_cb'].current(0)

    # --- Iniciar janela slide ---
    def abrir_janela_slide(self, valor):
        global identificacao, verso, texto, total, inicio
        match valor:
            case 0:
                pasta_selecionada = self.view.controles['pastas_cb'].get()
                arquivo_selecionado = self.view.controles['arquivo_cb'].get()
                pasta_caminho_new = os.path.join(dados.biblia_dir, pasta_selecionada, arquivo_selecionado)
                texto = dados.carregar_texto(pasta_caminho_new + ".txt", dados.biblia_dir)
                # Limpa os campos de filtro
                self.view.controles['filtro_livro_txt'].delete(0, tk.END)
                self.view.controles['filtro_capitulo_txt'].delete(0, tk.END)
                # Transfere o foco para o campo de filtro de pastas
                self.view.controles['filtro_livro_txt'].focus_set()
                inicio = self.view.controles['versiculo_cb'].current() + 1
                total = len(texto)
                verso = self.view.controles['versiculo_cb'].current()
                identificacao = 0
            case 1:
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
                        identificacao = 1
                    else:
                        messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")
                else:
                    messagebox.showwarning("Aviso", "Digite o número ou nome do hino!")
            case _:
                pass


        # 1. Cria a parte visual
        visual = JanelaSlide(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        # --- Inicialização ---
        logica.view.controles['janela_slide'].bind("<Right>", lambda _: atualizar_texto(0))
        logica.view.controles['janela_slide'].bind("<Left>", lambda _: atualizar_texto(1))

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

        logica.atualizar_hora()

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
            text=texto[verso], bg="black", fg="white", font=("Arial", tamanho_letra, "bold"), wraplength=largura_texto - borda_texto)

        logica.view.controles['lbl_slide_preview'].config(
            text=texto_verificado, bg="black", fg="white", font=("Arial", int(tamanho_letra / 2), "bold"), wraplength=largura_texto / 2 - borda_texto)

        # --- Iniciar janela slide view ---
        tamanho_letra_slide = identificar_proporcao()
        def abrir_janela_slide_view(janela_slide):
            # --- Variável ---
            global frame_html

            # 1. Cria a parte visual
            visual_slide = JanelaSlideView(janela_slide, second)

            # 2. Cria a lógica e passa a visão para ela controlar
            logica_slide = Funcoes(visual_slide)

            codigo_html = justificar_texto(texto[verso], tamanho_letra_slide)
            logica_slide.view.controles['frame_html'].load_html(codigo_html)
            frame_html = logica_slide.view.controles['frame_html']

        abrir_janela_slide_view(logica.view.controles['janela_slide'])

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

            codigo_html = justificar_texto(texto[index], tamanho_letra_slide)
            frame_html.load_html(codigo_html)
            frame_html.pack(expand=True, fill="both")
            frame_html.propagate(False)  # impede que o frame se ajuste ao conteúdo

            logica.view.controles['lbl_slide_visual'].config(text=texto[index])
            if (index + 1) < len(texto):
                logica.view.controles['lbl_slide_preview'].config(text=texto[index + 1])
            else:
                logica.view.controles['lbl_slide_preview'].config(text="")

            match identificacao:
                case 0:
                    if encerrar < 1 or encerrar > len(texto):
                        logica.fechar('janela_slide')
                case 1:
                    if encerrar < 1 or encerrar > (len(texto) - 1):
                        logica.fechar('janela_slide')

    def carregar_arquivos_harpa(self):
        arquivos = os.listdir(dados.harpa_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(dados.harpa_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower()) # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        estilo.LISTA_COMPLETA = arquivos_sem_ext
        self.view.controles['arquivo_harpa_cb']["values"] = arquivos_sem_ext

        if arquivos:
            self.view.controles['arquivo_harpa_cb'].current(0)