# programaigreja.spec
block_cipher = None

a = Analysis(
    ['programaigreja.py'],   # arquivo principal
    pathex=[],
    binaries=[],
    datas=[
        ('HarpaTexto', 'HarpaTexto'),
        ('Biblia', 'Biblia'),
    ],
    hiddenimports=['dados', 'slide', 'verificarversao', 'requests', 'urllib3', 'chardet', 'idna', 'certifi', 'screeninfo'],  # módulos auxiliares
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='programaigreja',
    debug=False,
    strip=False,
    upx=True,
    console=False,  # sem janela de prompt
)

