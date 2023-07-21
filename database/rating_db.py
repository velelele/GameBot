from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from database.interfaceDB import DB_Interface

engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/sys')

# Создание базовой модели
Base = declarative_base()


# Определение модели данных
class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    rating = Column(Integer, default=100)


Base.metadata.create_all(engine)


class Rating_DB(DB_Interface):
    def __init__(self):
        super().__init__()

    def add(self, rating):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(rating)
        session.commit()

    def exists(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        rating = session.query(Rating).filter_by(tg_id=tg_id).all()
        if len(rating) == 0:
            return False
        else:
            return True

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        rating = session.query(Rating).all()
        return rating

    def get(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        rating = session.query(Rating).filter_by(tg_id=tg_id).all()
        session.close()
        return rating[0]

    def set(self, tg_id, token):
        Session = sessionmaker(bind=engine)
        session = Session()
        rating = session.query(Rating).filter_by(tg_id=tg_id).first()
        rating.rating = rating
        session.commit()
