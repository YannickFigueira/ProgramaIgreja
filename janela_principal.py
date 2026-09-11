import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QTextEdit, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout
)

import config
import tema
from barra_titulo import BarraTituloCustomizada


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # Removendo bordas da janela padrão do SO para usar a customizada
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.nome_janela = "janela-principal"  # Identificador para o controlador
        self.controles = {}
        self.controles['janela_principal'] = self

        # Widget Container Principal com cantos arredondados do tema
        self.container_principal = QWidget()
        self.container_principal.setObjectName("ContainerPrincipal")
        self.setCentralWidget(self.container_principal)

        layout_geral = QVBoxLayout(self.container_principal)
        layout_geral.setContentsMargins(1, 1, 1, 1)
        layout_geral.setSpacing(0)

        # 1. Barra de Título Customizada
        titulo_texto = f"{config.NOME_PROGRAMA} {config.VERSION}"
        self.barra_titulo = BarraTituloCustomizada(self, titulo=titulo_texto)
        layout_geral.addWidget(self.barra_titulo)

        # 2. Conteúdo da Janela
        self.conteudo_widget = QWidget()
        layout_geral.addWidget(self.conteudo_widget, stretch=1)

        self._criar_layout()
        self._criar_barra_menu()

        # 3. Integração com o Tema
        tema.conectar_mudanca_tema(self)
        tema.atualizar_tema(self)

        # Configurações de redimensionamento e exibição
        self.setFixedSize(self.sizeHint())

    def _criar_layout(self):
        grid = QGridLayout(self.conteudo_widget)
        grid.setContentsMargins(12, 12, 12, 12)
        grid.setSpacing(8)

        linha = 0

        # --- BÍBLIA SAGRADA LAYOUT ---
        lbl_biblia = QLabel("Bíblia Sagrada")
        lbl_biblia.setStyleSheet("font-weight: bold; font-size: 14px;")
        grid.addWidget(lbl_biblia, linha, 0, 1, 2)
        linha += 1

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(sep1, linha, 0, 1, 2)
        linha += 1

        # Filtro de livros
        grid.addWidget(QLabel("Filtro do Livro:"), linha, 0)
        self.filtro_livro_txt = QLineEdit()
        grid.addWidget(self.filtro_livro_txt, linha, 1)
        self.controles['filtro_livro_txt'] = self.filtro_livro_txt
        linha += 1

        # Combobox de livros
        grid.addWidget(QLabel("Livro:"), linha, 0)
        self.pastas_cb = QComboBox()
        grid.addWidget(self.pastas_cb, linha, 1)
        self.controles['pastas_cb'] = self.pastas_cb
        linha += 1

        # Filtro de capítulos
        grid.addWidget(QLabel("Filtro do Capítulo:"), linha, 0)
        self.filtro_capitulo_txt = QLineEdit()
        grid.addWidget(self.filtro_capitulo_txt, linha, 1)
        self.controles['filtro_capitulo_txt'] = self.filtro_capitulo_txt
        linha += 1

        # Combobox de capítulos
        grid.addWidget(QLabel("Capítulo:"), linha, 0)
        self.arquivo_cb = QComboBox()
        grid.addWidget(self.arquivo_cb, linha, 1)
        self.controles['arquivo_cb'] = self.arquivo_cb
        linha += 1

        # Combobox de versículos (Bloqueado para digitação manual)
        grid.addWidget(QLabel("Versículo:"), linha, 0)
        self.versiculo_cb = QComboBox()
        self.versiculo_cb.setEditable(False)
        grid.addWidget(self.versiculo_cb, linha, 1)
        self.controles['versiculo_cb'] = self.versiculo_cb
        linha += 1

        # Botão de abrir Bíblia
        self.abrir_biblia_btn = QPushButton("Iniciar slide")
        self.abrir_biblia_btn.setObjectName("BtnAcao")
        grid.addWidget(self.abrir_biblia_btn, linha, 0, 1, 2)
        self.controles['abrir_biblia_btn'] = self.abrir_biblia_btn
        linha += 1

        # Separador Bíblia/Harpa
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(sep2, linha, 0, 1, 2)
        linha += 1

        # --- HARPA CRISTÃ LAYOUT ---
        lbl_harpa = QLabel("Harpa Cristã")
        lbl_harpa.setStyleSheet("font-weight: bold; font-size: 14px;")
        grid.addWidget(lbl_harpa, linha, 0, 1, 2)
        linha += 1

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.Shape.HLine)
        sep3.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(sep3, linha, 0, 1, 2)
        linha += 1

        # Filtro de hinos
        grid.addWidget(QLabel("Filtro do Hino:"), linha, 0)
        self.filtro_harpa_txt = QLineEdit()
        grid.addWidget(self.filtro_harpa_txt, linha, 1)
        self.controles['filtro_harpa_txt'] = self.filtro_harpa_txt
        linha += 1

        # Combobox de hinos
        grid.addWidget(QLabel("Hino:"), linha, 0)
        self.arquivo_harpa_cb = QComboBox()
        grid.addWidget(self.arquivo_harpa_cb, linha, 1)
        self.controles['arquivo_harpa_cb'] = self.arquivo_harpa_cb
        linha += 1

        # Botão de abrir Harpa
        self.abrir_harpa_btn = QPushButton("Iniciar slide")
        self.abrir_harpa_btn.setObjectName("BtnAcao")
        grid.addWidget(self.abrir_harpa_btn, linha, 0, 1, 2)
        self.controles['abrir_harpa_btn'] = self.abrir_harpa_btn
        linha += 1

        # --- SEPARADOR VERTICAL ---
        sep_v = QFrame()
        sep_v.setFrameShape(QFrame.Shape.VLine)
        sep_v.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(sep_v, 0, 2, linha, 1)

        # --- PAINEL LATERAL DIREITO (BUSCA) ---
        linha_lat = 0

        lbl_busca = QLabel("Busca")
        lbl_busca.setStyleSheet("font-weight: bold; font-size: 14px;")
        grid.addWidget(lbl_busca, linha_lat, 3, 1, 2)
        linha_lat += 2

        # Pasta de busca
        grid.addWidget(QLabel("Pasta de busca:"), linha_lat, 3)
        self.buscar_texto_cb = QComboBox()
        self.buscar_texto_cb.addItems(["Bíblia", "Harpa", "Músicas"])
        grid.addWidget(self.buscar_texto_cb, linha_lat, 4)
        self.controles['buscar_texto_cb'] = self.buscar_texto_cb
        linha_lat += 1

        # Campo de busca
        grid.addWidget(QLabel("Buscar:"), linha_lat, 3)
        self.buscar_texto_txt = QLineEdit()
        grid.addWidget(self.buscar_texto_txt, linha_lat, 4)
        self.controles['buscar_texto_txt'] = self.buscar_texto_txt
        linha_lat += 1

        # Botão de buscar
        self.buscar_texto_btn = QPushButton("Buscar")
        self.buscar_texto_btn.setObjectName("BtnAcao")
        grid.addWidget(self.buscar_texto_btn, linha_lat, 3, 1, 2)
        self.controles['buscar_texto_btn'] = self.buscar_texto_btn
        linha_lat += 1

        # Área de texto / Resultado da busca
        self.text_area = QTextEdit()
        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_area.setMinimumWidth(350)
        grid.addWidget(self.text_area, linha_lat, 3, 8, 2)
        self.controles['text_area'] = self.text_area

    def _criar_barra_menu(self):
        # Integração com o menu hambúrguer da BarraTituloCustomizada
        self.menu_arquivo = self.barra_titulo.adicionar_submenu("Arquivo")
        self.controles['menu_arquivo'] = self.menu_arquivo

        self.menu_ajuda = self.barra_titulo.adicionar_submenu("Ajuda")
        self.controles['menu_ajuda'] = self.menu_ajuda