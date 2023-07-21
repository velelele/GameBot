from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from database.interfaceDB import DB_Interface
from ban_db import Ban_DB, Ban
from rating_db import Rating, Rating_DB
from win_loss_db import Result_Battle_DB, Result_Battle

engine = create_engine('mysql+mysqlconnector://root:12345@localhost:3306/sys')

# Создание базовой модели
Base = declarative_base()


# Определение модели данных
class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name_player = Column(String(50))
    registration_date = Column(Date)
    position = Column(String(20))
    password = Column(String(100))


Base.metadata.create_all(engine)


class Player_DB(DB_Interface):
    def __init__(self):
        super().__init__()

    def add(self, player):
        Session = sessionmaker(bind=engine)
        session = Session()
        exists = self.exists(player.tg_id)
        if not exists:
            ban_db = Ban_DB()
            rating_DB = Rating_DB()
            result_Battle_DB = Result_Battle_DB()
            ban_db.add(Ban(player_id=player.id, date=datetime.now()))
            rating_DB.add(Rating(player_id=player.id))
            result_Battle_DB.add(Result_Battle(player_id=player.id))

            session.add(player)
            session.commit()
            return True  # f"Вы зарегистрировались как {user.post}!"
        else:
            session.commit()
            return False  # "Вы уже зарегистрированы"

    def definition_post(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            player = self.get_user(tg_id)
            session.commit()
            return player.post
        except:
            print("Проблема с базой данных")

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        player = session.query(Player).all()
        return player

    def get(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        player = session.query(Player).filter_by(tg_id=tg_id).all()
        session.close()
        return player[0]

    """  def get_position(self, tg_id):
        player = self.get(tg_id)
        return player.post
    """

    def exists(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        users = session.query(Player).filter_by(tg_id=tg_id).all()
        if len(users) == 0:
            return False
        else:
            return True

    def check_new_user(self, day):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Получите текущую дату и время
        current_date = datetime.now()
        # Вычислите дату, от которой нужно отсчитывать выборку
        start_date = current_date - timedelta(days=day)
        # Выполните запрос на получение столбцов за указанный период
        query = session.query(Player).filter(Player.date_registration >= start_date).all()
        session.commit()
        return query
