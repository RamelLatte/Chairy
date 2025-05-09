
# Pyinstaller 빌드 명령어:
#
# pyinstaller --noupx --onedir --icon=Icon.ico Chairy.pyw --hidden-import=winrt.windows.media --hidden-import=winrt.windows.foundation --hidden-import=winrt.windows.foundation.collections --hidden-import=winrt.windows.storage --hidden-import=winrt.windows.storage.streams
# 


if __name__ == '__main__':

    from ChairyApp.ChairyApp import ChairyApp
    from os import path

    ChairyApp.Init(path.abspath(path.dirname(__file__)))