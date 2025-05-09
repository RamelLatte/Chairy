
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

class ChairyInfo:
    """ ### Chairy 정보 """

    Version     : str = '1.0.0'
    """ 소프트웨어 버전 """