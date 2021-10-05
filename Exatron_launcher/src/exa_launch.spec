# -*- mode: python -*-

block_cipher = None
here = os.path.dirname(os.path.abspath(os.getcwd()))


a = Analysis(['exa_launch.py'],
             pathex=[os.path.join(here,"src")],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          icon = 'mchp.ico',
          name='exa_launch',
          debug=False,
          strip=False,
          upx=False,
          console=False)
