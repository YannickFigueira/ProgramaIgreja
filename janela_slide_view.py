import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout

class JanelaSlideView(QDialog):
    def __init__(self, parent=None, second=None):
        super().__init__(parent)

        self.nome_janela = "janela-slide-view"
        self.controles = {}

        # Remove bordas e fixa como janela de topo
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )

        self._criar_layout()

        if second is not None:
            geo = second.geometry()
            self.setGeometry(geo.x(), geo.y(), geo.width(), geo.height())

    def _criar_layout(self):
        # Layout principal da janela
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # QWebEngineView é o equivalente ao HtmlFrame do tkinterweb
        self.frame_html = QWebEngineView(self)

        # Define a cor de fundo inicial do WebView para preto para evitar um "flash" branco na inicialização
        self.frame_html.setStyleSheet("background-color: black;")

        layout_principal.addWidget(self.frame_html)

        # Mapeia nos controles como antes
        self.controles['frame_html'] = self.frame_html