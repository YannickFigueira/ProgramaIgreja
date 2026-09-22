from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLabel, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout

import config


class JanelaSlide(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.nome_janela = "janela-slide"  # Identificador para o controlador
        self.controles = {}
        self.controles['janela_slide'] = self

        # Exibe em Tela Cheia e sem bordas
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        # Cor de fundo usando a variável global do config
        self.setStyleSheet(f"QDialog {{ background-color: {config.FUNDO_COR}; }}")

        self._criar_layout()

    def _criar_layout(self):
        # Layout principal em Grid (equivalente ao .grid() do Tkinter)
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Label de controle/slide atual
        self.lbl_slide_atual = QLabel(self)
        grid_layout.addWidget(self.lbl_slide_atual, 0, 0)
        self.controles['lbl_slide_atual'] = self.lbl_slide_atual

        # Frame Principal (Exibição Visual)
        self.frame_principal = QFrame(self)
        self.frame_principal.setStyleSheet("background-color: transparent;")
        grid_layout.addWidget(self.frame_principal, 1, 0)
        self.controles['frame_principal'] = self.frame_principal

        layout_principal = QVBoxLayout(self.frame_principal)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        self.lbl_slide_visual = QLabel(self.frame_principal)
        self.lbl_slide_visual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.lbl_slide_visual)
        self.controles['lbl_slide_visual'] = self.lbl_slide_visual

        # Frame Preview (Pré-visualização do próximo slide)
        self.frame_preview = QFrame(self)
        self.frame_preview.setStyleSheet("background-color: transparent;")
        grid_layout.addWidget(self.frame_preview, 1, 1)
        self.controles['frame_preview'] = self.frame_preview

        layout_preview = QVBoxLayout(self.frame_preview)
        layout_preview.setContentsMargins(0, 0, 0, 0)

        self.lbl_slide_preview = QLabel(self.frame_preview)
        self.lbl_slide_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_preview.addWidget(self.lbl_slide_preview)
        self.controles['lbl_slide_preview'] = self.lbl_slide_preview

        # Frame Rodapé
        self.frame_rodape = QFrame(self)
        self.frame_rodape.setStyleSheet("background-color: transparent;")
        grid_layout.addWidget(self.frame_rodape, 2, 0, 1, 2,
                              Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        grid_layout.setRowStretch(2, 1)  # rowconfigure(2, weight=1)
        self.controles['frame_rodape'] = self.frame_rodape

        layout_rodape = QVBoxLayout(self.frame_rodape)
        layout_rodape.setContentsMargins(0, 0, 0, 0)

        # Label do Relógio
        self.label_relogio = QLabel("", self.frame_rodape)
        self.label_relogio.setFont(QFont("Helvetica", 50))
        self.label_relogio.setStyleSheet(f"color: white; background-color: {config.FUNDO_COR};")
        self.label_relogio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_rodape.addWidget(self.label_relogio)
        self.controles['label_relogio'] = self.label_relogio

    def showEvent(self, event):
        """Ativa a tela cheia automaticamente ao exibir a janela."""
        super().showEvent(event)
        self.showFullScreen()

    def keyPressEvent(self, event):
        """Captura o pressionamento de teclas."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()  # Fecha a janela ao pressionar ESC
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Executado quando a janela é fechada (Equivalente ao WM_DELETE_WINDOW)."""
        # Aqui você pode adicionar limpezas extras (como parar o timer do relógio) se necessário
        event.accept()