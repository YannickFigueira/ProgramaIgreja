
import os
from tkinter import messagebox
import tkinter as tk
import sys

# Diretórios base
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

biblia_dir = os.path.join(base_dir, "BS Para DataShow – PowerPoint")
harpa_dir = os.path.join(base_dir, "HarpaTexto")

# Variáveis da instância
hinos = []
titulo = 0
paragrafo = 0

    # ---------------- Métodos auxiliares ---------------- #

def carregar_hinos():
    """Carrega todos os hinos da pasta HarpaTexto"""
    if not os.path.exists(harpa_dir):
        messagebox.showerror("Erro", f"Pasta não encontrada: {harpa_dir}")
        return

    for arquivo in sorted(os.listdir(harpa_dir)):
        if arquivo.endswith(".txt"):
            caminho = os.path.join(harpa_dir, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                texto = f.read()
                paragrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
                hinos.append(paragrafos)

# Carregar Hinos
carregar_hinos()