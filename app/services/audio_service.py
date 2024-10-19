import os

import numpy as np
import librosa
import joblib
import pandas as pd
import openai

# 1. 저장된 모델 및 전처리 객체 로드
loaded_model = joblib.load('voice_type_model.joblib')  # AI 모델 로드
loaded_scaler = joblib.load('scaler.joblib')
loaded_gender_encoder = joblib.load('gender_encoder.joblib')
X_columns = joblib.load('X_columns.joblib')
type_encoder = joblib.load('type_encoder.joblib')  # 타입 인코더 추가

def audio_analyze(audio_buffer, input_gender):
    """
    음성 파일 데이터를 분석하여 목소리 유형을 예측하고, 추가 분석을 수행하는 함수.
    """
    # 2. 성별 인코딩
    input_gender_encoded = loaded_gender_encoder.transform([input_gender])[0]

    # 3. 오디오 파일에서 MFCC 추출
    y, sr = librosa.load(audio_buffer, sr=None)

    # 기본 주파수(F0) 계산
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=300)
    f0_mean = np.nanmean(f0).item()

    # 음량(Loudness) 계산
    rms = librosa.feature.rms(y=y)
    mean_rms = np.mean(rms).item()

    # 4. 멜 주파수 켑스트럼 계수(MFCC) 1번부터 20번까지 계산
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc, axis=1).tolist()

    # 5. AI 판별에 사용할 MFCC 값 (모든 MFCC 1~20 사용)
    selected_mfccs_mean = mfcc_mean[:20]

    # 6. 입력 데이터 구성 (선택한 MFCC 값과 성별 데이터 포함)
    input_features = np.append(selected_mfccs_mean, input_gender_encoded)

    # 입력 데이터를 DataFrame으로 변환하고 피처 이름 적용
    new_X = pd.DataFrame([input_features], columns=X_columns)

    # 7. 특성 데이터 스케일링
    new_X_scaled = loaded_scaler.transform(new_X)

    # 8. 모델을 사용해 목소리 유형 예측
    predicted_type_encoded = loaded_model.predict(new_X_scaled)
    predicted_type = type_encoder.inverse_transform(predicted_type_encoded)

    # 9. 예측된 목소리 유형을 기반으로 추가적인 분석 수행
    voice_analysis = analyze_voice_by_conditions(f0_mean, mean_rms, mfcc_mean, predicted_type[0])

    # 10. ChatGPT API를 사용해 추가 설명 생성
    chatgpt_explanation = get_voice_explanation_from_chatgpt(predicted_type[0], f0_mean, mean_rms, mfcc_mean)

    # 10. 분석 결과 반환
    return {
        "f0_mean": f0_mean,
        "mean_rms": mean_rms,
        "mfcc_1_to_20": mfcc_mean,
        "final_analysis": voice_analysis,
        "chatgpt_explanation": chatgpt_explanation
    }

def analyze_voice_by_conditions(f0_mean, mean_rms, mfcc_mean, predicted_type):
    """
    예측된 목소리 유형과 f0, RMS, MFCC 값을 바탕으로 최종 분석을 수행하는 함수.
    10가지 목소리 유형에 맞는 조건을 설정.
    """
    voice_conditions = [
        {
            "name": "딥 네이비",
            "description": "깊고 차분한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "깊고 따뜻한 목소리" and f0_mean < 120
        },
        {
            "name": "골든 소울",
            "description": "따뜻하고 감정이 풍부한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "깊고 따뜻한 목소리" and f0_mean >= 120 and f0_mean < 160
        },
        {
            "name": "라이트 코랄",
            "description": "밝고 경쾌한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "밝고 활기찬 목소리" and f0_mean >= 160 and mean_rms > 0.15
        },
        {
            "name": "실버 미스트",
            "description": "부드럽고 은은한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "부드럽고 매혹적인 목소리" and mean_rms < 0.1
        },
        {
            "name": "파이어 레드",
            "description": "강렬하고 힘찬 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "강렬하고 카리스마 있는 목소리" and f0_mean < 150 and mean_rms > 0.2
        },
        {
            "name": "크리스탈 화이트",
            "description": "맑고 깨끗한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "밝고 활기찬 목소리" and f0_mean > 160
        },
        {
            "name": "소프트 베이지",
            "description": "부드럽고 차분한 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "부드럽고 매혹적인 목소리" and f0_mean < 140
        },
        {
            "name": "스파클링 옐로우",
            "description": "밝고 활기찬 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "밝고 활기찬 목소리" and mean_rms > 0.2
        },
        {
            "name": "웜 브라운",
            "description": "따뜻하고 안정감 있는 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "깊고 따뜻한 목소리" and mean_rms < 0.15
        },
        {
            "name": "다크 체리",
            "description": "강렬하고 카리스마 있는 목소리입니다.",
            "conditions": lambda f0_mean, mean_rms, mfcc_mean, predicted_type: predicted_type == "강렬하고 카리스마 있는 목소리"
        }
    ]

    # 조건을 만족하는 목소리 유형을 찾음
    for voice in voice_conditions:
        if voice["conditions"](f0_mean, mean_rms, mfcc_mean, predicted_type):
            return {
                "voice_name": voice["name"],
                "description": voice["description"]
            }

    # 기본 반환: 마지막 항목이 항상 선택되도록 설계하지 않음
    return {
        "voice_name": "분석 불가",
        "description": "분석 가능한 목소리 유형이 아닙니다."
    }


def get_voice_explanation_from_chatgpt(predicted_type, f0_mean, mean_rms, mfcc_mean):
    """
    ChatGPT API를 호출하여 목소리 유형에 대한 설명과 과학적 원리를 기반으로 한 설명을 생성합니다.
    소숫점 아래 자리를 제거하여 간결한 설명을 생성합니다.
    """
    # 소숫점 아래 자리를 제거
    f0_mean_rounded = round(f0_mean)
    mean_rms_rounded = round(mean_rms, 2)
    mfcc_mean_rounded = [round(mfcc, 0) for mfcc in mfcc_mean[:5]]  # MFCC 값 소숫점 제거

    prompt = f"""
    당신은 음성 분석 전문가입니다. 아래 목소리 유형에 대해 설명해주세요.
    - 목소리 유형: '{predicted_type}'
    이 목소리는 어떤 특징을 갖는지 "목소리의 특징 :"으로 요약하고, 이어서 과학적인 분석을 "과학적 원리 :"로 시작하여 작성해주세요.

    과학적 분석은 다음의 목소리 특성에 기반해 작성해주세요:
    - 기본 주파수(f0): {f0_mean_rounded}Hz
    - 음량(RMS): {mean_rms_rounded}
    - MFCC 값: {mfcc_mean_rounded} (MFCC 1~5번만 예시로 제시했습니다).

    과학적 설명은 300 토큰 이내로 작성해주세요.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # 사용 가능한 모델로 설정
        messages=[
            {"role": "system", "content": "당신은 목소리 분석 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    # API 응답에서 설명 추출
    return response['choices'][0]['message']['content'].strip()