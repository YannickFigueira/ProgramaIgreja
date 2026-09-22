import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QComboBox, QPushButton, QGridLayout, QMenuBar, QWidget, QVBoxLayout, QFrame, QSizePolicy
)

# Caso não tenha o arquivo no teste local, desente a linha abaixo
from barra_titulo import BarraTituloCustomizada


class JanelaMusica(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Remove a borda/barra de título padrão do SO e define como Diálogo
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog
        )
        # 2. TORNA O FUNDO DO DIÁLOGO TRANSPARENTE (Remove as pontas brancas/escuras)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setWindowTitle("Músicas Gospel")
        # Aumentado para 180px para acomodar a Barra de Título + MenuBar + Formulário sem espremer os botões
        #self.setFixedSize(400, 180)

        self.nome_janela = "janela-musica"
        self.controles = {}

        # Dicionário de controles inclui a própria janela
        self.controles['janela_musica'] = self

        # 1. Layout Raiz da Janela
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # 2. Container Principal (QFrame)
        self.container = QFrame()
        self.container.setObjectName("ContainerPrincipal")
        layout_raiz.addWidget(self.container)

        # 3. Layout INTERNO do Container Principal
        layout_container = QVBoxLayout(self.container)
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setSpacing(0)

        # --- A) Barra de título personalizada no topo ---
        self.barra_titulo = BarraTituloCustomizada(self, titulo="Músicas Gospel")
        layout_container.addWidget(self.barra_titulo)

        # --- B) Barra de Menu (Inserida abaixo da barra de título) ---
        self._criar_barra_menu()

        # --- C) Conteúdo dos Filtros e Botões ---
        self.conteudo_widget = QWidget()
        layout_container.addWidget(self.conteudo_widget, stretch=1)

        self._criar_layout()

    def _criar_layout(self):
        layout = QGridLayout(self.conteudo_widget)

        layout.setContentsMargins(12, 8, 12, 12)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        # Controle de estiramento das colunas para impedir que o QLineEdit extrapole a janela
        layout.setColumnStretch(0, 0)  # Coluna dos labels fica do tamanho exato do texto
        layout.setColumnStretch(1, 1)  # Coluna dos campos ocupa o espaço restante

        linha = 0

        # Filtro das músicas
        lbl_filtro = QLabel("Filtro da Música:")
        layout.addWidget(lbl_filtro, linha, 0)

        self.filtro_musica_txt = QLineEdit()
        self.filtro_musica_txt.setFocus()  # Define o foco inicial
        # Define a política de expansão para se adaptar dentro da janela sem forçar estouro
        self.filtro_musica_txt.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.filtro_musica_txt, linha, 1)
        self.controles['filtro_musica_txt'] = self.filtro_musica_txt
        linha += 1

        # Combobox de músicas
        lbl_musica = QLabel("Música:")
        layout.addWidget(lbl_musica, linha, 0)

        self.musica_cb = QComboBox()
        self.musica_cb.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.musica_cb, linha, 1)
        self.controles['musica_cb'] = self.musica_cb
        linha += 1

        # Botão de abrir
        self.abrir_musica_btn = QPushButton("Iniciar slide")
        self.abrir_musica_btn.setObjectName("BtnAcao")
        layout.addWidget(self.abrir_musica_btn, linha, 0, 1, 2)
        self.controles['abrir_musica_btn'] = self.abrir_musica_btn

    def _criar_barra_menu(self):
        # Menu Arquivo
        self.menu_arquivo = self.barra_titulo.adicionar_submenu("Arquivo")
        self.controles['menu_arquivo'] = self.menu_arquivo