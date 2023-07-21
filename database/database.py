from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

# Установка соединения с базой данных
engine = create_engine('mysql+mysqlconnector://root:123123654654@@localhost:3306/fortgbot')

# Создание базовой модели
Base = declarative_base()

# Определение модели данных
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    tg_id = Column(Integer)
    token = Column(Integer, default=100)
    ban = Column(Boolean, default=False)
    wins_cnt = Column(Integer, default=0)
    losses_cnt = Column(Integer, default=0)
    date_registration = Column(Date)
    post = Column(String(20))

Base.metadata.create_all(engine)

def add_user(user):
    Session = sessionmaker(bind=engine)
    session = Session()
    exists = user_exist(user.tg_id)
    if not exists:
        session.add(user)
        session.commit()
        return f"Вы зарегистрировались как {user.post}!"
    else:
        session.commit()
        return "Вы уже зарегистрированы"

def definition_post(tg_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = get_user(tg_id)
        session.commit()
        return user.post
    except:
        print("Проблема с базой данных")

def get_all_user():
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(User).all()
    return users


def get_user(tg_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(tg_id=tg_id).all()
    session.close()
    return user[0]

def get_post(tg_id):
    user = get_user(tg_id)
    return user.post

def set_token(tg_id, token):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    user.token = token
    session.commit()

def set_ban(tg_id, ban):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    user.ban = ban
    session.commit()

def add_win(tg_id, win_cnt):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    user.wins_cnt = win_cnt  # Обновите значение поля name в объекте модели
    session.commit()  # Сохраните изменения в базе данных

def add_lose(tg_id, lose_cnt):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    user.losses_cnt = lose_cnt  # Обновите значение поля name в объекте модели
    session.commit()  # Сохраните изменения в базе данных

def check_ban(tg_id):
    user = get_user(tg_id)
    if user.ban:
        return True
    else:
        return False

def user_exist(tg_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(User).filter_by(tg_id=tg_id).all()
    if len(users) == 0:
        return False
    else:
        return True

def check_new_user(day):
    Session = sessionmaker(bind=engine)
    session = Session()
    # Получите текущую дату и время
    current_date = datetime.now()
    # Вычислите дату, от которой нужно отсчитывать выборку
    start_date = current_date - timedelta(days=day)
    # Выполните запрос на получение столбцов за указанный период
    query = session.query(User).filter(User.date_registration >= start_date).all()
    session.commit()
    return query

