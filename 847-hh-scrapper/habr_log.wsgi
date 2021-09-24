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


#---------------------------------- Variables End ----------


def application(env, start_response):
    out_s = ""
    #Инициализация SQLLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'habr.db')
    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

    
    Base = declarative_base()
    class Log(Base):
        __tablename__ = 'log'
        id = Column(Integer, primary_key=True, autoincrement=True)
        action = Column(String(64))
        status = Column(String(64))
        time = Column(Integer)
        donor = Column(String(64))

        def __init__(self, action, status, time, donor):
            self.action = action
            self.status = status
            self.time = time
            self.donor = donor

        def __repr__(self):
            return "<Log('%s','%s', '%s')>" % (self.action, self.status)


    # Создание таблицы
    Base.metadata.create_all(engine)


    Session = sessionmaker(bind=engine)
    sqllite_session = Session()


 
    out_s += "<table align=left cellspacing=8 cellpading=2 border=0><tr align=center><td>Date</td><td>Action</td><td>Status</td><td>Donor</td></tr>"
    log = sqllite_session.query(Log).order_by(desc(Log.id))[0:50]
    for item in log:
        date_time = datetime.fromtimestamp(item.time)
        s_date = date_time.strftime("%d %m %Y %H:%M:%S")
        out_s += f"<tr align=center><td>{s_date}</td><td>{item.action}</td><td>{item.status}</td><td>{item.donor}</td></tr>"

    out_s += "<br>"

    start_response('200 OK', [('Content-Type','text/html')])
    b = out_s.encode('utf-8')
    return [b]


