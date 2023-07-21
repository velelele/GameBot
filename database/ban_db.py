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
class Ban(Base):
    __tablename__ = 'bans'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    ban = Column(Boolean, default=False)
    ban_date = Column(Date)

Base.metadata.create_all(engine)

class Ban_DB(DB_Interface):
    def __init__(self):
        super().__init__()

    def add(self, ban):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(ban)
        session.commit()

    def exists(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        ban = session.query(Ban).filter_by(tg_id=tg_id).all()
        if len(ban) == 0:
            return False
        else:
            return True

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        ban = session.query(Ban).all()
        return ban

    def get(self, tg_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        ban = session.query(Ban).filter_by(tg_id=tg_id).all()
        session.close()
        return ban[0]

    def set(self, tg_id, token):
        Session = sessionmaker(bind=engine)
        session = Session()
        ban = session.query(Ban).filter_by(tg_id=tg_id).first()
        ban.token = token
        session.commit()

    def check_ban(self, tg_id):
        user = self.get(tg_id)
        if user.ban:
            return True
        else:
            return False