# -*- encoding: utf-8 -*-
# 
import os, json, sys, subprocess, urllib.parse, traceback
import random, time, datetime, re
from urllib.parse import unquote

virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))

import requests
#MySql
from mysql.connector import connect, Error

#декларативное определение SQLLite
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc


#---------------------------------- Variables ----------




#---------------------------------- Variables End ----------





def application(env, start_response):
    out_s = {}

    """
    for key in env:
        out_s = out_s + str(key) + "=" + str(env[key]) + "<br>"
    """
    #получаем $_GET из запроса
    get_query = env['QUERY_STRING']
    get_json = get_query.replace("q=", "")
    get_json = unquote(get_json)

    get_dict = json.loads(get_json)
    tm_id = str(get_dict['tm_id'])
    vk_id = str(get_dict['vk_id'])
    out_s["tm_id"] = tm_id
    
    #Инициализация MySQL
    mysql_connection = connect(
            host="localhost",
            user="id35114350",
            password="Hgatrdy5rTeq",
            database="id35114350_steelfeet",
            charset='utf8',
            use_unicode=True            
        )


    #------------------------------------------ Основной цикл ------------------

    #запрос wp_id по внешнему сервису
    params = {
        "action":"show_wp_id",
        "tm_id":tm_id
    }
    params_json = json.dumps(params)
    get_wp_url = "https://steelfeet.ru/app/get.php?q=" + params_json
    out_s["get_wp_url"] = get_wp_url

    response = requests.get(get_wp_url)
    wp_id = int(response.text)
    out_s["wp_id"] = wp_id




    now = datetime.datetime.now()
    for item in links_list:
        #добавляем показанные вакансии в лог
        #INSERT INTO `sf_log` (`user_id`, `date`, `hour`, `code`, `action`, `data_1`, `data_2`, `data_3`, `data_4`, `data`, `weight`) VALUES ('', '', '', '', '', '', '', '', '', '');

        exist_vacancies_query = "SELECT `id` FROM `sf_log` WHERE (`code` = 'read') AND (`data_1` = " + str(item["id"]) + ");"
        with mysql_connection.cursor(buffered=True) as cursor:
            cursor.execute(exist_vacancies_query)
            exist_vacancies = cursor.fetchall()


        if (len(exist_vacancies) == 0):
            mysql_query = "INSERT INTO `sf_log` (`user_id`, `date`, `hour`, `code`, `action`, `data_1`, `data_2`, `data_3`, `data_4`, `data`, `weight`) VALUES ('" + str(wp_id) + "', '" + str(int(time.time())) + "', '" + str(now.hour) + "', 'read', 'show_last', '" + str(item["id"]) + "', '', '" + str(item["title"]) + "', '', 'data_1=>read_id, data_3=>read_title', '');"
            
            with mysql_connection.cursor() as cursor:
                cursor.execute(mysql_query)
                
        mysql_connection.commit()



    start_response('200 OK', [('Content-Type','text/html')])
    out_s = json.dumps(out_s)
    b = out_s.encode('utf-8')
    return [b]


