
from winrt.windows.media.control import \
            GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.storage.streams import DataReader
import array, hashlib
from dataclasses import dataclass

from pygame import Surface, image
from io import BytesIO



@dataclass(slots=True)
class MediaInfo:
    """
    ### 미디어 정보 데이터

    현재 재생 중인 미디어 정보를 저장함.

    **update() 메서드는 UpdateExecuter에서 실행하여 미디어 정보를 업데이트 함.**
    """


    UseMediaDetection: bool # 미디어 감지 사용 여부, Configuration에 값이 있음.
    Playing: bool # 재생 중 여부

    Updated: str # 데이터 갱신됨 여부, True일 때 데이터를 적용하고, 그 이후 False로 바꿈.

    Album : str # 앨범명
    Artist: str # 게시자
    Title : str # 트랙명

    Thumbnail   : bytes # 썸네일 데이터
    Thumbnail_Hash: str # 썸네일 데이터 해시값, 썸네일 변화 여부를 반별하는데 사용.
    Thumbnail_Retry: int # 데이터 갱신 재시도 횟수



    def __init__(self):
        self.Updated = False

        self.Album  = None
        self.Artist = None
        self.Title  = None

        self.Thumbnail = None
        self.Thumbnail_Hash = None
        self.Thumbnail_Retry = 0

        self.Playing = False


    def getThumbnail(self) -> Surface:
        """ 썸네일을 Pygame Surface로 반환함. """
        return image.load(BytesIO(self.Thumbnail))
    

    async def update(self):
        """
        현재 재생 중인 미디어를 감지하고 데이터를 업데이트함. **UpdateExecutor를 통해 실행됨.** 
        
        WinRT 라이브러리를 사용하는 만큼, Windows 환경에서만 작동하며,
        Configuration에서 미디어 인식 기능을 비활성화 하면 데이터를 업데이트 하지 않음.
        """

        if not self.UseMediaDetection:
            return

        sessions = await MediaManager.request_async()

        current_session = sessions.get_current_session()

        if current_session:
            info = await current_session.try_get_media_properties_async()

            self.Playing = True

            # 재생 정보 변화 여부 감지
            if self.Artist != info.artist or self.Title != info.title or self.Album != info.album_title:
                self.Album = info.album_title
                self.Artist = info.artist
                self.Title = info.title
                self.Updated = True
                self.Thumbnail_Retry = 3 # 3번 정도는 썸네일을 2초마다 업데이트시켜 썸네일이 안 보이는 문제를 완화함.

            # 썸네일 정보 갱신 (만약 재시도 횟수가 남아있는 경우)
            if self.Thumbnail_Retry:

                thumbnail_ref = info.thumbnail
                self.Thumbnail_Retry -= 1

                # 썸네일 데이터가 없는 경우
                if thumbnail_ref is None:

                    if self.Thumbnail_Hash:
                        self.Updated = True
                    
                    self.Thumbnail = None
                    self.Thumbnail_Hash = None

                # 썸네일 데이터가 있는 경우
                else:

                    # 썸네일 스트림 열기
                    stream = await thumbnail_ref.open_read_async()
                    
                    size = stream.size
                    reader = DataReader(stream)
                    await reader.load_async(size)

                    # 빈 array 만들고 read_bytes로 채움
                    buf = array.array('B', [0] * size)
                    reader.read_bytes(buf)

                    # array를 bytes로 변환
                    thumbnail = buf.tobytes()
                    thumbnail_hash = hashlib.md5(thumbnail).hexdigest()

                    # 썸네일 비교
                    if self.Thumbnail_Hash != thumbnail_hash: # 해시값이 다르면(썸네일에 차이가 생겼다면)
                        self.Thumbnail = thumbnail
                        self.Thumbnail_Hash = thumbnail_hash
                        self.Updated = True

        else:

            # 재생 중이지 않거나 미디어 정보가 없다면
            if self.Title is not None or self.Artist is not None or self.Album is not None:
                self.Updated = True
                self.Album = None
                self.Title = None
                self.Artist = None
                self.Thumbnail = None
                self.Thumbnail_Hash = None
                self.Thumbnail_Retry = 0
                self.Playing = False