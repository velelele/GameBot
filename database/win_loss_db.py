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
class Result_Battle(Base):
    __tablename__ = 'win_loss_counts'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

Base.metadata.create_all(engine)

class Result_Battle_DB(DB_Interface):
    def __init__(self):
        super().__init__()

    def add(self, result):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(result)
        session.commit()

    def exists(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Result_Battle).filter_by(tg_id=tg_id).all()
        if len(result) == 0:
            return False
        else:
            return True

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Result_Battle).all()
        return result

    def get(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Result_Battle).filter_by(tg_id=tg_id).all()
        session.close()
        return result[0]

    def add_win(self, tg_id, win_cnt):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Result_Battle).filter_by(tg_id=tg_id).first()
        result.wins_cnt = win_cnt  # Обновите значение поля name в объекте модели
        session.commit()  # Сохраните изменения в базе данных

    def add_lose(self, tg_id, lose_cnt):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Result_Battle).filter_by(tg_id=tg_id).first()
        result.losses_cnt = lose_cnt  # Обновите значение поля name в объекте модели
        session.commit()  # Сохраните изменения в базе данных
