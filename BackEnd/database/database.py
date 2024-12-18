from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine,autocommit=False,autoflush=False)

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()