import math
import os
import platform
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from tkinter import messagebox, filedialog

# Desativa aceleração de hardware problemática do Chromium no Linux/X11/Wayland
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
# Força o uso do backend OpenGL/Software padronizado
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"

from PyQt6.QtCore import QUrl, Qt, QTimer, QStandardPaths
from PyQt6.QtGui import QDesktopServices, QFont, QGuiApplication
from PyQt6.QtWidgets import QMessageBox, QSizePolicy, QFileDialog

import dados, config, verificarversao
from arquivo_log import ler_pasta_log, abrir_logs, gerar_arquivo_log, registrar_log
from janela_logs import JanelaLogs

from janela_slide import JanelaSlide
from janela_slide_view import JanelaSlideView
from janela_musica import JanelaMusica
from janela_slide_view_lirics import JanelaSlideViewLirics

# Variáveis globais
lista_completa = []
lista_musicas = []
janela_logs_aberta = False

# --- Comandos gerais ---
def justificar_texto(texto_slide_view, tamanho_letra_slide):
    largura_slide = "91%"
    tamanho_fonte = f"{tamanho_letra_slide}px"

    # Formata quebras de linha para HTML
    texto_formatado = texto_slide_view.replace('\n', '<br>').upper()

    codigo_html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="utf-8">
        <style>
            html, body {{
                background-color: black;
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden; /* Evita barras de rolagem na exibição */
            }}
            .slide-conteudo {{
                color: white; 
                font-family: Arial, sans-serif; 
                font-size: {tamanho_fonte}; 
                font-weight: bold; 
                text-align: center;
                margin: auto;
                max-width: {largura_slide};
                width: 100%;
                line-height: 1.1;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div id="conteudo-slide" class="slide-conteudo">
            {texto_formatado}
        </div>
    </body>
    </html>
    """

    return codigo_html

def identificar_proporcao(width, height):
    relacao = width / height
    tela16_9 = int(height *.086)
    tela4_3 = int(height *.074)
    if abs(relacao - (16 / 9)) < 0.05:
        return tela16_9
    elif abs(relacao - (4 / 3)) < 0.05:
        return tela4_3
    elif abs(relacao - (16 / 10)) < 0.05:
        return tela16_9
    elif relacao > 2.0:
        return tela16_9
    else:
        return tela16_9


def identificar_monitor():
    telas = QGuiApplication.screens()

    if not telas:
        return None, None

    first = None

    # 1. Busca o monitor primário oficial do SO
    for t in telas:
        geo = t.geometry()
        # No Qt, testamos t.isPrimary() ou a origem X=0, Y=0
        if t == QGuiApplication.primaryScreen() or (geo.x() == 0 and geo.y() == 0):
            first = t
            break

    # Fallback se não encontrar a origem
    if not first:
        first = telas[0]

    # 2. Identifica o monitor secundário
    if len(telas) > 1:
        outros = [t for t in telas if t != first]
        second = outros[0] if outros else telas[1]
    else:
        second = first

    return first, second

def remover_acentos(filtro_texto):
    """Remove acentos e caracteres especiais do texto."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', filtro_texto)
        if unicodedata.category(c) != 'Mn'
    )


def abrir_pasta_musica():
    if platform.system() == "Windows":
        # arquivo = "C:\\Programa Igreja\\doc\\CHANGELOG.md"
        subprocess.run(["explorer", config.MUSICAS_DIR])
    elif platform.system() == "Linux":
        # arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
        subprocess.run(["xdg-open", config.MUSICAS_DIR])  # ou "gedit"
    else:
        print("Sistema não suportado")


class Funcoes:
    def __init__(self, view):
        self.view = view
        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "janela-slide":
                self._vincular_janela_slide()
            elif view.nome_janela == "janela-slide-view":
                self._vincular_janela_slide_view()
            elif view.nome_janela == "janela-musica":
                self._vincular_janela_musica()
            elif view.nome_janela == "janela-slide-lirics":
                self._vincular_janela_slide_view_lirics()
            elif view.nome_janela == "logs":
                self._vincular_logs()

    def _vincular_janela_principal(self):
        # --- Inicialização ---
        # Só executa a lógica do Mutex se estiver rodando no Windows
        if os.name == 'nt':
            # noinspection PyBroadException
            try:
                import ctypes
                # Cria o Mutex único para o Inno Setup detectar
                # noinspection PyUnresolvedReferences
                mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MeuProgramaIgrejaMutexUnico")
                # 183 é o código para ERROR_ALREADY_EXISTS (programa já aberto)
                # noinspection PyUnresolvedReferences
                if ctypes.windll.kernel32.GetLastError() == 183:
                    sys.exit(0)
            except AttributeError:
                # Prevenção caso o ambiente mude abruptamente
                pass
            except Exception:
                pass

        self.atualizar_pastas_biblia()
        #self.atualizar_versiculos()
        self.carregar_arquivos_harpa()

        # --- Controles da Janela Principal ---
        self.view.controles['filtro_livro_txt'].textChanged.connect(self.atualizar_pastas_biblia)
        self.view.controles['pastas_cb'].currentTextChanged.connect(self.atualizar_arquivos_biblia)

        self.view.controles['filtro_capitulo_txt'].textChanged.connect(self.atualizar_arquivos_biblia)
        self.view.controles['arquivo_cb'].currentTextChanged.connect(self.atualizar_versiculos)
        self.view.controles['abrir_biblia_btn'].clicked.connect(lambda: self.abrir_janela_slide("biblia"))
        # Captura especificamente o Enter
        self.view.controles['filtro_capitulo_txt'].returnPressed.connect(
            lambda: self.acao_enter("biblia")
        )
        #self.view.controles['abrir_biblia_btn'].clicked.connect(lambda e: self.acao_enter(e, "biblia", self.view.controles['janela_principal']))
        # Captura qualquer tecla liberada
        self.view.controles['filtro_harpa_txt'].textChanged.connect(self.filtrar_lista_harpa)
        self.view.controles['abrir_harpa_btn'].clicked.connect(lambda: self.abrir_janela_slide("harpa"))
        #self.view.controles['abrir_harpa_btn'].configure(
        #    command=lambda: self.abrir_slide_lirics())
        # Captura especificamente o Enter
        self.view.controles['filtro_harpa_txt'].returnPressed.connect(lambda: self.acao_enter("harpa"))
        #self.view.controles['abrir_harpa_btn'].bind("<Key>", lambda e: self.acao_enter(e, "harpa", self.view.controles['janela_principal']))
        #self.view.controles['abrir_harpa_btn'].bind("<Key>", lambda e: self.abrir_slide_lirics())
        self.view.controles['buscar_texto_btn'].clicked.connect(lambda: self.localizar_arquivo())
        self.view.controles['buscar_texto_txt'].returnPressed.connect(lambda: self.acao_enter("localizar"))

        # --- Menu da Janela Principal ---
        self.view.controles['menu_arquivo'].addAction("Músicas", lambda: self.abrir_janela_musica())
        self.view.controles['menu_arquivo'].addAction("Logs", lambda: self.abrir_janela_logs())
        self.view.controles['menu_ajuda'].addAction("Verificar atualização", lambda: verificarversao.consultar_lancamento(config.REPO, config.VERSION, self.view))
        self.view.controles['menu_ajuda'].addAction("Notas da versão", lambda: abrir_logs(self.view))
        self.view.controles['menu_ajuda'].addAction("Sobre", lambda: self.visitar_site())
        self.view.controles['menu_ajuda'].addAction("Sair", self.view.close)


    def _vincular_janela_slide(self):
        pass

    def _vincular_janela_slide_view(self):
        pass

    def _vincular_janela_slide_view_lirics(self):
        pass

    def _vincular_janela_musica(self):
        # --- Inicialização ---
        if os.listdir(config.MUSICAS_DIR):
            self.carregar_arquivos_musicas()
        # --- Menu da janela musicas ---
        self.view.controles['menu_arquivo'].addAction("Adicionar Música",
                                                        lambda: self.selecionar_arquivo(self.view))
        self.view.controles['menu_arquivo'].addAction("Abrir pasta das músicas",
                                                        lambda: abrir_pasta_musica())
        # Captura qualquer tecla
        self.view.controles['filtro_musica_txt'].textChanged.connect(self.filtrar_lista_musicas)
        self.view.controles['abrir_musica_btn'].clicked.connect(lambda: self.abrir_janela_slide("musica"))


    def _vincular_logs(self):
        # --- Inicialização da janela logs ---
        arquivos_log = ler_pasta_log()
        texto_log = "\n".join([f"{item}" for item in arquivos_log])

        # --- Controles da Janlea Logs ---

        self.view.controles['lbl_logs'].setText(texto_log)
        # 1. Atualiza as opções do ComboBox
        self.view.controles['cmb_selecao'].clear()
        self.view.controles['cmb_selecao'].addItems(arquivos_log)

        # 2. Define o valor selecionado usando o funcao .set()
        if arquivos_log:
            self.view.controles['cmb_selecao'].setCurrentIndex(0)
        self.view.controles['btn_abrir_logs'].clicked.connect(lambda: abrir_logs(self.view))

    # --- Inicialização das janelas ---
    # --- Iniciar janela slide ---
    def abrir_janela_slide(self, slide):
        global inicio, total, texto, verso

        match slide:
            case "biblia":
                pasta_selecionada = self.view.controles["pastas_cb"].currentText()
                arquivo_selecionado = self.view.controles[
                    "arquivo_cb"
                ].currentText()
                pasta_caminho_new = os.path.join(
                    dados.biblia_dir, pasta_selecionada, arquivo_selecionado
                )
                texto = dados.carregar_texto(
                    pasta_caminho_new + ".txt", dados.biblia_dir
                )
                inicio = self.view.controles["versiculo_cb"].currentIndex() + 1

                # Limpa os campos de filtro
                self.view.controles["filtro_livro_txt"].clear()
                self.view.controles["filtro_capitulo_txt"].clear()
                total = len(texto)
                verso = inicio - 1

            case "harpa":
                if self.view.controles["filtro_harpa_txt"].text() != "":
                    arquivo = self.view.controles["arquivo_harpa_cb"].currentText()
                    self.view.controles["filtro_harpa_txt"].clear()

                    if arquivo:
                        caminho = os.path.join(dados.harpa_dir, arquivo)
                        texto = dados.carregar_texto(
                            caminho + ".txt", dados.harpa_dir
                        )
                        self.carregar_arquivos_harpa()
                        inicio = 1
                        total = len(texto) - 1
                        verso = 1
                    else:
                        QMessageBox.warning(
                            self.view,
                            "Aviso",
                            "Selecione ou digite um nome de arquivo válido.",
                        )
                        return
                else:
                    QMessageBox.warning(
                        self.view, "Aviso", "Digite o número ou nome do hino!"
                    )
                    return

            case "musica":
                self.view.controles["filtro_musica_txt"].clear()
                arquivo = self.view.controles["musica_cb"].currentText()

                if arquivo:
                    caminho = os.path.join(config.MUSICAS_DIR, arquivo)
                    texto = dados.carregar_texto(
                        caminho + ".txt", config.MUSICAS_DIR
                    )
                    self.carregar_arquivos_musicas()
                    inicio = 1
                    total = len(texto) - 1
                    verso = 1
                else:
                    QMessageBox.warning(
                        self.view,
                        "Aviso",
                        "Selecione ou digite um nome de arquivo válido.",
                    )
                    return

        # 1. Cria a parte visual e guarda a referência na classe (Evita destruição pelo GC)
        self.visual_slide_control = JanelaSlide()
        self.logica_slide_control = Funcoes(self.visual_slide_control)

        # Identifica a quantidade de monitores
        first, second = identificar_monitor()

        # --- Mapeamento das Teclas ---
        janela_control = self.logica_slide_control.view.controles["janela_slide"]
        key_press_original = janela_control.keyPressEvent
        janela_control = self.logica_slide_control.view.controles["janela_slide"]

        def tratar_teclas(event):
            # Fecha se pressionar ESC ou Q
            if event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Q):
                if hasattr(self, "visual_slide_projecao") and self.visual_slide_projecao:
                    self.visual_slide_projecao.close()
                if hasattr(self, "visual_slide_control") and self.visual_slide_control:
                    self.visual_slide_control.close()
                event.accept()
                return

            if event.key() == Qt.Key.Key_Right:
                atualizar_texto(0)
                event.accept()
            elif event.key() == Qt.Key.Key_Left:
                atualizar_texto(1)
                event.accept()
            else:
                # Repassa para o evento original caso precise
                key_press_original = getattr(janela_control, "_key_original", None)
                if key_press_original:
                    key_press_original(event)

        # Armazena e sobrescreve o evento na instância
        janela_control._key_original = janela_control.keyPressEvent
        janela_control.keyPressEvent = tratar_teclas

        # --- Inicialização do Relógio (QTimer) ---
        self.logica_slide_control.timer_relogio = QTimer(janela_control)
        self.logica_slide_control.timer_relogio.timeout.connect(
            self.logica_slide_control.atualizar_hora
        )
        self.logica_slide_control.timer_relogio.start(1000)
        self.logica_slide_control.atualizar_hora()

        # Dimensões para proporção da tela primária
        largura = first.geometry().width() // 2
        altura = first.geometry().height() // 2

        medida_letra = 16
        tamanho_letra = int(altura / medida_letra)

        texto_verificado = ""
        if not len(texto) == verso + 1:
            texto_verificado = texto[verso + 1]

        # --- Configuração de Tamanhos dos Frames (Respeitando a Proporção) ---
        frame_principal = self.logica_slide_control.view.controles["frame_principal"]
        frame_preview = self.logica_slide_control.view.controles["frame_preview"]
        frame_rodape = self.logica_slide_control.view.controles["frame_rodape"]

        frame_principal.setFixedSize(int(largura), int(altura))
        frame_preview.setFixedSize(int(largura // 2), int(altura // 2))
        frame_rodape.setFixedSize(int(largura), int(altura // 4))

        # --- Label Slide Atual ---
        lbl_atual = self.logica_slide_control.view.controles["lbl_slide_atual"]
        lbl_atual.setText(f"{inicio} / {total}")
        lbl_atual.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lbl_atual.setStyleSheet(f"background-color: {config.FUNDO_COR}; color: white;")

        # --- Label Slide Visual (Principal) ---
        lbl_visual = self.logica_slide_control.view.controles["lbl_slide_visual"]
        lbl_visual.setText(texto[verso])
        lbl_visual.setFont(QFont("Arial", int(tamanho_letra), QFont.Weight.Bold))
        lbl_visual.setStyleSheet("background-color: black; color: white;")
        lbl_visual.setWordWrap(True)
        lbl_visual.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Label Slide Preview (Próximo) ---
        lbl_preview = self.logica_slide_control.view.controles["lbl_slide_preview"]
        lbl_preview.setText(texto_verificado)
        lbl_preview.setFont(
            QFont("Arial", int(tamanho_letra / 2), QFont.Weight.Bold)
        )
        lbl_preview.setStyleSheet("background-color: black; color: white;")
        lbl_preview.setWordWrap(True)
        lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Margens da Grid ---
        layout_grid = self.logica_slide_control.view.controles["janela_slide"].layout()
        if layout_grid:
            espace_largura = 20
            espace_altura = 10
            layout_grid.setContentsMargins(espace_largura, espace_altura, espace_largura, espace_altura)
            layout_grid.setSpacing(espace_largura)

        self.visual_slide_control.showFullScreen()

        # Cálculo de proporção da segunda tela
        second_geo = second.geometry()
        tamanho_letra_slide = identificar_proporcao(
            int(second_geo.width()), int(second_geo.height())
        )

        match slide:
            case "biblia":
                self.abrir_janela_slide_view(second, tamanho_letra_slide)
            case _:
                titulo_txt = f"{texto[0].replace('\n', ' - ')} - 1 / {total} "
                self.visual_slide_projecao = self.abrir_slide_lirics(titulo_txt, texto[1])

        # --- FORÇAR EXIBIÇÃO E FOCO NA JANELA DO OPERADOR ---
        janela_control = self.logica_slide_control.view.controles["janela_slide"]

        # 1. Configura a janela para ser a ativa
        self.visual_slide_control.showFullScreen()
        self.visual_slide_control.raise_()
        self.visual_slide_control.activateWindow()

        # 2. Garante o foco do teclado no widget do container
        janela_control.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        janela_control.setFocus()

        # 3. Solução para o S.O (Garante o foco após a transição de renderização do SO/X11/Wayland/Windows)
        def aplicar_foco_definitivo():
            if hasattr(self, 'visual_slide_control') and self.visual_slide_control:
                self.visual_slide_control.raise_()
                self.visual_slide_control.activateWindow()
                janela_control.setFocus()

        QTimer.singleShot(100, aplicar_foco_definitivo)

        index = verso
        index_contador = inicio
        encerrar = inicio

        def atualizar_texto(valor_atualizar):
            nonlocal index, encerrar, index_contador

            if valor_atualizar == 0:
                index = (index + 1) % len(texto)
                encerrar += 1
                index_contador += 1
            else:
                index = (index - 1) % len(texto)
                encerrar -= 1
                index_contador -= 1

            # Substituído .config() por .setText()
            self.logica_slide_control.view.controles["lbl_slide_atual"].setText(
                f"{index_contador} / {total}"
            )
            self.logica_slide_control.view.controles["lbl_slide_visual"].setText(
                texto[index]
            )

            if (index + 1) < len(texto):
                self.logica_slide_control.view.controles[
                    "lbl_slide_preview"
                ].setText(texto[index + 1])
            else:
                self.logica_slide_control.view.controles[
                    "lbl_slide_preview"
                ].setText("")

            match slide:
                case "biblia":
                    if hasattr(self, "frame_html") and self.frame_html:
                        # Prepara e limpa o texto para evitar quebras de sintaxe no JavaScript
                        texto_formatado = texto[index].replace('\n', '<br>').upper()
                        texto_js = texto_formatado.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

                        # Injeta a alteração diretamente no DOM sem recarregar o navegador
                        script = f"document.getElementById('conteudo-slide').innerHTML = '{texto_js}';"
                        self.frame_html.page().runJavaScript(script)

                    if encerrar < 1 or encerrar > len(texto):
                        self.visual_slide_projecao.close()
                        self.visual_slide_control.close()
                        # self.fechar("janela_slide")
                case _:
                    titulo_fmt = (
                        f"{texto[0].replace('\n', ' - ')} - {index} / {total} "
                    )
                    self.visual_slide_projecao.controles["lbl_titulo"].setText(titulo_fmt)
                    self.visual_slide_projecao.controles["lbl_texto"].setText(texto[index].upper())

                    if encerrar < 1 or encerrar > (len(texto) - 1):
                        self.visual_slide_projecao.close()
                        self.visual_slide_control.close()

        # Exibe a janela de controle do operador
        self.visual_slide_control.show()

    # --- Abrir janela slide view (Projeção) ---
    def abrir_janela_slide_view(self, second, tamanho_letra_slide):
        self.visual_slide_projecao = JanelaSlideView(second=second)
        self.logica_slide_projecao = Funcoes(self.visual_slide_projecao)

        codigo_html = justificar_texto(texto[verso], tamanho_letra_slide)

        self.frame_html = self.logica_slide_projecao.view.controles["frame_html"]
        self.frame_html.setHtml(codigo_html)

        if second is not None:
            geo = second.geometry()
            self.visual_slide_projecao.setGeometry(geo.x(), geo.y(), geo.width(), geo.height())

        # Exibe a projeção sem chamar o activateWindow() para não roubar o foco da janela do operador
        self.visual_slide_projecao.showFullScreen()

    # --- Abrir janela slide lirics ---
    def abrir_slide_lirics(self, titulo, texto_slide):
        # --- Inicialização ---
        first, second = identificar_monitor()

        largura = 0
        if second is not None:
            geo = second.geometry()
            largura = geo.width() / 2

        borda_texto = int(largura * 0.1)

        # 1. Cria a parte visual
        visual_slide_projecao = JanelaSlideViewLirics(self.view, second)
        logica_slide_projecao = Funcoes(visual_slide_projecao)

        # --- Ajuste do Título ---
        lbl_titulo = logica_slide_projecao.view.controles['lbl_titulo']
        lbl_titulo.setText(str(titulo))
        lbl_titulo.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet("background-color: black; color: white;")

        #logica_slide_projecao.view.controles['lbl_titulo'].pack(pady=(50,0))

        #logica_slide_projecao.view.controles['janela_slide_view_lirics'].config(bg="black")
        # --- Ajuste da Letra ---
        lbl_texto = logica_slide_projecao.view.controles['lbl_texto']
        lbl_texto.setText(texto_slide.upper())
        lbl_texto.setWordWrap(True)
        lbl_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Cálculo dinâmico do tamanho da fonte com base na altura do monitor
        alt_monitor = second.geometry().height() if hasattr(second, "geometry") else second.height
        tamanho_fonte = int(alt_monitor * 0.064)

        lbl_texto.setFont(QFont("Arial", tamanho_fonte, QFont.Weight.Bold))
        lbl_texto.setStyleSheet("background-color: black; color: white;")

        return logica_slide_projecao.view

    # --- Abrir janela música
    def abrir_janela_musica(self):
        # 1. Cria a parte visual
        visual_musica = JanelaMusica(self.view)

        # 2. Cria a lógica e passa a visão para ela controlar
        logica_slide = Funcoes(visual_musica)

        visual_musica.show()

    # --- Abrir janela de logs ---
    def abrir_janela_logs(self):
        global janela_logs_aberta
        # 1. Cria a parte visual
        visual = JanelaLogs(self.view)

        # 2. Cria a lógica e passa a visão para ela controlar
        logica = Funcoes(visual)

        janela_logs_aberta = True
        visual.exec()
        janela_logs_aberta = False

    # --- Comandos da Janela Principal ---
    def atualizar_pastas_biblia(self, texto_filtro=""):
        # Obtém o texto do filtro (caso a função seja chamada manualmente sem argumento)
        if not isinstance(texto_filtro, str):
            texto_filtro = self.view.controles['filtro_livro_txt'].text()

        filtrar_texto = remover_acentos(texto_filtro.lower())
        filtrado = [f for f in config.TODAS_PASTAS if filtrar_texto in remover_acentos(f.lower())]

        combo_pastas = self.view.controles['pastas_cb']

        # Bloqueia temporariamente os sinais para evitar chamadas de eventos em cadeia ao limpar/adicionar
        combo_pastas.blockSignals(True)
        combo_pastas.clear()
        combo_pastas.addItems(filtrado)
        combo_pastas.blockSignals(False)

        if filtrado:
            combo_pastas.setCurrentIndex(0)
            self.atualizar_arquivos_biblia()

    def atualizar_arquivos_biblia(self, texto_selecionado=None):
        selecionar_pasta = self.view.controles['pastas_cb'].currentText()

        # Se nenhuma pasta estiver selecionada (ex: combobox vazia), interrompe a execução
        if not selecionar_pasta:
            return

        texto_filtrado = self.view.controles['filtro_capitulo_txt'].text().lower()
        pasta_caminho = os.path.join(dados.biblia_dir, selecionar_pasta)

        if os.path.isdir(pasta_caminho):
            arquivos = [f for f in os.listdir(pasta_caminho) if os.path.isfile(os.path.join(pasta_caminho, f))]
            arquivos = sorted(arquivos, key=lambda x: x.lower())  # ordena ignorando maiúsculas/minúsculas

            if texto_filtrado:
                arquivos = [f for f in arquivos if texto_filtrado in f.lower()]

            arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]

            combo_arquivo = self.view.controles['arquivo_cb']

            # Bloqueia temporariamente os sinais para evitar chamadas de eventos em cadeia ao limpar e recarregar
            combo_arquivo.blockSignals(True)
            combo_arquivo.clear()

            if arquivos_sem_ext:
                combo_arquivo.addItems(arquivos_sem_ext)
                combo_arquivo.setCurrentIndex(0)

            combo_arquivo.blockSignals(False)

        self.atualizar_versiculos()

    def atualizar_versiculos(self, event=None):
        caminho = os.path.join(dados.biblia_dir, self.view.controles['pastas_cb'].currentText(), self.view.controles['arquivo_cb'].currentText())
        contar = dados.carregar_texto(caminho + ".txt", dados.biblia_dir)

        # Gera "Versículo 1,Versículo 2,Versículo 3..." direto pela quantidade de itens
        versiculo = [f"Versículo {i}" for i in range(1, len(contar) + 1)]

        #combo_versiculo = self.view.controles['versiculo_cb']
        self.view.controles['versiculo_cb'].clear()
        self.view.controles['versiculo_cb'].addItems(versiculo)
        self.view.controles['versiculo_cb'].setCurrentIndex(0)

    def atualizar_hora(self):
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        self.view.controles['label_relogio'].setText(hora_formatada)

    def fechar(self, nome):
        self.view.controles[nome].destroy()

    def acao_enter(self, slide):
        if slide == "localizar":
            self.localizar_arquivo()
        else:
            self.abrir_janela_slide(slide)

    def filtrar_lista_harpa(self, event=None):
        global lista_completa
        texto_harpa = self.view.controles['filtro_harpa_txt'].text().lower()
        filtrados = [f for f in lista_completa if texto_harpa in f.lower()]
        self.view.controles['arquivo_harpa_cb'].clear()
        self.view.controles['arquivo_harpa_cb'].addItems(filtrados)

        if filtrados:
            self.view.controles['arquivo_harpa_cb'].setCurrentIndex(0)

    def filtrar_lista_musicas(self, event=None):
        global lista_musicas
        texto_musicas = self.view.controles['filtro_musica_txt'].text().lower()
        filtrados = [f for f in lista_musicas if texto_musicas in f.lower()]
        self.view.controles['musica_cb'].clear()
        self.view.controles['musica_cb'].addItems(filtrados)
        if filtrados:
            self.view.controles['musica_cb'].setCurrentIndex(0)

    def carregar_arquivos_harpa(self):
        global lista_completa
        arquivos = os.listdir(dados.harpa_dir)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(dados.harpa_dir, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower()) # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        lista_completa = arquivos_sem_ext
        combo_arquivo = self.view.controles['arquivo_harpa_cb']
        combo_arquivo.clear()
        combo_arquivo.addItems(arquivos_sem_ext)

        if arquivos:
            self.view.controles['arquivo_harpa_cb'].setCurrentIndex(0)

    def selecionar_arquivo(self, janela):
        # Obtém o caminho dinâmico da pasta Documentos do usuário atual
        pasta_documentos = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )

        # Exibe a mensagem de aviso
        QMessageBox.information(
            janela, "Aviso", "Selecione o arquivo de texto .txt"
        )

        # Abre a caixa de diálogo iniciando na pasta Documentos
        arquivo, _ = QFileDialog.getOpenFileName(
            janela,
            "Selecione um arquivo de texto",
            pasta_documentos,  # Define o diretório inicial
            "Arquivos de texto (*.txt);;Todos os arquivos (*.*)",
        )

        if arquivo:
            shutil.copy(arquivo, config.MUSICAS_DIR)
            self.carregar_arquivos_musicas()

    def carregar_arquivos_musicas(self):
        global lista_musicas
        arquivos = os.listdir(config.MUSICAS_DIR)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(config.MUSICAS_DIR, f))]
        arquivos = sorted(arquivos, key=lambda x: str(x).lower())  # ordena ignorando maiúsculas/minúsculas
        arquivos_sem_ext = [os.path.splitext(f)[0] for f in arquivos]
        lista_musicas = arquivos_sem_ext
        self.view.controles['musica_cb'].clear()
        self.view.controles['musica_cb'].addItems(arquivos_sem_ext)
        self.view.controles['musica_cb'].setCurrentIndex(0)

    def localizar_arquivo(self):
        busca = self.view.controles['buscar_texto_cb'].currentText()
        if busca == "Bíblia":
            pasta_raiz = dados.biblia_dir
        elif busca == "Harpa":
            pasta_raiz = dados.harpa_dir
        else:
            pasta_raiz = config.MUSICAS_DIR

        # Normaliza e converte para minúsculas o termo pesquisado
        termo_busca = remover_acentos(self.view.controles['buscar_texto_txt'].text().lower())

        resultado = ""
        for raiz, pastas, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.endswith('.txt'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    try:
                        # Divisão de caminho multiplataforma
                        nome_arquivo = os.path.basename(caminho_completo)

                        with open(caminho_completo, 'r', encoding='utf-8') as f:
                            for numero_linha, linha in enumerate(f, 1):
                                # Normaliza a linha do arquivo para ignorar acentos e maiúsculas
                                linha_normalizada = remover_acentos(linha.lower())

                                if termo_busca in linha_normalizada:
                                    resultado += f" {nome_arquivo} -> Verso {math.ceil(numero_linha / 3)} -> {linha.strip()}\n"
                    except Exception as e:
                        caminho_erro = gerar_arquivo_log()
                        registrar_log(caminho_erro, f"Erro ao ler o arquivo {caminho_completo}: {e}")

        self.view.controles['text_area'].setText(resultado.replace(".txt", ""))

    def fechar_janelas(self, janela):
        global janela_logs_aberta

        match janela:
            case 'janela_principal':
                if janela_logs_aberta:
                    return
        try:
            self.view.controles[f'{janela}'].destroy()
        except Exception:
            pass

    def visitar_site(self=None):
        pagina = "https://github.com/YannickFigueira"

        # Instancia a caixa de mensagem do PyQt6
        msg_box = QMessageBox(self.view)
        msg_box.setWindowTitle("Sobre")
        msg_box.setText(
            f"<b>{config.NOME_PROGRAMA} {config.VERSION}</b><br>"
            f"Desenvolvedor: YannickFigueira<br>"
            f"chronostimeinchain@gmail.com<br><br>"
            f"Deseja visitar a página?"
        )
        msg_box.setIcon(QMessageBox.Icon.Information)

        # Configura os botões em português
        btn_sim = msg_box.addButton("Sim", QMessageBox.ButtonRole.YesRole)
        btn_nao = msg_box.addButton("Não", QMessageBox.ButtonRole.NoRole)

        msg_box.setDefaultButton(btn_sim)
        msg_box.exec()

        # Verifica qual botão foi clicado
        if msg_box.clickedButton() == btn_sim:
            # Abre a URL (usando QDesktopServices ou webbrowser.open)
            QDesktopServices.openUrl(QUrl(pagina))