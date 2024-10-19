from pydub import AudioSegment
import io
import librosa
from app.services.audio_service import audio_analyze
from fastapi import UploadFile

async def handle_audio_upload(file: UploadFile, gender: str, age: int):
    await file.seek(0)
    audio_data = await file.read()
    if not audio_data:
        raise ValueError("업로드된 파일이 비어 있습니다.")

    # 업로드된 파일의 MIME 타입과 확장자 출력
    content_type = file.content_type.split(';')[0]  # MIME 타입의 주요 부분만 추출
    print(f"Received file content type: {content_type}")

    # 지원되는 오디오 형식 목록 (MIME 타입 기반)
    supported_formats = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/flac', 'audio/webm']

    if content_type not in supported_formats:
        raise ValueError(f"지원되지 않는 오디오 형식입니다: {content_type}")

    audio_buffer = io.BytesIO(audio_data)

    try:
        # 파일 형식 자동 감지
        audio = AudioSegment.from_file(audio_buffer, format=content_type.split('/')[-1])
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        y, sr = librosa.load(wav_io, sr=None)
        wav_io.seek(0)
    except Exception as e:
        print(f"오디오 파일 로드 중 오류 발생: {e}")
        raise ValueError(f"오디오 파일을 처리할 수 없습니다: {e}")

    result = await audio_analyze(wav_io, gender, age)
    return result