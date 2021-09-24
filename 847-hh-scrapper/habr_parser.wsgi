# -*- encoding: utf-8 -*-
# 
import os, urllib.parse, traceback
virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))


from bs4 import BeautifulSoup
import random, time, datetime
import requests
from requests.exceptions import ProxyError

#декларативное определение
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#---------------------------------- Variables ----------

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; rv:23.0) Gecko/20100101 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 YaBrowser/1.7.1364.21027 Safari/537.22",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.15",
    "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10.14; rv: 75.0) Gecko / 20100101 Firefox / 75.0",
    "Mozilla / 5.0 (Windows NT 6.1; Win64; x64; rv: 74.0) Gecko / 20100101 Firefox / 74.0",
    "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit / 537.36 (KHTML, как Gecko) Chrome / 80.0.3987.163 Safari / 537.36",
    "Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T MIUI/V12.0.5.0.QFJMIXM)"
]


#---------------------------------- Variables End ----------




def application(env, start_response):
    out_s = ""
    #Инициализация SQLLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'habr.db')
    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


    Base = declarative_base()
    class Links(Base):
        __tablename__ = 'links'
        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String(512))
        href = Column(String(512))
        donor = Column(String(255))
        donor_link_id = Column(Integer) #внутренний идентификатор для донора, https://habr.com/ru/company/skillfactory/blog/578014/ -> 578014
        parse_date = Column(Integer)
        text = Column(Text)

        def __init__(self, title, href, donor, donor_link_id, parse_date, text):
            self.title = title
            self.href = href
            self.donor = donor
            self.donor_link_id = donor_link_id
            self.parse_date = parse_date
            self.text = text

        def __repr__(self):
            return "<Link('%s', '%s')>" % (self.title, self.href)


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


    #"""
    #формируем запрос
    user_agent = random.choice(user_agents)
    url = "https://habr.com/ru/all/"
    referer = "https://habr.com/ru/all/"

    headers = {
            "Host": str("habr.com"),
            'User-Agent': str(user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': str(referer),
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'}


    response = requests.get(url, headers=headers)
    post_html = response.text

    with open(os.path.join(basedir, 'habr.html'), 'w', encoding="utf-8") as f:
        f.write(post_html)

    #Парсим ссылки habr.com
    soup = BeautifulSoup(post_html, "lxml")
    vacancies = soup.find_all('div', {'class': 'tm-article-snippet'})
    for vacancy in vacancies:
        try:
            link_title = str(vacancy.find('h2', {'class': 'tm-article-snippet__title_h2'}).text).strip()
            link_href = str(vacancy.find('a', {'class': 'tm-article-snippet__title-link'}).get('href')).strip()
            link_href = "https://habr.com" + link_href

            #donor_link_id - предпоследнее число из link_href
            donor_link_ids = link_href.split("/")
            donor_link_id = donor_link_ids[len(donor_link_ids)-2]

            out_s += str(link_title) + "<br>"
            out_s += str(link_href + " :: " + str(donor_link_id)) + "<br>"

            #уникальность ссылки
            out_s += "Проверяем уникальность\n" + "<br>"
            link_n = sqllite_session.query(Links).filter(Links.donor_link_id == donor_link_id).count()
            out_s += "link_n: " + str(link_n) + "<br>"
            if (link_n == 0):
                out_s += "Добавляем в базу" + "<br>"
                new_link = Links(
                    title = link_title, 
                    href = link_href,
                    donor = 'habr.ru', 
                    donor_link_id = donor_link_id, 
                    parse_date = int(time.time()), 
                    text = ""
                    )
                sqllite_session.add(new_link)
            else:
                out_s += "В базе ссылка есть" + "<br>"

            out_s += "<br>"
            status = 'Ok'

        except Exception as e:
            out_s += str(traceback.format_exc())
            status = str(traceback.format_exc())

    new_log = Log(
        action = "parse", 
        status = status, 
        time = int(time.time()),
        donor = 'habr.ru', 
        )
    sqllite_session.add(new_log)

    sqllite_session.commit()
    out_s += "<br>success"
    start_response('200 OK', [('Content-Type','text/html')])
    b = out_s.encode('utf-8')
    return [b]


