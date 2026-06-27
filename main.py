import argparse
import tkinter as tk

from funcoes import Funcoes
from janela import JanelaPrincipal

# --- Configuração do CLI (Argparse) ---
parser = argparse.ArgumentParser(prog=REPO, description=nome_programa)
parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
args = parser.parse_args()

# --- Inicialização da Interface ---
if __name__ == "__main__":
    # 1. Inicia a janela base do Tkinter
    root = tk.Tk()

    # 2. Cria a parte visual (passando o root e a versão)
    visual = JanelaPrincipal(root, REPO, VERSION, nome_programa)

    # 3. Passa a visão para a sua classe de Lógica controlar
    logica = Funcoes(visual)

    # 4. Inicia o programa
    root.mainloop()