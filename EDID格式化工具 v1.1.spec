# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['edid_format.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtCore'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='EDID格式化工具 v1.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\px1903\\Desktop\\自製工具\\EDIDFormater\\q3.ico'],
)
