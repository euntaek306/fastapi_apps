from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# db 엔진 : sqlite3용
DB_URL = 'sqlite:///todos.sqlite3'

# mysql용 엔진
# DB_URL = 'mysql엔진'

# mysql 연결시
# "mysql+pymysql://user_ID:password@host_IP:3306/DB_name"
# DB_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db_name}"

# 데이터베이스에 연결하는 엔진을 생성하는 함수
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()