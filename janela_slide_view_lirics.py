import platform
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class JanelaSlideViewLirics(QDialog):
    def __init__(self, janela_slide, second):
        super().__init__(janela_slide)

        self.nome_janela = "janela-slide-lirics"  # Identificador para o controlador
        self.controles = {}

        # --- Configuração de Flags e Estilo da Janela ---
        # FramelessWindowHint remove as barras de título e bordas
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog

        if platform.system() == "Windows":
            # Força a janela a ficar sempre no topo se estiver no Windows
            flags |= Qt.WindowType.WindowStaysOnTopHint

        self.setWindowFlags(flags)

        # Define fundo preto padronizado para a janela de projeção
        self.setStyleSheet("background-color: black;")

        # --- Posicionamento e Exibição na Segunda Tela ---
        if second is not None:
            # Captura a geometria do monitor secundário (seja screeninfo ou QScreen)
            if hasattr(second, "geometry"):
                geo = second.geometry()
                x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()
            else:
                x, y, w, h = second.x, second.y, second.width, second.height

            self.setGeometry(x, y, w, h)

        # Constrói os componentes de layout
        self._criar_layout()

        # Exibe em tela cheia sem roubar o foco da janela principal
        self.showFullScreen()

    def _criar_layout(self):
        # Mapeia a própria janela para o dicionário de controles
        self.controles["janela_slide_view_lirics"] = self

        # --- Layout Principal (Vertical) ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 50, 0, 0)
        layout.setSpacing(0)

        # --- Label de Título ---
        self.lbl_titulo = QLabel(self)
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titulo.setStyleSheet("color: white; font-weight: bold;")

        layout.addWidget(self.lbl_titulo, alignment=Qt.AlignmentFlag.AlignTop)
        self.controles["lbl_titulo"] = self.lbl_titulo

        # --- Label do Texto/Letra ---
        self.lbl_texto = QLabel(self)
        self.lbl_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_texto.setWordWrap(True)  # Quebra linha automaticamente
        self.lbl_texto.setStyleSheet("color: white; font-weight: bold;")

        layout.addWidget(self.lbl_texto, stretch=1)
        self.controles["lbl_texto"] = self.lbl_texto