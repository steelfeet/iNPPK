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
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#---------------------------------- Variables ----------

areas = {"bryansk":19}
specializations = ['программист', 'стажер', 'стажировка']

proxies = [
                {
                'http': 'http://linbergsergey_gmail_:56c2134eac@212.81.34.171:30013',
                'https': 'http://linbergsergey_gmail_:56c2134eac@212.81.34.171:30013',
                },
                {
                'http': 'http://linbergsergey_gmail_:56c2134eac@212.81.33.230:30013',
                'https': 'http://linbergsergey_gmail_:56c2134eac@212.81.33.230:30013',
                },
                {},
            ]

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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hhtm.db')
    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


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


    #"""
    #формируем запрос
    city, area = random.choice(list(areas.items())) 
    host = city + ".hh.ru"
    #t = random.choice([0,1])
    t = 1
    if (t == 1):
        specialization = random.choice(specializations)
    else:
        specialization = ""
    user_agent = random.choice(user_agents)

    params = {
            'clusters': 'true',
            'area': area,
            'enable_snippets': 'true',
            'salary': '',
            'st': 'searchVacancy',
            'text': specialization
        }

    url = "https://" + host + "/search/vacancy?"+urllib.parse.urlencode(params)
    referer = "https://" + host + "/search/vacancy?"+urllib.parse.urlencode(params) + "&customDomain=1"

    headers = {
            "Host": str(host),
            'User-Agent': str(user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': str(referer),
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'}


    print(url)
    response = requests.get(url, headers=headers, params=params)
    post_html = response.text
    print(post_html)

    with open(os.path.join(basedir, 'response.html'), 'w', encoding="utf-8") as f:
        f.write(post_html)


    out_s += str(response.status_code)


    """
    with open(os.path.dirname(os.path.abspath(__file__)) + '/response.html', 'r', encoding='utf-8') as f:
        post_html = f.read()
    """
    
    
    #Парсим вакансии
    vacancies_count = 0
    soup = BeautifulSoup(post_html, "lxml")
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for vacancy in vacancies:
        try:
            vacancy_title = str(vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text).strip()
            vacancy_href = str(vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')).strip()
            vacancy_href = vacancy_href.split("?")[0]

            vacancy_id = vacancy_href.split("/")
            vacancy_id = int(vacancy_id[len(vacancy_id) - 1])

            #<span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_s-only">24.03.21</span>
            """
            vacancy_date = str(vacancy.find('span', {'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_s-only'}).text).strip()
            vacancy_date = int(time.mktime(datetime.datetime.strptime(vacancy_date, "%d.%m.%y").timetuple()))
            """

            #<a href="/employer/2936112" class="bloko-link bloko-link_secondary" data-qa="vacancy-serp__vacancy-employer"> Квадратный метр</a>
            vacancy_employer = str(vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).text).strip()
            vacancy_employer_id = str(vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).get('href')).strip()
            vacancy_employer_id = vacancy_employer_id.replace('/employer/', '')
            

            out_s += str(vacancy_title) + "<br>"
            out_s += str(vacancy_href + " :: " + str(vacancy_id)) + "<br>"
            #out_s += str(vacancy_date) + "<br>"
            out_s += str(vacancy_employer + " :: " + vacancy_employer_id) + "<br>"

            #уникальность вакансии
            out_s += "Проверяем уникальность\n" + "<br>"
            vacancy_n = session.query(Vacancies).filter(Vacancies.href == vacancy_href).count()
            out_s += str(vacancy_n) + "<br>"
            if (vacancy_n == 0):
                out_s += "Добавляем в базу" + "<br>"
                new_vacancy = Vacancies(
                    title = vacancy_title, 
                    city = city, 
                    specialization = specialization, 
                    href = vacancy_href,
                    donor = 'hh.ru', 
                    vacancy_id = vacancy_id, 
                    vacancy_date = int(time.time()), 
                    parse_date = int(time.time()), 
                    employer=vacancy_employer, 
                    canal_city_id = 0, 
                    canal_city_date = 0, 
                    canal_spec_id = 0,
                    canal_spec_date = 0
                    )
                session.add(new_vacancy)
                vacancies_count += 1
            out_s += "<br>"
            status = 'Ok'
        except Exception as e:
            out_s += str(traceback.format_exc())
            status = str(traceback.format_exc())

    new_log = Log(
        action = "parse", 
        status = status, 
        time = int(time.time()),
        donor = 'hh.ru', 
        city = city, 
        specialization = specialization,
        vacancies_count = vacancies_count, 
        canal_id = 0, 
        )
    session.add(new_log)



    session.commit()
    start_response('200 OK', [('Content-Type','text/html')])
    b = out_s.encode('utf-8')
    return [b]


