from fastapi import APIRouter, UploadFile, File, Form
from app.controllers.audio_controller import handle_audio_upload

router = APIRouter()

# 음성 분석 API 엔드포인트
@router.post("/analyze_audio")
async def analyze_audio(file: UploadFile = File(...), gender: str = Form(...), age: int = Form(...)):
    """
    프론트엔드에서 multi-part/form-data로 전달받은 음성 파일과 성별을 저장하지 않고 바로 분석하는 API.
    """
    # 성별과 파일을 함께 handle_audio_upload 함수로 전달
    result = handle_audio_upload(file, gender, age)
    return result