# estilo.py
import os
from pathlib import Path

# Versão e repositório
VERSION = "v0.7.5"
REPO= "ProgramaIgreja"
NOME_PROGRAMA = "Programa Igreja Slides"


# Pastas do programa
home_programa_dir = "programaigreja"
home_dir = os.path.expanduser('~')
programa_dir = f"{home_dir}/.{home_programa_dir}"
notas = f"{home_dir}/.{home_programa_dir}/notas"
log_files = Path(f"{home_dir}/.{home_programa_dir}/logs")
log_files_erros = Path(f"{home_dir}/.{home_programa_dir}/erros")
musicas_dir = f"{home_dir}/.{home_programa_dir}/musicas"

if not os.path.exists(programa_dir):
    os.mkdir(programa_dir)
if not os.path.exists(notas):
    os.mkdir(notas)
if not os.path.exists(log_files):
    os.mkdir(log_files)
if not os.path.exists(log_files_erros):
    os.mkdir(log_files_erros)
if not os.path.exists(musicas_dir):
    os.mkdir(musicas_dir)

# Margens padrão para janelas e frames
# Medidas
ESPACO = 5
LINHA_PAINEL_ESQUERDO = 0

# Margens padrão para janelas e frames
PADX_JANELA = 20
PADY_JANELA = 20

# Margens padrão para componentes menores (botões, inputs, labels)
PADX_COMPONENTE = 10
PADY_COMPONENTE = 5

# Arquivo de log
ARQUIVO_ERRO = "copiar_arquivos.log"

# Estilo
FONTE_VAZIA=("", 14, "normal")
FONTE_ARIAL=("Arial", 11, "normal")

# Variáveis gerais
# Preencher pastas
TODAS_PASTAS = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', 'Samuel, I',
                     'Samuel, II', 'Reis, I', 'Reis, II', 'Crônicas, I', 'Crônicas, II', 'Esdras', 'Neemias', 'Ester',
                     'Jó', 'Salmos', 'Provérbios', 'Eclesiastes', 'Cânticos', 'Isaías', 'Jeremias', 'Lamentações',
                     'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Obadias', 'Jonas', 'Miquéias', 'Naum',
                     'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias', 'Mateus', 'Marcos', 'Lucas', 'João',
                     'Atos', 'Romanos', 'Corintios, I', 'Corintios, II', 'Gálatas', 'Efésios', 'Filipenses',
                     'Colossenses', 'Tessalonicenses, I', 'Tessalonicenses, II', 'Timóteo, I', 'Timóteo, II', 'Tito',
                     'Filemom', 'Hebreus', 'Tiago', 'Pedro, I', 'Pedro, II', 'João, I', 'João, II', 'João, III',
                     'Judas', 'Apocalipse']

LISTA_COMPLETA = []
LISTA_MUSICAS = []
# Fontes
FUNDO_COR = "#2E8B57" # cor do fundo
