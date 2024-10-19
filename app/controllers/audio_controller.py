import io
from fastapi import UploadFile
from app.services.audio_service import audio_analyze

def handle_audio_upload(file: UploadFile, gender: str):
    """
    음성 파일을 저장하지 않고, 메모리에서 바로 분석 서비스로 넘겨줍니다.
    성별을 추가적으로 입력받아 분석에 활용합니다.
    """
    # 파일의 내용을 메모리에서 읽어 바이너리 데이터로 변환
    audio_data = file.file.read()

    # 'BytesIO'를 사용하여 바이너리 데이터를 librosa가 처리할 수 있는 형태로 변환
    audio_buffer = io.BytesIO(audio_data)

    # 메모리 상의 파일 데이터와 성별을 이용해 음성 분석 수행
    result = audio_analyze(audio_buffer, gender)

    # 분석 결과 반환
    return result