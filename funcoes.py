import logging
import os
import platform
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

import dados
import estilo
import verificarversao
from janela_slide import JanelaSlide

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

# --- Comandos do Menu
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

class Funcoes:
    def __init__(self, view):
        self.view = view

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "janela-slide":
                self._vincular_janela_slide()

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

        # --- Controles da Janela Principal ---
        self.view.controles['filtro_livro_txt'].bind("<KeyRelease>", self.atualizar_pastas_biblia)
        self.view.controles['pastas_cb'].bind("<<ComboboxSelected>>", self.atualizar_arquivos_biblia)
        self.view.controles['filtro_capitulo_txt'].bind("<KeyRelease>", self.atualizar_arquivos_biblia)
        self.view.controles['arquivo_cb'].bind("<<ComboboxSelected>>", self.atualizar_versiculos)
        self.view.controles['abrir_biblia_btn'].config(command=lambda: self.abrir_arquivo(0))
        # Captura especificamente o Enter
        self.view.controles['filtro_capitulo_txt'].bind("<Key>", lambda e: self.acao_enter(e, 0))
        self.view.controles['abrir_biblia_btn'].bind("<Key>", lambda e: self.acao_enter(e, 0))

        # --- Menu da Janela Principal ---
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                    command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão",
                                    command=lambda: abrir_logs())
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                                    command=lambda: visitar_site())
        self.view.controles['menu_ajuda'].add_command(label="Sair", command=self.view.controles['janela_principal'].quit)

    def _vincular_janela_slide(self):
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

    def atualizar_versiculos(self):
        caminho = os.path.join(dados.biblia_dir, self.view.controles['pastas_cb'].get(), self.view.controles['arquivo_cb'].get())
        contar = dados.carregar_texto(caminho + ".txt", dados.biblia_dir)
        versiculo = "Versículo 1"
        index = 2

        for texto in contar:
            if index <= len(contar):
                versiculo = versiculo + ",Versículo " + str(index)
                index += 1

        versiculos = versiculo.split(",")
        self.view.controles['versiculo_cb']["values"] = versiculos
        self.view.controles['versiculo_cb'].current(0)

    def abrir_arquivo(self, valor):

        if valor == 0:
            pasta_selecionada = self.view.controles['pastas_cb'].get()
            arquivo_selecionado = self.view.controles['arquivo_cb'].get()
            pasta_caminho_new = os.path.join(dados.biblia_dir, pasta_selecionada, arquivo_selecionado)
            capitulo = dados.carregar_texto(pasta_caminho_new + ".txt", dados.biblia_dir)
            # Limpa os campos de filtro
            self.view.controles['filtro_livro_txt'].delete(0, tk.END)
            self.view.controles['filtro_capitulo_txt'].delete(0, tk.END)
            # Transfere o foco para o campo de filtro de pastas
            self.view.controles['filtro_livro_txt'].focus_set()
            self.abrir_janela_slide(capitulo, 0, self.view.controles['versiculo_cb'].current())
        else:
            if self.filtro_harpa_txt.get() != "":
                self.filtro_harpa_txt.delete(0, tk.END)  # Limpa o campo do texto

                arquivo = self.arquivo_harpa_cb.get()
                if arquivo:
                    caminho = os.path.join(dados.harpa_dir, arquivo)
                    hino = dados.carregar_texto(caminho + ".txt", dados.harpa_dir)
                    self.carregar_arquivos_harpa()
                    #slide.iniciar_slide(root, hino, 1, 1)
                    self.abrir_janela_slide()
                else:
                    messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")
            else:
                messagebox.showwarning("Aviso", "Digite o número ou nome do hino!")
    # Iniciar janela slide

    def abrir_janela_slide(self, texto, identificacao, verso):
        # 1. Cria a parte visual
        visual = JanelaSlide(self.view.controles['janela_principal'])

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)
        # --- Verificação ---
        texto_verificado = ""
        if not len(texto) == (verso + 1):
                texto_verificado = texto[verso + 1]

        logica.view.controles['lbl_slide_atual'].config(
            text=f"{verso + identificacao + 1} / {len(texto) - identificacao}", bg=estilo.FUNDO_COR, font=("Arial", 20, "bold"))