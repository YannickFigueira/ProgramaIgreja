import os
import sys
import argparse
from PyQt6.QtWidgets import QApplication

# Desativa a inicialização da GPU pelo Chromium para evitar avisos de GPUInfo/GBM
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-gpu "
    "--disable-software-rasterizer "
    "--disable-dev-shm-usage "
    "--no-sandbox"
)

import config
from funcoes import Funcoes
from janela_principal import JanelaPrincipal

# --- Configuração do CLI (Argparse) ---
parser = argparse.ArgumentParser(prog=config.REPO, description=config.NOME_PROGRAMA)
parser.add_argument("--version", action="version", version=f"%(prog)s {config.VERSION}")
args = parser.parse_args()

# --- Inicialização da Interface ---
if __name__ == "__main__":
    # 1. Inicia a aplicação Qt
    app = QApplication(sys.argv)

    # 2. Instancia a janela principal (herdada de QMainWindow ou QWidget)
    visual = JanelaPrincipal()

    # 3. Passa a visão para a classe de Lógica controlar
    logica = Funcoes(visual)

    # 4. Exibe a janela e inicia o loop de eventos
    visual.show()
    sys.exit(app.exec())