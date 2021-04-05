import os, json, sys, subprocess, time
virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))


from google.oauth2 import service_account
from google.cloud import vision


def application(env, start_response):
 
    out_s = ""
    #Загрузка данных
    json_filename = os.path.dirname(os.path.abspath(__file__)) + "/calorizator.ru.json"
    if os.path.exists(json_filename):
            try:
                with open(json_filename, "r", encoding="utf-8") as f:
                    load_list = json.load(f)
                out_s += "Загружено из "+ json_filename + ": " + str(len(load_list))
            except Exception as e:
                load_list = []
                out_s += "Файл " + str(json_filename) + " не загружен"
                out_s += str(e)
    else:
        load_list = []
        out_s += "Файла "+ json_filename + " нет. Закачиваем новый"
    out_s += "<br>"
    full_data = load_list
    
    json_filename = os.path.dirname(os.path.abspath(__file__)) + "/1000.menu.json"
    if os.path.exists(json_filename):
            try:
                with open(json_filename, "r", encoding="utf-8") as f:
                    load_list = json.load(f)
                out_s += "Загружено из "+ json_filename + ": " + str(len(load_list))
            except Exception as e:
                load_list = []
                out_s += "Файл " + str(json_filename) + " не загружен"
                out_s += str(e)
    else:
        load_list = []
        out_s += "Файла "+ json_filename + " нет. Закачиваем новый"
    out_s += "<br>"
    full_data = full_data + load_list
    

    json_filename = os.path.dirname(os.path.abspath(__file__)) + "/daily-menu.ru.json"
    if os.path.exists(json_filename):
            try:
                with open(json_filename, "r", encoding="utf-8") as f:
                    load_list = json.load(f)
                out_s += "Загружено из "+ json_filename + ": " + str(len(load_list))
            except Exception as e:
                load_list = []
                out_s += "Файл " + str(json_filename) + " не загружен"
                out_s += str(e)
    else:
        load_list = []
        out_s += "Файла "+ json_filename + " нет. Закачиваем новый"
    out_s += "<br>"
    full_data = full_data + load_list
    
    out_s += "Всего рецептов: " + str(len(full_data)) + "<br>"
    

    n = 1
    id_full_data = []
    for dish in full_data:
        dish["id"] = n
        id_full_data.append(dish)
        n += 1

    fd_filename = os.path.dirname(os.path.abspath(__file__)) + "/full_data.json"
    with open(fd_filename, "w", encoding="utf-8") as file:
        json.dump(id_full_data, file, indent=4, ensure_ascii=False)


    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    b = out_s.encode('utf-8')
    return [b]