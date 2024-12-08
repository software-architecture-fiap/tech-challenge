from os import environ as env
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL: str = env.get('DATABASE_URL', '')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Cria uma sessão de banco de dados e garante que ela seja fechada ao final.

    Esta função é usada como uma dependência em frameworks como FastAPI para garantir
    que cada requisição tenha sua própria sessão de banco de dados.

    Yields:
        Generator[Session, None, None]: Uma sessão de banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
