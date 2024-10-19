import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"

class EngineConn:
    def __init__(self):
        # 데이터베이스 엔진을 생성 (pool_recycle은 MySQL 서버의 wait_timeout에 맞춰 설정)
        self.engine = create_engine(DATABASE_URL, pool_recycle=3600)  # 1시간으로 설정
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        # 세션 객체를 반환하는 메서드 (의존성 주입에서 사용)
        return self.SessionLocal()

    def connection(self):
        # 커넥션을 반환하는 메서드 (직접적으로 사용할 경우 with 구문을 사용하는 것을 추천)
        conn = self.engine.connect()
        return conn

engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()