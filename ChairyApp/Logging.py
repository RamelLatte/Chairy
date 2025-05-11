
import logging
from datetime import datetime
from traceback import format_exception
from os import mkdir
from os.path import exists



class LoggingManager:
    """
    ### LoggingManager

    소프트웨어의 구동 기록을 기록하고, 오류와 경고를 처리함.
    """

    LOGGER      : logging.Logger    = logging.getLogger()
    LOG_FILE_NM : str               = ""
    DIRECTORY   : str               = ""

    PROBLEMS    : list[list]        = []



    @staticmethod
    def Init(dir: str):
        """ LoggingManager 초기화 """
        LoggingManager.DIRECTORY = dir

        # 로그의 레벨
        LoggingManager.LOGGER.setLevel(logging.INFO)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s >> %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        LoggingManager.LOGGER.addHandler(stream_handler)

        # log를 파일에 출력
        LoggingManager.LOG_FILE_NM = "log/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".log"
        if not exists(LoggingManager.DIRECTORY + "/log"):
            mkdir(LoggingManager.DIRECTORY + "/log/")
        file_handler = logging.FileHandler(LoggingManager.DIRECTORY + "/" + LoggingManager.LOG_FILE_NM)
        file_handler.setFormatter(formatter)
        LoggingManager.LOGGER.addHandler(file_handler)


    @staticmethod
    def info(msg: str, exception: Exception = None):
        """
        일반 메시지 출력
        - - -
        #### 매개변수:
        - **msg:** 메시지
        - **exception:** 추가로 출력할 예외, 기본값은 None이며 이땐 Traceback을 출력하지 않음.
        """

        LoggingManager.LOGGER.info(msg)
        if exception is not None:
            LoggingManager.LOGGER.error('자세한 오류 내용 (Traceback):\n' + ''.join(format_exception(type(exception), exception, exception.__traceback__)))


    @staticmethod
    def warning(msg: str, exception: Exception = None, block: bool = False):
        """
        경고 메시지를 출력하고 PROBLEMS 리스트에 예외(있으면) 기록을 추가함.
        - - -
        #### 매개변수:
        - **msg:** 메시지
        - **exception:** 추가로 출력할 예외, 기본값은 None이며 이땐 Traceback을 출력하지 않음.
        - **block:** ErrorDialog를 띄울지 여부
        """

        if block:
            LoggingManager.PROBLEMS.append([False, msg, str(exception), False])

        LoggingManager.LOGGER.warning(msg)
        if exception is not None:
            LoggingManager.LOGGER.error('자세한 오류 내용 (Traceback):\n' + ''.join(format_exception(type(exception), exception, exception.__traceback__)))


    @staticmethod
    def error(msg: str, exception: Exception = None, fatal: bool = False, block: bool = False):
        """
        오류 메시지 출력하고 PROBLEMS 리스트에 예외(있으면) 기록을 추가함.
        - - -
        #### 매개변수:
        - **msg:** 메시지
        - **exception:** 추가로 출력할 예외, 기본값은 None이며 이땐 Traceback을 출력하지 않음.
        - **fatal:** 치명적인지 여부, True인 경우는 프로그램을 더 이상 실행할 수 없는 경우임.
        - **block:** ErrorDialog를 띄울지 여부, **fatal 값이 True이면 block 값과 관계없이 ErrorDialog를 띄움.**
        """

        if block or fatal:
            LoggingManager.PROBLEMS.append([True, msg, str(exception), fatal])

        LoggingManager.LOGGER.error(msg)
        if exception is not None:
            LoggingManager.LOGGER.error('자세한 오류 내용 (Traceback):\n' + ''.join(format_exception(type(exception), exception, exception.__traceback__)))

    
    @staticmethod
    def popProblem() -> list:
        """
        PROBLEMS로부터 맨 먼저 일어난 예외 기록을 꺼냄.
        """
        return LoggingManager.PROBLEMS.pop(0)
    

    @staticmethod
    def hasProblem() -> bool:
        """
        PROBLEMS 리스트에 예외 기록이 있는지 여부를 반환함.
        """
        return len(LoggingManager.PROBLEMS) > 0