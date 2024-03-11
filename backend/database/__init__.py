import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# from .schema import
try:
    engine = create_engine(f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                           f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}",
                           isolation_level="READ COMMITTED", pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
except SQLAlchemyError as e:
    print(e)