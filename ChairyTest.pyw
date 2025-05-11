
# Pyinstaller 빌드 명령어:
#
# pyinstaller --noupx --onedir --icon=Icon.ico Chairy.pyw --hidden-import=winrt.windows.media --hidden-import=winrt.windows.foundation --hidden-import=winrt.windows.foundation.collections --hidden-import=winrt.windows.storage --hidden-import=winrt.windows.storage.streams
# 

### 지금 쓰고 있는 라이브러리 ####
# 
#  - pygame   : GUI 및 상호작용
#  - pyopenxl : 통계 자료 관리
#  - requests : NEIS 연동용 API 호출
#
# ■ 미디어 재생 현황 확인 기능에 쓰이는 라이브러리는 다음과 같음.
#  - winrt-Windows.media
#  - winrt-Windows.media.control
#  - winrt-Windows.foundation
#  - winrt-Windows.foundation.collections
#  - winrt-Windows.storage
#  - winrt-Windows.storage.streams
# ■ 진짜 이 위의 5개 일일이 pip install 해야함.
#  -> 그래서 PyInstaller로 만들어두는게 실사용 환경을 고려하면 매우 좋음.
#  -> 번거롭게 파이썬 깔고, 라이브러리 하나하나 보고 입력하지 않아도 됨.
#
###



if __name__ == '__main__':

    from ChairyApp.ChairyApp import ChairyApp
    from os import path

    ChairyApp.Init(path.abspath(path.dirname(__file__)))