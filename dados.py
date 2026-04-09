
import os
from tkinter import messagebox
import sys

# Diretórios base
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

#biblia_dir = os.path.join(base_dir, "BS Para DataShow – PowerPoint")
biblia_dir = os.path.join(base_dir, "Biblia")
harpa_dir = os.path.join(base_dir, "HarpaTexto")

# Variáveis da instância

    # ---------------- Métodos auxiliares ---------------- #

def carregar_texto(caminho, diretorio):
    """Carrega todo o texto da pasta HarpaTexto"""
    if not os.path.exists(diretorio):
        messagebox.showerror("Erro", f"Pasta não encontrada: {diretorio}")

    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()
        paragrafo = [p.strip() for p in texto.split("\n\n") if p.strip()]
        return paragrafo