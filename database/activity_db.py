from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.interfaceDB import DB_Interface

# Установка соединения с базой данных
engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/sys')

# Создание базовой модели
Base = declarative_base()


# Определение модели данных
class Matches(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    player1_id = Column(Integer)
    player2_id = Column(Integer)
    winner_id = Column(Integer)
    name_game = Column(String(15))


Base.metadata.create_all(engine)


class Activity_DB(DB_Interface):
    def __init__(self):
        super().__init__()

    def exists(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        match = session.query(Matches).filter_by(tg_id=tg_id).all()
        if len(match) == 0:
            return False
        else:
            return True

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        matches = session.query(Matches).all()
        return matches

    def get(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        match = session.query(Matches).filter_by(tg_id=tg_id).all()
        session.close()
        return match[0]

    def add(self, game):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(game)
        session.commit()

    def check_activity(self, day):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Получите текущую дату и время
        current_date = datetime.now()
        # Вычислите дату, от которой нужно отсчитывать выборку
        start_date = current_date - timedelta(days=day)
        # Выполните запрос на получение столбцов за указанный период
        query = session.query(Matches).filter(Matches.date >= start_date).all()
        session.commit()
        return query
