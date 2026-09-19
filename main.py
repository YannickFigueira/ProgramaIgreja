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
# --- Inicialização da Interface ---
if __name__ == "__main__":
    # 1. Inicia a aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName(config.NOME_PROGRAMA)
    app.setApplicationDisplayName(config.NOME_PROGRAMA)

    # 2. Instancia a janela principal
    visual = JanelaPrincipal()

    # 3. Centraliza a janela principal na tela primária
    primary_screen = app.primaryScreen()
    if primary_screen:
        screen_geometry = primary_screen.availableGeometry()
        window_geometry = visual.frameGeometry()
        # Move o centro do retângulo da janela para o centro da tela
        window_geometry.moveCenter(screen_geometry.center())
        visual.move(window_geometry.topLeft())

    # 4. Passa a visão para a classe de Lógica controlar
    logica = Funcoes(visual)

    # 5. Exibe a janela, traz para frente e força o foco do sistema operacional
    visual.show()
    visual.raise_()
    visual.activateWindow()

    # 6. Inicia o loop de eventos
    sys.exit(app.exec())