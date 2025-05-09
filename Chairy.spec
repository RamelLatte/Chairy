# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Chairy.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['winrt.windows.media', 'winrt.windows.foundation', 'winrt.windows.foundation.collections', 'winrt.windows.storage', 'winrt.windows.storage.streams'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Chairy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Chairy',
)
