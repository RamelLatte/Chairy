
from .Configuration import Configuration, ConfigurationError
from .NeisData      import NeisData, NeisError
from .StudentData   import StudentData
from .RoomData      import RoomData
from .DailyStatistics import DailyStatistics
from .MonthlyStatistics import MonthlyStatistics
from .PeriodStatistics import PeriodStatistics
from .MediaInfo import MediaInfo



__all__ = ['Configuration', 'ConfigurationError',
           'NeisData', 'NeisError',
           'StudentData', 'RoomData',
           'ChairyData',
           'DailyStatistics', 'MonthlyStatistics', 'PeriodStatistics',
           'MediaInfo']



from datetime import datetime, time, timedelta
from ..Logging import LoggingManager as logging



class ChairyData:
    """ 다양한 형태의 데이터를 저장하고 관리하는 클래스. """

    LOADPROGRESS    : int = 0
    MAX_PROGRESS    : int = 5
    CURRENT_PROGRESS: str = 'Chairy 시작 중'
    
    Ready: bool = False

    _Dir            : str

    DATETIME        : datetime      = None

    RESTART_AT      : datetime      = None

    CONFIGURATION   : Configuration = None
    NEISDATA        : NeisData      = None

    ROOMDATA        : RoomData      = None

    STUDENTS        : dict          = None
    CURRENT_STUDENT : StudentData   = None

    CURRENT_MEDIA   : MediaInfo     = None

    _min : int = -1
    _hou : int = -1
    _day : int = -1



    @staticmethod
    def Progress(desc: str):
        ChairyData.CURRENT_PROGRESS = desc
        ChairyData.LOADPROGRESS += 1


    @staticmethod
    def Init():
        """
        다양한 데이터를 불러오고, ChairyData 클래스를 준비한다.

        **실행 전 미리 ChairyData._Dir의 값을 지정해야 함!**
        """

        # 시간
        ChairyData.DATETIME = datetime.now()
        ChairyData._min = ChairyData.DATETIME.minute
        ChairyData._hou = ChairyData.DATETIME.hour
        ChairyData._day = ChairyData.DATETIME.day

        # Configuration
        ChairyData.Progress('구성 데이터를 불러오는 중') # 1
        logging.info("구성 데이터(configuration.xlsx)를 불러오는 중...")

        try:
            ChairyData.CONFIGURATION = Configuration(ChairyData._Dir)
            
            logging.info("자리 " + str(len(ChairyData.CONFIGURATION.Arrangement)) + "석의 배치 데이터 불러옴.")
            logging.info("등록된 이용자 " + str(len(ChairyData.CONFIGURATION.Students)) + "명.")
        except Exception as e:
            logging.error("구성 데이터(configuration.xlsx)를 읽는 도중에 오류가 발생하였습니다.", e, True)
            return
        

        # NEIS
        ChairyData.Progress('NEIS와 동기화 중') # 2
        ChairyData.NEISDATA = None

        try:
            ChairyData.NEISDATA     = NeisData(ChairyData.CONFIGURATION.NeisOpenApiKey, 
                                               ChairyData.CONFIGURATION.NeisOfficeCode, 
                                               ChairyData.CONFIGURATION.NeisSchoolCode, 
                                               ChairyData.CONFIGURATION.NeisTargetGrade,
                                               ChairyData.CONFIGURATION.NeisCanIgnoreSSL)
        except Exception as e:
            logging.error("NEIS API와 연동을 준비하는 중에 오류가 발생하였습니다.", e, True)
            return

        if ChairyData.NEISDATA != None:
            ChairyData.NEISDATA.update()

        # StudentData
        ChairyData.Progress('학생 정보를 불러오는 중') # 3
        logging.info("학생 정보를 불러오는 중...")

        StudentData.CONFIG      = ChairyData.CONFIGURATION
        StudentData.DIRECTORY   = ChairyData._Dir

        ChairyData.STUDENTS = {}

        CurrentID = "알 수 없음"
        try:
            Created = 0
            for i in ChairyData.CONFIGURATION.StudentIDs:
                CurrentID = i
                sd = StudentData(i)
                ChairyData.STUDENTS[i] = sd
                if sd.Created:
                    Created += 1

            if Created > 0:
                logging.info(str(Created) + "명의 학생 데이터가 새로 생성됨.")

            ChairyData.Progress('입실 데이터를 불러오는 중') # 4

            # RoomData
            ChairyData.ROOMDATA = RoomData.Init(ChairyData.CONFIGURATION, ChairyData._Dir)
            for key, value in ChairyData.ROOMDATA.Current.items():
                if value[1] != None and value[1] in ChairyData.STUDENTS and 'VAC' not in value[0]:
                        ChairyData.STUDENTS[value[1]].CurrentSeat = str(key)

        except Exception as e:
            logging.error("[" + CurrentID + "] 학번의 데이터를 처리하는 도중 오류가 발생했습니다.", e, True)
            return

        ChairyData.Progress('인터페이스를 불러오는 중') # 5

        # 이외 Class Init
        ChairyData.CURRENT_MEDIA = MediaInfo()
        ChairyData.CURRENT_MEDIA.UseMediaDetection = ChairyData.CONFIGURATION.MediaDetection

        # 준비 완료 표시
        ChairyData.Ready = True

        # 재설정 시각 지정
        ChairyData.RESTART_AT = datetime.combine(ChairyData.ROOMDATA.DATA_DATE + timedelta(days=1), time(5, 0, 0))


    @staticmethod
    def Restart():
        """
        재시작 시 호출되는 메서드
        """

        ChairyData.Ready = False
        ChairyData.LOADPROGRESS = 0
        logging.info("데이터 재설정 진행 중...")

        # 재설정 시각 지정
        ChairyData.RESTART_AT += timedelta(days=1)

        # 시간
        ChairyData.DATETIME = datetime.now()
        ChairyData._min = ChairyData.DATETIME.minute
        ChairyData._hou = ChairyData.DATETIME.hour
        ChairyData._day = ChairyData.DATETIME.day

        # Configuration
        ChairyData.Progress('재설정 중...(configuration.xlsx)') # 1
        logging.info("구성 데이터(configuration.xlsx)를 불러오는 중...")

        try:
            ChairyData.CONFIGURATION.Init()
            
            logging.info("자리 " + str(len(ChairyData.CONFIGURATION.Arrangement)) + "석의 배치 데이터 불러옴.")
            logging.info("등록된 이용자 " + str(len(ChairyData.CONFIGURATION.Students)) + "명.")
        except Exception as e:
            logging.error("구성 데이터(configuration.xlsx)를 읽는 도중에 오류가 발생하였습니다.", e, True)
            return
        

        # NEIS
        ChairyData.Progress('재설정 중...(NEIS)') # 2
        if ChairyData.NEISDATA != None:
            ChairyData.NEISDATA.update()

        # StudentData
        ChairyData.Progress('재설정 중...(학생 정보)') # 3
        logging.info("학생 정보를 불러오는 중...")

        ChairyData.STUDENTS = {}

        CurrentID = "알 수 없음"
        try:
            Created = 0
            for i in ChairyData.CONFIGURATION.StudentIDs:
                CurrentID = i
                sd = StudentData(i)
                ChairyData.STUDENTS[i] = sd
                if sd.Created:
                    Created += 1

            if Created > 0:
                logging.info(str(Created) + "명의 학생 데이터가 새로 생성됨.")

            ChairyData.Progress('재설정 중...(입실 데이터)') # 4

            # RoomData
            ChairyData.ROOMDATA = RoomData.Init(ChairyData.CONFIGURATION, ChairyData._Dir)
            for key, value in ChairyData.ROOMDATA.Current.items():
                if value[1] != None and value[1] in ChairyData.STUDENTS and 'VAC' not in value[0]:
                        ChairyData.STUDENTS[value[1]].CurrentSeat = str(key)

        except Exception as e:
            logging.error("[" + CurrentID + "] 학번의 데이터를 처리하는 도중 오류가 발생했습니다.", e, True)
            return

        ChairyData.Progress('데이터 재설정 완료') # 5
        logging.info("데이터 재설정 완료")

        # 준비 완료 표시
        ChairyData.Ready = True