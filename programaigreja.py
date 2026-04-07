from operator import index

import dados
import slide
import verificarversao

import argparse
import os
#import sys
#import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

VERSION = "0.3.3"
repo= "ProgramaIgreja"

class FileBrowserApp:

    # Principal
    def __init__(self, janela):
        # Config
        linha = 0
        # Declaração
        self.lista_completa = []

        parser = argparse.ArgumentParser(prog="programaigreja")
        parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
        args = parser.parse_args()

        self.janela = janela
        self.janela.title("Programa Igreja Slides")
        self.janela.geometry("440x480")
        self.janela.columnconfigure(1, weight=1)

        # Bíblia Sagrada Layout #
        ttk.Label(root, text="Bíblia Sagrada").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        linha += 1
        ttk.Label(root, text="\u2012" * 300).grid(row=linha, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        linha += 1

        # Filtro de pastas
        ttk.Label(root, text="Filtro do Livro:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.filtro_livro_txt = ttk.Entry(root)
        self.filtro_livro_txt.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        self.filtro_livro_txt.bind("<KeyRelease>", self.atualizar_pastas_biblia)
        self.filtro_livro_txt.focus_set()  # Define o foco inicial
        linha += 1

        # Combobox de pastas
        ttk.Label(root, text="Livro:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.pastas_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.pastas_cb.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        self.pastas_cb.bind("<<ComboboxSelected>>", self.atualizar_arquivos_biblia)
        linha += 1

        # Campo de filtro de arquivos
        ttk.Label(root, text="Filtro do Capítulo:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.filtro_capitulo_txt = ttk.Entry(root)
        self.filtro_capitulo_txt.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        self.filtro_capitulo_txt.bind("<KeyRelease>", self.atualizar_arquivos_biblia)
        linha += 1

        # Combobox de arquivos
        ttk.Label(root, text="Capítulo:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.arquivo_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.arquivo_cb.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        linha += 1

        # Combobox de versículos
        ttk.Label(root, text="Versículo:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.versiculo_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.versiculo_cb.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        linha += 1

        # Botão de abrir
        self.abrir_biblia_btn = ttk.Button(root, text="Abrir Arquivo", command=lambda: self.abrir_arquivo(0))
        self.abrir_biblia_btn.grid(row=linha, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        linha += 1

        # Captura especificamente o Enter
        self.filtro_capitulo_txt.bind("<Key>",
                                      lambda e: self.acao_enter_biblia(e, 0) if e.keysym in ("Return", "KP_Enter") else None)
        self.abrir_biblia_btn.bind("<Key>",
                                   lambda e: self.acao_enter_biblia(e, 0) if e.keysym in ("Return", "KP_Enter") else None)

        # Preencher pastas
        self.todas_pastas = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', 'Samuel, I', 'Samuel, II',
                             'Reis, I', 'Reis, II', 'Crônicas, I', 'Crônicas, II', 'Esdras', 'Neemias', 'Ester', 'Jó', 'Salmos', 'Provérbios',
                             'Eclesiastes', 'Cânticos', 'Isaías', 'Jeremias', 'Lamentações', 'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós',
                             'Obadias', 'Jonas', 'Miquéias', 'Naum', 'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias', 'Mateus',
                             'Marcos', 'Lucas', 'João', 'Atos', 'Romanos', 'Corintios, I', 'Corintios, II', 'Gálatas', 'Efésios', 'Filipenses',
                             'Colossenses', 'Tessalonicenses, I', 'Tessalonicenses, II', 'Timóteo, I', 'Timóteo, II', 'Tito', 'Filemom',
                             'Hebreus', 'Tiago', 'Pedro, I', 'Pedro, II', 'João, I', 'João, II', 'João, III', 'Judas', 'Apocalipse']
        self.atualizar_pastas_biblia()
        self.atualizar_versiculos()

        # Separador
        ttk.Label(root, text="\u2012" * 300).grid(row=linha, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        linha += 1

        # Fim da Bíblia Sagrada layout #
        # Harpa Cristã Layout #
        ttk.Label(root, text="Harpa Cristã").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        linha += 1
        ttk.Label(root, text="\u2012" * 300).grid(row=linha, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        linha += 1

        # Campo de filtro
        ttk.Label(root, text="Filtro do Hino:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
        self.filtro_harpa_txt = ttk.Entry(root)
        self.filtro_harpa_txt.grid(row=linha, column=1, padx=5, pady=10, sticky="ew")
        linha += 1

        # Captura qualquer tecla liberada
        self.filtro_harpa_txt.bind("<KeyRelease>", self.filtrar_lista)

        # Combobox de arquivos
        ttk.Label(root, text="Hino:").grid(row=linha, column=0, padx=5, pady=10, sticky="w")
        self.arquivo_harpa_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.arquivo_harpa_cb.grid(row=linha, column=1, padx=5, pady=5, sticky="ew")
        linha += 1

        # Botão de abrir
        self.abrir_harpa_btn = ttk.Button(root, text="Abrir Arquivo", command=lambda: self.acao_enter_harpa(self, 1))
        self.abrir_harpa_btn.grid(row=linha, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        linha += 1

        # Captura especificamente o Enter
        self.filtro_harpa_txt.bind("<Key>",
                                   lambda e: self.acao_enter_harpa(e, 1) if e.keysym in ("Return", "KP_Enter") else None)
        self.abrir_harpa_btn.bind("<Key>",
                                  lambda e: self.acao_enter_harpa(e, 1) if e.keysym in ("Return", "KP_Enter") else None)

        # Carregar arquivos
        self.carregar_arquivos_harpa()

        # verificar versão
        button_update = ttk.Button(root, text="Verificar atualização",
                                   command=lambda: verificarversao.consultar_lancamento(repo, VERSION))
        button_update.grid(row=linha, column=0, columnspan=2, padx=5, pady=10, sticky="we")
        linha += 1

    # Fim da Harpa Cristã Laytout #

    # Comandos do programa #
    def acao_enter_biblia(self, event, valor):
        # Abre o primeiro arquivo da lista filtrada, se houver
        if self.filtro_livro_txt.get() != "":
            self.abrir_arquivo(valor)
            #slide.iniciar_slide(root, dados.hinos[titulo][1])

    def acao_enter_harpa(self, valor, event):
        # Abre o primeiro arquivo da lista filtrada, se houver
        if self.filtro_harpa_txt.get() != "":
            self.filtro_harpa_txt.delete(0, tk.END)  # Limpa o campo do texto
            self.abrir_arquivo(valor)
        else:
            messagebox.showwarning("Aviso", "Digite o número ou nome do hino!")

    def atualizar_pastas_biblia(self, event=None):
        filtrar_texto = self.filtro_livro_txt.get().lower()
        filtrado = [f for f in self.todas_pastas if filtrar_texto in f.lower()]
        self.pastas_cb["values"] = filtrado
        if filtrado:
            self.pastas_cb.current(0)
            self.atualizar_arquivos_biblia()

    def atualizar_arquivos_biblia(self, event=None):
        selecionar_pasta = self.pastas_cb.get()
        texto_filtrado = self.filtro_capitulo_txt.get().lower()
        pasta_caminho = os.path.join(dados.biblia_dir, selecionar_pasta)

        #pasta_caminho_new = os.path.join(dados.biblia_dir_new, selecionar_pasta)
        #print(pasta_caminho_new)
        if os.path.isdir(pasta_caminho):
            arquivos = [f for f in os.listdir(pasta_caminho) if os.path.isfile(os.path.join(pasta_caminho, f))]

            #arquivos_new = [f for f in os.listdir(pasta_caminho_new) if os.path.isfile(os.path.join(pasta_caminho_new, f))]
            arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
            #arquivos_new = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
            arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
            if texto_filtrado:
                arquivos = [f for f in arquivos if texto_filtrado in f.lower()]
                #arquivos_new = [f for f in arquivos if texto_filtrado in f.lower()]
                arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            if arquivos_sem_ext != "":
                self.arquivo_cb["values"] = arquivos_sem_ext
            else:
                self.arquivo_cb["values"] = arquivos
            if arquivos:
                self.arquivo_cb.current(0)

        self.atualizar_versiculos()

    def atualizar_versiculos(self):
        caminho = os.path.join(dados.biblia_dir, self.pastas_cb.get(), self.arquivo_cb.get())
        contar = dados.carregar_texto(caminho + ".txt")
        versiculo = "Versículo 1"
        index = 1
        for texto in contar:
            if index < len(contar):
                versiculo = versiculo + ",Versículo " + str(index + 1)
                index += 1
        versiculos = versiculo.split(",")
        self.versiculo_cb["values"] = versiculos
        self.versiculo_cb.current(0)

    def carregar_arquivos_harpa(self):
        arquivos = os.listdir(dados.harpa_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(dados.harpa_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower()) # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        self.lista_completa = arquivos_sem_ext
        self.arquivo_harpa_cb["values"] = arquivos_sem_ext
        if arquivos:
            self.arquivo_harpa_cb.current(0)

    def filtrar_lista(self, event=None):
        texto = self.filtro_harpa_txt.get().lower()
        filtrados = [f for f in self.lista_completa if texto in f.lower()]
        self.arquivo_harpa_cb["values"] = filtrados
        if filtrados:
            self.arquivo_harpa_cb.current(0)

    def abrir_arquivo(self, valor):

        if valor == 0:

            pasta_selecionada = self.pastas_cb.get()
            arquivo_selecionado = self.arquivo_cb.get()
            #pasta_caminho = os.path.join(dados.biblia_dir, pasta_selecionada, arquivo_selecionado + ".ppt")

            pasta_caminho_new = os.path.join(dados.biblia_dir, pasta_selecionada, arquivo_selecionado)
            capitulo = dados.carregar_texto(pasta_caminho_new + ".txt")
            # Limpa os campos de filtro
            self.filtro_livro_txt.delete(0, tk.END)
            self.filtro_capitulo_txt.delete(0, tk.END)
            # Transfere o foco para o campo de filtro de pastas
            self.filtro_livro_txt.focus_set()

            slide.iniciar_slide(root, capitulo, 0, self.versiculo_cb.current())

            '''if os.path.isfile(pasta_caminho):
                try:
                    if sys.platform.startswith("win"):  # windows
                        subprocess.run(["explorer", pasta_caminho])
                    elif sys.platform.startswith("darwin"):  # macOS
                        subprocess.run(["open", pasta_caminho])
                    else:  # Linux
                        subprocess.run(["xdg-open", pasta_caminho])
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")
            else:
                messagebox.showerror("Erro", "Arquivo não encontrado.")'''
        else:
            arquivo = self.arquivo_harpa_cb.get()
            if arquivo:
                caminho = os.path.join(dados.harpa_dir, arquivo)
                hino = dados.carregar_texto(caminho + ".txt")
                self.carregar_arquivos_harpa()
                slide.iniciar_slide(root, hino, 1, 1)
            else:
                messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")
    # Fim dos comandos #

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x250")
    app = FileBrowserApp(root)
    root.mainloop()
