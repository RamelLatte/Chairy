
from . import Configuration
from datetime import datetime
from os import path
from . import RoomData
import json



class StudentData():
    """
    ### 학생별 데이터

    학번, 이름은 물론, 지정석과 주간 자습 참석 여부, 현재 좌석과 활동 기록을 저장하는 클래스.

    JSON으로 저장, 불러오기가 가능함.
    """

    @staticmethod
    def Init(config: Configuration, Directory: str):
        StudentData.CONFIG = config
        StudentData.DIRECTORY = Directory


    CONFIG      : Configuration     # Static
    DIRECTORY   : str               # Static

    Created : bool # 파일 새로 생겼는지 여부

    StudentID   : str # 학번
    Name        : str # 이름

    SeatReserved: bool # 지정석 여부
    ReservedSeat: str # 지정석 번호

    WeeklyCheckInStamp  : list[bool] # 주간 자습 참여 여부
    WeeklyCheckInStamp_ : int # 위에거 데이터가 몇주차인지 값
    """
    WeeklyCheckInStamp는 일주일마다 초기화되는데, 만약 주차가 같고 연도가 다른 경우 초기화가 안되는 버그가 있음.
    **근데 그 버그가 일어날 상황은 사실상 없기 때문에 무시해도 됨.**
    """

    CurrentSeat : str # 현재 쓰고 있는 좌석 번호

    Activity: dict[list[str]]  # '%Y%m%d': ["<FirstChkIn>", "<LastChkOut>", "<LastSeat>", TotalMove]



    def __init__(self, studentID: str):
        """ **studentID:** 데이터를 불러올 학번 """

        self.StudentID = studentID

        self.CurrentSeat = None

        self.SeatReserved = False
        self.ReservedSeat = None

        self.Activity = {}

        self.TotalMove = 0

        # 기존 데이터가 없으면 만듦
        if not path.exists(StudentData.DIRECTORY + "/student_data/" + self.StudentID + ".json"):
            self.Created = True
            self.Name = None

            for s in self.CONFIG.Students:
                if s[0] == studentID:
                    self.Name = s[1]
                    if str(s[2]).strip() not in ("", "None") and RoomData.TodayReservedSeat():
                        self.SeatReserved = True
                        self.ReservedSeat = s[2]
                    break

            self.WeeklyCheckInStamp = [False, False, False, False, False, False, False]
            self.WeeklyCheckInStamp_ = datetime.now().isocalendar()[1]

            self.save()
        
        # 기존 데이터가 있으면 불러옴
        else:
            self.Created = False
            d: dict
            with open(StudentData.DIRECTORY + "/student_data/" + self.StudentID + ".json", 'r', encoding='utf-8') as f:
                d = json.load(f)

            self.Name = d['Name']
            for s in self.CONFIG.Students:
                if s[0] == studentID:
                    if s[0] != self.Name:
                        self.Name = s[1]
                    if str(s[2]).strip() not in ("", "None") and RoomData.TodayReservedSeat():
                        self.SeatReserved = True
                        self.ReservedSeat = s[2]
                    break

            if d['Week'] == datetime.now().isocalendar()[1]:
                self.WeeklyCheckInStamp = d['WeekStamp']
                self.WeeklyCheckInStamp_ = d['Week']
            else:
                self.WeeklyCheckInStamp = [False, False, False, False, False, False, False]
                self.WeeklyCheckInStamp_ = datetime.now().isocalendar()[1]

            self.Activity = d['Activity']


    def save(self):
        """ StudentData를 저장함. JSON 형식으로 저장됨. """
        import os
        if not os.path.exists(StudentData.DIRECTORY + '/student_data/'):
            os.makedirs(StudentData.DIRECTORY + '/student_data/')
        with open(StudentData.DIRECTORY + "/student_data/" + self.StudentID + ".json", 'w', encoding='utf-8') as f:
            json.dump(self.raw(), f, indent="\t")


    def raw(self) -> dict:
        """ JSON 파일로 저장하기 위해 딕셔너리로 감쌈. """

        return {

            'ID': self.StudentID,
            'Name': self.Name,

            'WeekStamp' : self.WeeklyCheckInStamp,
            'Week'      : self.WeeklyCheckInStamp_,

            'Activity': self.Activity

        }
    

    def getLastUsedSeat(self) -> str:
        """ 마지막으로 사용한 좌석 번호를 반환함. """

        Latest = -1

        for date in self.Activity.keys():
            if Latest < int(date):
                Latest = int(date)

        if Latest == -1:
            return None

        Seat = self.Activity[str(Latest)][2]

        return Seat
    

    def getLastCheckIn(self) -> datetime:
        """ 마지막으로 자습한 날의 입실 시간을 반환함. **데이터가 없으면 None을 반환함.** """

        Latest = -1

        for date in self.Activity.keys():
            if Latest < int(date):
                Latest = int(date)

        if Latest == -1:
            return None

        if self.Activity[str(Latest)][0] != None:
            return datetime.strptime(self.Activity[str(Latest)][0], '%Y%m%d%H%M%S.%f')
        else:
            return None
    

    def getLastCheckOut(self) -> datetime:
        """ 마지막으로 자습한 날의 퇴실 시간을 반환함. **데이터가 없으면 None을 반환함.** """

        Latest = -1

        for date in self.Activity.keys():
            if Latest < int(date):
                Latest = int(date)

        if Latest == -1:
            return None

        if self.Activity[str(Latest)][1] != None:
            return datetime.strptime(self.Activity[str(Latest)][1], '%Y%m%d%H%M%S.%f')
        else:
            return None