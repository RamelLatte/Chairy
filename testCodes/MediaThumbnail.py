
# 지금 재생되는 미디어의 썸네일을 가져오는 코드 스니펫.

import asyncio, array
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
from winrt.windows.storage.streams import DataReader

# ChatGPT가 써준 코드를 약간 수정함.
async def get_media_thumbnail():
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = manager.get_current_session()
    
    if session:
        properties = await session.try_get_media_properties_async()
        thumbnail_ref = properties.thumbnail
        
        if thumbnail_ref is not None:
            # 썸네일 스트림 열기
            stream = await thumbnail_ref.open_read_async()
            
            size = stream.size
            reader = DataReader(stream)
            await reader.load_async(size)

            # 빈 array 만들고 read_bytes로 채움
            buf = array.array('B', [0] * size)
            reader.read_bytes(buf)

            # array를 bytes로 변환
            data = buf.tobytes()

            # buffer를 Base64로 인코딩 후 반환
            return data

        else:
            return None
    else:
        return None


# 테스트용 렌더링

data = asyncio.run(get_media_thumbnail())

if data == None:
    print("데이터 없음.")

import io
import pygame as pg

pg.init()

DISP = pg.display.set_mode((300, 300))

DISP.blit(pg.transform.scale(pg.image.load(io.BytesIO(data)), (300, 300)), (0, 0))
pg.display.update()

def loop():
    while 1:

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                return

loop()