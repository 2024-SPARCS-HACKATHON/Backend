from fastapi import FastAPI, Depends
from .config.database import EngineConn  # 엔진 클래스 변경
from app.routes.audio_route import router as audio_router
from fastapi.middleware.cors import CORSMiddleware

from .models.models import Base

app = FastAPI()

app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 엔진 연결 및 세션 생성
engine = EngineConn()

# 테이블 생성
Base.metadata.create_all(bind=engine.engine)

# 의존성 주입으로 세션을 관리
def get_db():
    db = engine.get_session()
    try:
        yield db
    finally:
        db.close()

# FastAPI 라우터 등록
app.include_router(audio_router, prefix="/audio")

# @app.get("/")
# async def first_get(db: Session = Depends(get_db)):
#     # 데이터베이스 쿼리 예시
#     result = db.execute("SELECT 'Hello' AS message").fetchone()
#     return {"message": result["message"]}