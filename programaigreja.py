import argparse
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

VERSION = "0.1.0"


class FileBrowserApp:

    # Principal
    def __init__(self, janela):
        # Declaração
        self.lista_completa = []

        parser = argparse.ArgumentParser(prog="programaigreja")
        parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
        args = parser.parse_args()

        self.janela = janela
        self.janela.title("Programa Igreja Slides")
        self.janela.geometry("400x440")
        self.janela.columnconfigure(1, weight=1)

        # Diretório base fixo
        if getattr(sys, 'frozen', False):
            # Quando rodado pelo PyInstaller
            biblia_pasta = sys._MEIPASS  # type: ignore[attr-defined] # Diretório temporário criado pelo PyInstaller
            harpa_pasta = sys._MEIPASS  # type: ignore[attr-defined] # Diretório temporário criado pelo PyInstaller
        else:
            # Quando rodado pelo Python normal
            biblia_pasta = os.path.dirname(__file__)
            harpa_pasta = os.path.dirname(__file__)

        self.biblia_dir = os.path.join(biblia_pasta, "BS Para DataShow – PowerPoint")
        self.harpa_dir = os.path.join(harpa_pasta, "Harpa Crista 640 DataShow – PowerPoint")

        # Bíblia Sagrada Layout #
        ttk.Label(root, text="Bíblia Sagrada").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(root, text="\u2012" * 300).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Filtro de pastas
        ttk.Label(root, text="Filtro do Livro:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.filtro_livro_txt = ttk.Entry(root)
        self.filtro_livro_txt.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.filtro_livro_txt.bind("<KeyRelease>", self.atualizar_pastas_biblia)
        self.filtro_livro_txt.focus_set()  # Define o foco inicial

        # Combobox de pastas
        ttk.Label(root, text="Livro:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.pastas_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.pastas_cb.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.pastas_cb.bind("<<ComboboxSelected>>", self.atualizar_arquivos_biblia)

        # Campo de filtro de arquivos
        ttk.Label(root, text="Filtro do Capítulo:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.filtro_capitulo_txt = ttk.Entry(root)
        self.filtro_capitulo_txt.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.filtro_capitulo_txt.bind("<KeyRelease>", self.atualizar_pastas_biblia)

        # Combobox de arquivos
        ttk.Label(root, text="Capítulo:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.arquivo_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.arquivo_cb.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Botão de abrir
        self.abrir_biblia_btn = ttk.Button(root, text="Abrir Arquivo", command=lambda: self.abrir_arquivo(0))
        self.abrir_biblia_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Captura especificamente o Enter
        self.filtro_capitulo_txt.bind("<Key>",
                                      lambda e: self.acao_enter(e, 0) if e.keysym in ("Return", "KP_Enter") else None)
        self.abrir_biblia_btn.bind("<Key>",
                                   lambda e: self.acao_enter(e, 0) if e.keysym in ("Return", "KP_Enter") else None)

        # Preencher pastas
        self.todas_pastas = []
        self.preencher_pastas()

        # Separador
        ttk.Label(root, text="\u2012" * 300).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Fim da Bíblia Sagrada layout #
        # Harpa Cristã Layout #
        ttk.Label(root, text="Harpa Cristã").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(root, text="\u2012" * 300).grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Campo de filtro
        ttk.Label(root, text="Filtro do Hino:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.filtro_harpa_txt = ttk.Entry(root)
        self.filtro_harpa_txt.grid(row=10, column=1, padx=5, pady=10, sticky="ew")
        # self.arquivo_hino_txt.focus_set()  # Define o foco inicial

        # Captura qualquer tecla liberada
        self.filtro_harpa_txt.bind("<KeyRelease>", self.filtrar_lista)

        # Combobox de arquivos
        ttk.Label(root, text="Hino:").grid(row=11, column=0, padx=5, pady=10, sticky="w")
        self.arquivo_harpa_cb = ttk.Combobox(root, takefocus=False, state="readonly")
        self.arquivo_harpa_cb.grid(row=11, column=1, padx=5, pady=5, sticky="ew")

        # Botão de abrir
        self.abrir_harpa_btn = ttk.Button(root, text="Abrir Arquivo", command=lambda: self.abrir_arquivo(1))
        self.abrir_harpa_btn.grid(row=12, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Captura especificamente o Enter
        self.filtro_harpa_txt.bind("<Key>",
                                   lambda e: self.acao_enter(e, 1) if e.keysym in ("Return", "KP_Enter") else None)
        self.abrir_harpa_btn.bind("<Key>",
                                  lambda e: self.acao_enter(e, 1) if e.keysym in ("Return", "KP_Enter") else None)

        # Carregar arquivos
        self.carregar_arquivos_harpa()

    # Fim da Harpa Cristã Laytout #

    # Comandos do programa #
    def acao_enter(self, event, valor):
        # Abre o primeiro arquivo da lista filtrada, se houver
        # self.filtro_hino_txt.insert(0, valor)
        self.abrir_arquivo(valor)

    def preencher_pastas(self):
        self.todas_pastas = [f for f in os.listdir(self.biblia_dir) if os.path.isdir(os.path.join(self.biblia_dir, f))]
        self.atualizar_pastas_biblia()

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
        pasta_caminho = os.path.join(self.biblia_dir, selecionar_pasta)
        if os.path.isdir(pasta_caminho):
            arquivos = [f for f in os.listdir(pasta_caminho) if os.path.isfile(os.path.join(pasta_caminho, f))]
            arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
            if texto_filtrado:
                arquivos = [f for f in arquivos if texto_filtrado in f.lower()]
            self.arquivo_cb["values"] = arquivos
            if arquivos:
                self.arquivo_cb.current(0)

    def carregar_arquivos_harpa(self):
        arquivos = os.listdir(self.harpa_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(self.harpa_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower()) # ordena ignorando maiúsculas/minúsculas
        self.lista_completa = arquivos
        self.arquivo_harpa_cb["values"] = arquivos
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
            pasta_caminho = os.path.join(self.biblia_dir, pasta_selecionada, arquivo_selecionado)

            if os.path.isfile(pasta_caminho):
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
                messagebox.showerror("Erro", "Arquivo não encontrado.")

            # Limpa os campos de filtro
            self.filtro_livro_txt.delete(0, tk.END)
            self.filtro_capitulo_txt.delete(0, tk.END)
            # Transfere o foco para o campo de filtro de pastas
            self.filtro_livro_txt.focus_set()
        else:
            arquivo = self.arquivo_harpa_cb.get()
            if arquivo:
                caminho = os.path.join(self.harpa_dir, arquivo)
                try:
                    if sys.platform.startswith("win"):  # windows
                        subprocess.run(["explorer", caminho])
                    elif sys.platform.startswith("darwin"):  # macOS
                        subprocess.run(["open", caminho])
                    else:  # Linux
                        subprocess.run(["xdg-open", caminho])
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")
            else:
                messagebox.showwarning("Aviso", "Selecione ou digite um nome de arquivo válido.")
            self.filtro_harpa_txt.delete(0, tk.END)  # Limpa o campo do texto
    # Fim dos comandos #


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x250")
    app = FileBrowserApp(root)
    root.mainloop()
