
from . import Configuration, StudentData
from datetime import datetime, timedelta, time, date
from ..Info import ChairyInfo as CI



class RoomData():
    """
    ### 좌석 데이터

    좌석별로 현재 이용 중인 학생의 학번과 이름을 저장하고, 입퇴실과 이동 기록을 저장함.
    통계 4종을 내보내고 조회할 때 필요하며, 당시의 좌석 배치가 같이 저장됨.
    
    **매일 오전 5시에 자동으로 초기화되도록 프로그램이 설계되었으며. JSON으로 저장되고 불러와짐.**
    """

    __slots__ = ('DIRECTORY', 'CONFIG', 'DIRNAME', 'FILENAME', 'DATA_DATE', 'DATA', 'Current', 'Arrangement', 'UserNames', 'Begin', 'End', 'Version', 'Logs')


    # Static
    DIRECTORY   : str
    CONFIG      : Configuration
    DIRNAME: str # 폴더 이름
    FILENAME: str # 파일 이름
    DATA_DATE: date # 현재 RoomData 날짜

    DATA: type['RoomData']
    #

    Current     : dict[list[str]] # 현재 좌석 현황
    Arrangement : list # 좌석 배치
    UserNames   : list # 입실한 사용자 학번

    Begin   : time # 기록 시작 시각
    End     : time # 기록 종료 시각
    Version   : str # 기록한 Chairy 소프트웨어 버전

    Logs: list[dict] # 입퇴실, 이동 기록



    def __init__(self):

        self.Current = {}
        self.Arrangement = RoomData.CONFIG.Arrangement
        self.UserNames = []
        self.Logs = []

        self.Begin = datetime.now().time()
        self.End = None
        self.Version = CI.Version

        # 좌석 현황 초기화
        for a in RoomData.CONFIG.Arrangement:
            self.Current[a[0]] = ['VAC_FRE', None, None]

        # 지정석 미리 지정
        if RoomData._holiday():
            # 오늘 휴일인데 지정석을 시행하도록 설정했으면
            if RoomData.CONFIG.ReservedSeatInHoliday:
                for i in self.CONFIG.Students:
                    
                    if i[2] != None:
                        self.Current[i[2]] = ['VAC_RES', i[0], i[1]]
        else:
            # 휴일이 아니면 무조건 지정석 시행
            for i in self.CONFIG.Students:
                    
                if i[2] != None:
                    self.Current[i[2]] = ['VAC_RES', i[0], i[1]]

        RoomData.DATA = self


    def isReserved(self, seat: str) -> bool:
        """
        해당 좌석의 지정석 여부
        - - -
        #### 매개변수:
        - **seat:** 좌석
        """
        return "RES" in self.Current[seat][0]
    

    def isVacant(self, seat: str) -> bool:
        """
        해당 좌석의 빈 좌석 여부
        - - -
        #### 매개변수:
        - **seat:** 좌석
        """
        return "VAC" in self.Current[seat][0]
    

    def getStudent(self, seat: str) -> str:
        """
        해당 좌석을 이용 중인 학생의 학번 반환
        - - -
        #### 매개변수:
        - **seat:** 좌석
        """
        return self.Current[seat][1]
    

    def getStudentName(self, seat: str) -> str:
        """
        해당 좌석을 이용 중인 학생의 이름 반환
        - - -
        #### 매개변수:
        - **seat:** 좌석
        """
        return self.Current[seat][2]
            

    def CheckIn(self, student: StudentData, seat: str):
        """
        입실 처리 및 기록 추가
        - - -
        #### 매개변수:
        - **student:** 입실한 학생의 StudentData
        - **seat:** 입실 좌석
        """
        now = datetime.now()

        self.Logs.append({'TimeStamp': now.strftime('%Y%m%d%H%M%S.%f'), 'ID': student.StudentID, 'Name': student.Name, 'Action': 'ChkIn', 'Seat': seat})

        date = self.DATA_DATE.strftime('%Y%m%d')
        time = float(now.strftime('%H%M%S.%f'))

        if date in student.Activity:
            if student.Activity[date][0] != None:
                if float(student.Activity[date][0]) > time:
                    student.Activity[date][0] = now.strftime('%Y%m%d%H%M%S.%f')
            else:
                student.Activity[date][0] = now.strftime('%Y%m%d%H%M%S.%f')
        else:
            student.Activity[date] = [now.strftime('%Y%m%d%H%M%S.%f'), None, "", 0]

        student.Activity[date][2] = seat

        student.CurrentSeat = seat

        student.WeeklyCheckInStamp[RoomData.DATA_DATE.weekday()] = True

        if student.Name not in self.UserNames:
            self.UserNames.append(student.Name)

        self.Current[seat] = ['OCC_FRE', student.StudentID, student.Name]

        self.Save()
    

    def CheckInReserved(self, student: StudentData):
        """
        지정석 입실 처리 및 기록 추가
        - - -
        #### 매개변수:
        - **student:** 입실한 학생의 StudentData
        - 지정석이 있는 학생은 StudentData에 지정석 번호가 저장되어 있어 **seat는 매개변수로 투입할 필요가 없음.**
        """

        if student.SeatReserved:
            now = datetime.now()

            self.Logs.append({'TimeStamp': now.strftime('%Y%m%d%H%M%S.%f'), 'ID': student.StudentID, 'Name': student.Name, 'Action': 'ChkIn', 'Seat': student.ReservedSeat, 'Comment':'Reserved'})

            date = self.DATA_DATE.strftime('%Y%m%d')
            time = float(now.strftime('%Y%m%d%H%M%S.%f'))

            if date in student.Activity:
                if student.Activity[date][0] != None:
                    if float(student.Activity[date][0]) > time:
                        student.Activity[date][0] = now.strftime('%Y%m%d%H%M%S.%f')
                else:
                    student.Activity[date][0] = now.strftime('%Y%m%d%H%M%S.%f')
            else:
                student.Activity[date] = [now.strftime('%Y%m%d%H%M%S.%f'), None, "", 0]

            student.Activity[date][2] = student.ReservedSeat

            student.CurrentSeat = student.ReservedSeat

            student.WeeklyCheckInStamp[RoomData.DATA_DATE.weekday()] = True

            if student.Name not in self.UserNames:
                self.UserNames.append(student.Name)

            self.Current[student.ReservedSeat] = ['OCC_RES', student.StudentID, student.Name]

        self.Save()


    def CheckOut(self, student: StudentData):
        """
        퇴실 처리 및 기록 추가
        - - -
        #### 매개변수:
        - **student:** 퇴실한 학생의 StudentData
        """

        now = datetime.now()

        self.Logs.append({'TimeStamp': now.strftime('%Y%m%d%H%M%S.%f'), 'ID': student.StudentID, 'Name': student.Name, 'Action': 'ChkOut', 'Seat': student.CurrentSeat})

        date = self.DATA_DATE.strftime('%Y%m%d')
        time = float(now.strftime('%Y%m%d%H%M%S.%f'))

        if date in student.Activity:
            if student.Activity[date][1] != None:
                if float(student.Activity[date][1]) < time:
                    student.Activity[date][1] = now.strftime('%Y%m%d%H%M%S.%f')
                else:
                    student.Activity[date][1] = now.strftime('%Y%m%d%H%M%S.%f')
            else:
                student.Activity[date][1] = now.strftime('%Y%m%d%H%M%S.%f')

        if not student.SeatReserved:
            self.Current[student.CurrentSeat] = ['VAC_FRE', None, None]
        else:
            self.Current[student.CurrentSeat] = ['VAC_RES', student.StudentID, student.Name]

        student.CurrentSeat = None

        self.Save()


    def Move(self, student: StudentData, seatTo: str):
        """
        이동 처리 및 기록 추가
        - - -
        #### 매개변수:
        - **student:** 퇴실한 학생의 StudentData
        - **seatTo:** 이동한 좌석 번호
        """

        now = datetime.now()

        self.Logs.append({'TimeStamp': now.strftime('%Y%m%d%H%M%S.%f'), 'ID': student.StudentID, 'Name': student.Name, 'Action': 'Move', 'From': student.CurrentSeat, 'Seat': seatTo})

        date = self.DATA_DATE.strftime('%Y%m%d')
        student.Activity[date][2] = seatTo

        student.Activity[date][3] += 1

        if not student.SeatReserved:
            self.Current[student.CurrentSeat] = ['VAC_FRE', None, None]

            self.Current[seatTo] = ['OCC_FRE', student.StudentID, student.Name]

        student.CurrentSeat = seatTo

        self.Save()

        
    def ToRaw(self):
        """
        JSON으로 내보낼 수 있도록 딕셔너리로 감싸 반환함.
        """

        return {

            'Begin': self.Begin.strftime('%Y%m%d%H%M%S.%f'),
            'End': datetime.now().strftime('%Y%m%d%H%M%S.%f'),
            'Version': self.Version,
            
            'Users': self.UserNames,
            'Current': self.Current,
            'Arrangement': self.Arrangement,

            'Logs': self.Logs

        }
    

    @staticmethod
    def FromRaw(raw: dict):
        """
        JSON에서 받아온 딕셔너리 값을 언팩하여 RoomData 클래스를 복원함.
        """
        data = RoomData()

        data.Begin = datetime.strptime(raw['Begin'], '%Y%m%d%H%M%S.%f').time()
        data.End = datetime.strptime(raw['Begin'], '%Y%m%d%H%M%S.%f').time()
        data.Version = raw['Version']

        data.UserNames = raw['Users']
        data.Current = raw['Current']
        data.Arrangement = raw['Arrangement']
        data.Logs = raw['Logs']

        return data
    

    def Save(self):
        """
        RoomData를 JSON 형식의 파일로 저장함.
        """
        import orjson, os
        if not os.path.exists(RoomData.DIRECTORY + '/RoomData/' + RoomData.DIRNAME + '/'):
            os.makedirs(RoomData.DIRECTORY + '/RoomData/' + RoomData.DIRNAME + '/')
        with open(RoomData.DIRECTORY + '/RoomData/' + RoomData.DIRNAME + '/' + RoomData.FILENAME, 'w', encoding='utf-8') as f:
            f.write(orjson.dumps(self.ToRaw()).decode('utf-8'))

    
    @staticmethod
    def Init(config: Configuration, DIR: str):
        """
        RoomData 사용을 위한 초기화 과정
        - - -
        #### 매개변수:
        - **config:** ChairyData.CONFIGURATION을 그대로 투입해야 함.
        - **DIR:** ChairyData._Dir을 그대로 투입해야 함.
        """

        now = datetime.now()

        if now.hour < 5:
            now -= timedelta(days=1)

        RoomData.DATA_DATE = now.date()

        RoomData.DIRNAME = now.strftime("%Y%m")
        RoomData.FILENAME = now.strftime("%Y%m%d.json")

        RoomData.DIRECTORY  = DIR
        RoomData.CONFIG     = config
        from os.path import exists

        if not exists(DIR + '/RoomData/' + RoomData.DIRNAME + '/' + RoomData.FILENAME):
            return RoomData()
        
        else:
            import orjson

            s: str = ""
            with open(DIR + '/RoomData/' + RoomData.DIRNAME + '/' + RoomData.FILENAME, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    s += line
            return RoomData.FromRaw(orjson.loads(s))
                
    
    @staticmethod
    def Load(date: date) -> type['RoomData']:
        """
        특정 일자의 RoomData를 불러옴. 없으면 None을 반환함.
        - - -
        #### 매개변수:
        - **data:** 불러올 날짜
        """
        from os.path import exists

        fn = date.strftime('%Y%m/%Y%m%d.json')

        if not exists(RoomData.DIRECTORY + '/RoomData/' + fn):
            return None
        
        else:
            import orjson
            s : str = ""
            with open(RoomData.DIRECTORY + '/RoomData/' + fn, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    s += line
            return RoomData.FromRaw(orjson.loads(s))
                

    @staticmethod
    def _holiday():
        """ 휴일 여부, 주말이거나 Neis에서 오늘 학사 일정이 공휴일이거나 휴업일이면 True를 반환, 그 외는 False를 반환함. """
        from . import ChairyData as CD

        return (RoomData.DATA_DATE.weekday() >= 5 or CD.NEISDATA.Holiday)
    

    @staticmethod
    def TodayReservedSeat() -> bool:
        """ 오늘 지정석을 시행하는 날인지 여부를 반환. """
        return (RoomData.DATA_DATE.weekday() >= 5 or RoomData._holiday()) and RoomData.CONFIG.ReservedSeatInHoliday