from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CelebVoiceAnalysis(Base):
    __tablename__ = 'voice_analysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)                # 사용
    voice_name = Column(String(255), nullable=False)          # 목소리 유형
    description = Column(Text, nullable=True)                 # 설명 추가

    def __repr__(self):
        return (f"<VoiceAnalysis(name={self.name}, voice_name={self.voice_name}, "
                f"description={self.description})>")

class VoiceTypeInfo(Base):
    __tablename__ = 'voice_type_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voice_type = Column(String(255), nullable=False)          # 목소리 타입
    description = Column(Text, nullable=True)                 # 목소리 타입 설명
    solution1 = Column(Text, nullable=True)                   # 첫 번째 해결 방법
    solution2 = Column(Text, nullable=True)                   # 두 번째 해결 방법
    solution3 = Column(Text, nullable=True)                   # 세 번째 해결 방법

    def __repr__(self):
        return (f"<VoiceTypeInfo(voice_type={self.voice_type}, "
                f"description={self.description}, solution1={self.solution1}, "
                f"solution2={self.solution2}, solution3={self.solution3})>")

# 타이틀, 설명, 배경 색상 코드가 포함된 모델 추가
class VoiceUITheme(Base):
    __tablename__ = 'voice_ui_theme'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)               # 타이틀
    description = Column(Text, nullable=True)                 # 설명
    background_color_start = Column(String(7), nullable=False)      # 배경 색상 코드 (예: '#FFFFFF')
    background_color_end = Column(String(7), nullable=False)      # 배경 색상 코드 (예: '#FFFFFF')
    title_kor = Column(String(255), nullable=True)            # 한글 타이틀

    def __repr__(self):
        return (f"<VoiceUITheme(title={self.title}, description={self.description}, "
                f"background_color_start={self.background_color_start}, background_color_end={self.background_color_end})>")