
import requests
import orjson as json
from datetime import datetime, timedelta, timezone
from re import sub as ReSub
from ..Logging import LoggingManager as logging
from requests.exceptions import SSLError, ConnectionError, HTTPError, Timeout
from urllib3.exceptions import NameResolutionError, MaxRetryError
from socket import gaierror
from dataclasses import dataclass



SCHOOLINFO_URL      = "http://open.neis.go.kr/hub/schoolInfo"
SCHOOLSCHEDULE_URL  = "https://open.neis.go.kr/hub/SchoolSchedule"
DIETINFO_URL        = "https://open.neis.go.kr/hub/mealServiceDietInfo"

KST = timezone(timedelta(hours=9), 'Asia/Seoul')



class NeisError(Exception):

    CODE: str
    NEIS_MSG: str

    def __init__(self, code: str, neis_msg: str):
        self.CODE = code
        self.NEIS_MSG = neis_msg
        super().__init__(code + " -> " + neis_msg)



@dataclass(slots=True)
class NeisData():
    """
    ### 나이스 연동 데이터
    
    Neis Open API로부터 학교 정보, 식단 정보, 학사 일정을 받아와 필요한 형태로 다듬고 저장함.
    """


    # 설정
    CanIgnoreSSL: bool

    # 연동 정보
    KEY         : str   # 인증 코드
    OFFICE_CODE : str   # 시도교육청코드
    SCHOOL_CODE : str   # 학교 행정표준코드

    # 학교 정보
    OfficeName : str  # 시도교육청명
    SchoolName : str  # 학교명

    # 석식 식단
    Kcal: str   # 칼로리 정보 (kcal)
    Dish: list  # 식단명

    # 오늘 일정
    Events  : list[tuple[str]]
    Holiday : bool

    # 기타 변수
    DinnerDate      : datetime
    DinnerInfoDate  : str
    Today           : datetime
    TargetGrade     : int

    # 오류 코드
    ErrorCode   : str



    def __init__(self, key: str, office: str, school: str, targetGrade: int, canIgnoreSSL: bool):
        """
        ### 매개변수:
        - **key:** Neis Open API 키, Configuration.NeisOpenApiKey에 저장되어 있음.
        - **office:** 시도교육청코드, Configuration.NeisOfficeCode에 저장되어 있음.
        - **school:** 학교의 행정표준코드, Configuration.NeisSchoolCode에 저장되어 있음.
        - **targetGrade:** 대상 학년, Configuration.NeisTargetGrade에 저장되어 있음.
        - **canIgnoreSSL:** SSL 인증 무시 여부, Configuration.NeisCanIgnoreSSL에 저장되어 있음.

        - - -
        ### 추가 설명:
        일부 학교나 환경에 따라 Neis API에 접근할 때 SSL 인증이 안 되는 경우가 있는데, 그래서 SSL 인증 무시 여부를 넣어둔 것.
        /school_data/configuration.xlsx에서 전부 수정 가능함. 테스트 시에는 적절한 API 키가 입력되어 있어야 오류가 나지 않음.
        """

        self.CanIgnoreSSL   = canIgnoreSSL

        self.KEY            = key
        self.OFFICE_CODE    = office
        self.SCHOOL_CODE    = school

        self.TargetGrade = targetGrade

        self.OfficeName = ""
        self.SchoolName = ""

        self.DinnerDate = None
        self.DinnerInfoDate = "오늘"

        self.Events = []
        self.Holiday = False

        self.Kcal = ""
        self.Dish = []

        self.ErrorCode = None


    def _update(self, Verify: bool = True):
        """ 내부 사용 용도, update()에서 호출됨. """

        self.ErrorCode = None

        ## 학교 정보 획득 ##
        resp = requests.get(SCHOOLINFO_URL, params={

            'KEY'           : self.KEY,
            'Type'          : 'json',
            'pIndex'        : '1',
            'pSize'         : '5',
            'SD_SCHUL_CODE' : self.SCHOOL_CODE

        }, verify=Verify, timeout=15)

        res = json.loads(resp.text)

        if 'RESULT' in res:

            c = res['RESULT']['CODE']
            m = res['RESULT']['MESSAGE']

            if 'ERROR' in c or c == 'INFO-300' or c == 'INFO-200':
                self.ErrorCode = c
                raise NeisError(c, m)

        self.OfficeName = res['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_NM']
        self.SchoolName = res['schoolInfo'][1]['row'][0]['SCHUL_NM']

        resp.close()


        ## 날짜 연산 ##
        self.Today = datetime.now(KST)
        self.DinnerDate = self.Today
        self.DinnerInfoDate = "오늘"

        if self.Today.weekday() < 5:
            
            if self.Today.hour >= 18:
                self.DinnerDate += timedelta(days= 1)
                self.DinnerInfoDate = "내일"

        if self.DinnerDate.weekday() > 4:
            self.DinnerDate += timedelta(days= 7 - self.DinnerDate.weekday())
            self.DinnerInfoDate = "월요일"


        ## 학사 일정 ##
        resp = requests.get(SCHOOLSCHEDULE_URL, params={

            'KEY'               : self.KEY,
            'Type'              : 'json',
            'pIndex'            : '1',
            'pSize'             : '100',
            'ATPT_OFCDC_SC_CODE': self.OFFICE_CODE,
            'SD_SCHUL_CODE'     : self.SCHOOL_CODE,
            'AA_YMD'            : self.Today.strftime('%Y%m%d')

        }, verify=Verify, timeout=15)

        res = json.loads(resp.text)

        if 'RESULT' in res:

            c = res['RESULT']['CODE']
            m = res['RESULT']['MESSAGE']

            if 'ERROR' in c or c == 'INFO-300':
                self.ErrorCode = c
                raise NeisError(c, m)

        self.Events = []

        if 'SchoolSchedule' in res:
            for row in res['SchoolSchedule'][1]['row']:

                if self.TargetGrade == 3 and row['THREE_GRADE_EVENT_YN'] == 'Y':
                    self.Events.append((row['EVENT_NM'], row['SBTR_DD_SC_NM']))
                elif self.TargetGrade == 2 and row['TW_GRADE_EVENT_YN'] == 'Y':
                    self.Events.append((row['EVENT_NM'], row['SBTR_DD_SC_NM']))
                elif self.TargetGrade == 1 and row['ONE_GRADE_EVENT_YN'] == 'Y':
                    self.Events.append((row['EVENT_NM'], row['SBTR_DD_SC_NM']))

                if len(self.Events) > 2:
                    break


        self.Holiday = False
        for event in self.Events:
            if event[1] in ("공휴일", "휴업일"):
                self.Holiday = True

        resp.close()


        ## 석식 식단 ##
        resp = requests.get(DIETINFO_URL, params={

            'KEY'               : self.KEY,
            'Type'              : 'json',
            'pIndex'            : '1',
            'pSize'             : '100',
            'ATPT_OFCDC_SC_CODE': self.OFFICE_CODE,
            'SD_SCHUL_CODE'     : self.SCHOOL_CODE,
            'MLSV_YMD'          : self.DinnerDate.strftime('%Y%m%d')

        }, verify=Verify, timeout=15)

        res = json.loads(resp.text)

        if 'RESULT' in res:

            c = res['RESULT']['CODE']
            m = res['RESULT']['MESSAGE']

            if 'ERROR' in c or c == 'INFO-300':
                self.ErrorCode = c
                raise NeisError(c, m)
            
        self.Kcal = ""
        self.Dish = []
            
        if 'mealServiceDietInfo' in res:
            for row in res['mealServiceDietInfo'][1]['row']:

                if row['MMEAL_SC_NM'] == '석식':
                    self.Kcal = row['CAL_INFO']
                    self.Dish = [ReSub(r'\s*\(\d+(?:[.,]\d+)*\)', '', item) for item in str(row['DDISH_NM']).split("<br/>")]
                    break

        resp.close()


    def update(self) -> int:
        """
        Neis API로부터 데이터를 가져와서 NeisData를 갱신함.
        오류가 발생한 경우, 예외를 일으키며 ErrorCode의 값이 None에서 바뀜.

        - - -
        ### ErrorCode:
        - API 호출 도중에 오류가 발생한 경우, ErrorCode의 값은 'ApiError'로 기입됨.
        - Neis에서 오류 코드를 반환한 경우, 해당 오류 코드가 ErrorCode의 값으로 기입됨.

        예를 들어 Api Key를 잘못 입력하여 Neis에서 'ERROR-290' 코드를 반환하면, ErrorCode의 값도 None에서 'ERROR-290'이 됨.

        - - -
        ### 추가 설명:
        일부 학교나 환경에 따라 Neis API에 접근할 때 SSL 인증이 안 되는 경우가 있는데, 그래서 SSL 인증 무시 여부를 넣어둔 것.
        /school_data/configuration.xlsx에서 전부 수정 가능함. 테스트 시에는 적절한 API 키가 입력되어 있어야 오류가 나지 않음.
        """
        
        logging.info("NEIS API에서 정보를 가져옵니다...")

        try:
            self._update()
            logging.info("NEIS로부터 정보 갱신 완료")
            return 0 # 정상
        
        except NeisError as e:
            logging.warning("NEIS에서 오류를 보고했습니다.", e)
            self.ErrorCode = 'ApiError'
            return 1 # NeisError로 업데이트 불가
        
        except SSLError as e:
            if self.CanIgnoreSSL:
                logging.warning("SSL 인증 오류가 발생하여 인증 과정을 생략하였습니다. 이는 보안 상의 이유로 권장하지 않으며 설정 파일에서 해당 사항을 관리할 수 있습니다.", e)
                self._update(False)
                logging.info("NEIS로부터 정보 갱신 완료")
                return 2 # SSLError였지만 무시함
            else:
                logging.warning('SSL 인증 오류가 발생하여 NEIS와 연동되지 않았습니다. 인증을 무시해도 되는 경우, 설정 파일을 수정하여 무시하도록 설정합니다.', e)
                self.ErrorCode = 'ApiError'
                return 3 # SSLError로 인해 업데이트 불가
            
        except (NameResolutionError, ConnectionError, MaxRetryError, gaierror, HTTPError, Timeout) as e:
            logging.warning('NEIS API에 연결할 수 없습니다. 컴퓨터의 인터넷 연결 상태를 확인해주십시오.', e)
            self.ErrorCode = 'ApiError'
            return 4 # 인터넷 문제로 업데이트 불가
        
        except Exception as e:
            logging.warning('기타 오류로 인해 NEIS API에 연결할 수 없습니다.', e)
            self.ErrorCode = 'ApiError'
            return 5 # 기타 오류로 업데이트 불가