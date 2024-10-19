from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CelebVoiceAnalysis(Base):
    __tablename__ = 'voice_analysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)                # 사용
    voice_name = Column(String(255), nullable=False)          # 목소리 유형

    def __repr__(self):
        return f"<VoiceAnalysis(voice_name={self.voice_name}, f0_mean={self.f0_mean})>"

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