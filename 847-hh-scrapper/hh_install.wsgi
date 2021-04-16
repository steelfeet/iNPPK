# -*- encoding: utf-8 -*-
# 
import os

"""
DATABASE_USER = 'id35114350'
DATABASE_PASSWORD = 'e4bq9KYzEuPCh4s'
DATABASE_HOST = '/var/run/postgresql'
DATABASE_PORT = '5432'
DATABASE_NAME = 'id35114350_hh'
"""

DATABASE_USER = 'id35114350'
DATABASE_PASSWORD = 'Hgatrdy5rTeq'
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'id35114350_hh'


virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def application(env, start_response):
    out_s = ""

    """
    engine = create_engine(
            f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}',
            pool_pre_ping=True
        )
    """
    engine = create_engine(
            f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}',
            pool_pre_ping=True
        )


    metadata = MetaData()
    vacancies_table = Table('vacancies', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('title', String(512)),
        Column('city', String(20)),
        Column('specialization', String(255)),
        Column('href', String(512)),
        Column('donor', String(255)),
        Column('vacancy_id', Integer),
        Column('vacancy_date', Integer),
        Column('parse_date', Integer),
        Column('employer', String(255)),
        Column('canal_city_id', Integer),
        Column('canal_city_date', Integer),
        Column('canal_spec_id', Integer),
        Column('canal_spec_date', Integer)
    )

    """
    log_table = Table('log', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('action', String(64)),
        Column('time', Integer),
        Column('donor', String(64)),
        Column('city', String(20)),
        Column('vacancies_count', Integer),
        Column('status', String(64)),
        Column('canal_id', Integer),
    )
    """


    metadata.create_all(engine)

    out_s = "success"
    start_response('200 OK', [('Content-Type','text/html')])
    b = out_s.encode('utf-8')
    return [b]
