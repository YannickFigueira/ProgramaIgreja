from pathlib import Path

# --- Metadados e Versão ---
VERSION = "v0.8.6"
REPO = "ProgramaIgreja"
NOME_PROGRAMA = "Programa Igreja Slides"

# --- Diretos e Caminhos ---
HOME_DIR = Path.home()
PROGRAMA_DIR = HOME_DIR / ".programaigreja"
NOTAS_DIR = PROGRAMA_DIR / "notas"
LOG_FILES_DIR = PROGRAMA_DIR / "logs"
LOG_ERRORS_DIR = PROGRAMA_DIR / "erros"
MUSICAS_DIR = PROGRAMA_DIR / "musicas"

def garantir_diretorios():
    """Garante que a estrutura de pastas do sistema exista."""
    for pasta in [PROGRAMA_DIR, NOTAS_DIR, LOG_FILES_DIR, LOG_ERRORS_DIR, MUSICAS_DIR]:
        pasta.mkdir(parents=True, exist_ok=True)

# Executa ao importar ou chama explicitamente no main.py
garantir_diretorios()

# --- Constantes Visuais e Layout ---
ESPACO = 5
PADX_JANELA = 20
PADY_JANELA = 20
PADX_COMPONENTE = 10
PADY_COMPONENTE = 5
FUNDO_COR = "#2E8B57"

# --- Dados Estáticos ---
TODAS_PASTAS = [
    'Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', 'Samuel, I',
    'Samuel, II', 'Reis, I', 'Reis, II', 'Crônicas, I', 'Crônicas, II', 'Esdras', 'Neemias', 'Ester',
    'Jó', 'Salmos', 'Provérbios', 'Eclesiastes', 'Cânticos', 'Isaías', 'Jeremias', 'Lamentações',
    'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Obadias', 'Jonas', 'Miquéias', 'Naum',
    'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias', 'Mateus', 'Marcos', 'Lucas', 'João',
    'Atos', 'Romanos', 'Corintios, I', 'Corintios, II', 'Gálatas', 'Efésios', 'Filipenses',
    'Colossenses', 'Tessalonicenses, I', 'Tessalonicenses, II', 'Timóteo, I', 'Timóteo, II', 'Tito',
    'Filemom', 'Hebreus', 'Tiago', 'Pedro, I', 'Pedro, II', 'João, I', 'João, II', 'João, III',
    'Judas', 'Apocalipse'
]