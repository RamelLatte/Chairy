
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



from datetime import datetime
from ..Logging import LoggingManager as logging



class ChairyData:
    """ 다양한 형태의 데이터를 저장하고 관리하는 클래스. """

    LOADPROGRESS    : int = 0
    MAX_PROGRESS    : int = 5

    _Dir            : str

    DATETIME        : datetime      = None

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
    def Init(directory: str):
        """
        다양한 데이터를 불러오고, ChairyData 클래스를 준비한다.
        - - -
        #### 매개변수:
        - **directory:** 실행 파일이 존재하는 디렉토리 위치
        """

        ChairyData._Dir     = directory

        # 시간

        ChairyData.DATETIME = datetime.now()
        ChairyData._min = ChairyData.DATETIME.minute
        ChairyData._hou = ChairyData.DATETIME.hour
        ChairyData._day = ChairyData.DATETIME.day

        # Configuration
        logging.info("구성 데이터(configuration.xlsx)를 불러오는 중...")

        try:
            ChairyData.CONFIGURATION = Configuration(ChairyData._Dir)
            
            logging.info("자리 " + str(len(ChairyData.CONFIGURATION.Arrangement)) + "석의 배치 데이터 불러옴.")
            logging.info("등록된 이용자 " + str(len(ChairyData.CONFIGURATION.Students)) + "명.")
        except Exception as e:
            logging.error("구성 데이터(configuration.xlsx)를 읽는 도중에 오류가 발생하였습니다.", e, True)
            return

        ChairyData.LOADPROGRESS += 1 # 1

        # NEIS
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

        ChairyData.LOADPROGRESS += 1 # 2

        # StudentData
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

            ChairyData.LOADPROGRESS += 1 # 3

            # RoomData
            ChairyData.ROOMDATA = RoomData.Init(ChairyData.CONFIGURATION, ChairyData._Dir)
            for key, value in ChairyData.ROOMDATA.Current.items():
                if value[1] != None and value[1] in ChairyData.STUDENTS and 'VAC' not in value[0]:
                        ChairyData.STUDENTS[value[1]].CurrentSeat = str(key)

            ChairyData.LOADPROGRESS += 1 # 4

        except Exception as e:
            logging.error("[" + CurrentID + "] 학번의 데이터를 처리하는 도중 오류가 발생했습니다.", e, True)
            return

        ChairyData.LOADPROGRESS += 1 # 5

        # 이외 Class Init
        ChairyData.CURRENT_MEDIA = MediaInfo()
        ChairyData.CURRENT_MEDIA.UseMediaDetection = ChairyData.CONFIGURATION.MediaDetection