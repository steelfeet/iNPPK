# -*- encoding: utf-8 -*-
# 
import os, urllib.parse, traceback

virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))


import random, time
from datetime import datetime

#декларативное определение
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

#---------------------------------- Variables ----------
DATABASE_USER = 'id35114350'
DATABASE_PASSWORD = 'Hgatrdy5rTeq'
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'id35114350_hh'

#---------------------------------- Variables End ----------


def application(env, start_response):
    out_s = ""
    engine = create_engine(
            f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}',
            pool_pre_ping=True
        )
    
    Base = declarative_base()
    class Vacancies(Base):
        __tablename__ = 'vacancies'
        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String(512))
        city = Column(String(20))
        specialization = Column(String(255))
        href = Column(String(512))
        donor = Column(String(255))
        vacancy_id = Column(Integer)
        vacancy_date = Column(Integer)
        parse_date = Column(Integer)
        employer = Column(String(255))
        canal_city_id = Column(Integer)
        canal_city_date = Column(Integer)
        canal_spec_id = Column(Integer)
        canal_spec_date = Column(Integer)

        def __init__(self, title, city, specialization, href, donor, vacancy_id, vacancy_date, parse_date, employer, canal_city_id, canal_city_date, canal_spec_id, canal_spec_date):
            self.title = title
            self.city = city
            self.specialization = specialization
            self.href = href
            self.donor = donor
            self.vacancy_id = vacancy_id
            self.vacancy_date = vacancy_date
            self.parse_date = parse_date
            self.employer = employer
            self.canal_city_id = canal_city_id
            self.canal_city_date = canal_city_date
            self.canal_spec_id = canal_spec_id
            self.canal_spec_date = canal_spec_date

        def __repr__(self):
            return "<Vacancy('%s','%s', '%s')>" % (self.title, self.specialization, self.href)


    class Log(Base):
        __tablename__ = 'log'
        id = Column(Integer, primary_key=True, autoincrement=True)
        action = Column(String(64))
        status = Column(String(64))
        time = Column(Integer)
        donor = Column(String(64))
        city = Column(String(20))
        specialization = Column(String(20))
        vacancies_count = Column(Integer)
        canal_id = Column(String(64))

        def __init__(self, action, status, time, donor, city, specialization, vacancies_count, canal_id):
            self.action = action
            self.status = status
            self.time = time
            self.donor = donor
            self.city = city
            self.specialization = specialization
            self.vacancies_count = vacancies_count
            self.canal_id = canal_id

        def __repr__(self):
            return "<Log('%s','%s', '%s')>" % (self.action, self.status)

    # Создание таблицы
    Base.metadata.create_all(engine)


    Session = sessionmaker(bind=engine)
    session = Session()


 
    out_s += "<table align=left cellspacing=8 cellpading=2 border=0><tr align=center><td>Date</td><td>Action</td><td>Status</td><td>Donor</td><td>Сity</td><td>Specialization</td><td>Vacancies Count</td><td>Canal ID</td></tr>"
    log = session.query(Log).order_by(desc(Log.id))[0:50]
    for item in log:
        date_time = datetime.fromtimestamp(item.time)
        s_date = date_time.strftime("%d %m %Y %H:%M:%S")
        out_s += f"<tr align=center><td>{s_date}</td><td>{item.action}</td><td>{item.status}</td><td>{item.donor}</td><td>{item.city}</td><td>{item.specialization}</td><td>{item.vacancies_count}</td><td>{item.canal_id}</td></tr>"

    out_s += "<br>"

    start_response('200 OK', [('Content-Type','text/html')])
    b = out_s.encode('utf-8')
    return [b]


