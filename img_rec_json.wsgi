import os, json, sys, subprocess, time, cgi
form = cgi.FieldStorage()
print(form)

virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))


from google.oauth2 import service_account
from google.cloud import vision

from urllib.parse import parse_qs

ext_s = str(print(os.getenv))


def application(env, start_response):
 
    out_s = ""
    json_s = ""
    #Загрузка данных
    json_filename = os.path.dirname(os.path.abspath(__file__)) + "/full_data.json"
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
    
   
    out_s += "Всего рецептов: " + str(len(full_data)) + "<br>"
    
    #статистика меток
    stat_filename = os.path.dirname(os.path.abspath(__file__)) + "/stat.json"
    try:
        with open(stat_filename, "r", encoding="utf-8") as f:
            label_stats = json.load(f)
        out_s += "Загружено из "+ stat_filename.replace("/home/users/i/id35114350/domains/studs.steelfeet.ru/_hack/2020-21/world-it-planet/", "") + ": " + str(len(label_stats))
    except Exception as e:
        out_s += "Файл " + str(stat_filename) + " не загружен"
        out_s += str(e)
    out_s += "<br>"

    out_s += "Всего меток: " + str(len(label_stats)) + "<br>"


    
    """
    булочка
    https://eda.ru/img/eda/c620x415i/s2.eda.ru/StaticContent/Photos/120213182735/120213182923/p_O.jpg
    https://www.vkusnyblog.ru/wp-content/uploads/2009/02/assorted-buns-450x600.jpg
    https://www.koolinar.ru/all_image/recipes/107/107078/recipe_38b71ad5-c00f-4f60-b132-649fcc0ea18b.jpg

    борщ
    https://cdn.lifehacker.ru/wp-content/uploads/2014/12/ob-05_1568611223.jpg
    https://img.povar.ru/main/ab/23/b4/9c/samii_vkusnii_borsh-404089.jpg
    https://2recepta.com/recept/borshh/borshh.jpg

    """
    
    #получаем переданную строку
    d = os.environ.get("SERVER_NAME")
    
    #image_uri = d.get('image_uri', [])
    #image_uri  = escape(image_uri)
    out_s = ext_s

    #отдаем на распознавание другому процессу
    queue_dict ={}
    queue_dict['type'] = "href"
    #queue_dict['image_uri'] = image_uri
    queue_dict['time'] = int(time.time())
    current_filename = os.path.dirname(os.path.abspath(__file__)) + "/current.json"
    with open(current_filename, "w", encoding="utf-8") as file:
        json.dump(queue_dict, file, indent=4, ensure_ascii=False)
    
    t = subprocess.call('python3.8 ~/domains/studs.steelfeet.ru/_hack/2020-21/world-it-planet/img_recognize.py', shell=True)

    #немножко подождем
    time.sleep(3)
    
    try:
        with open(current_filename, "r", encoding="utf-8") as f:
            queue_dict = json.load(f)
            if (queue_dict["status"] == "Ok"):
                source_labels = queue_dict["labels"]
                out_s += "Загружены распознанные метки   " + ": " + str(len(source_labels)) + "<br>"
                out_s += "<ul>"
                for source_label in source_labels:
                    out_s += "<li>" + source_label + ": " + str(label_stats[source_label])
                out_s += "</ul>"

                #непосредственно распознавание: выбираем пять наиболее подходящих рецепта
                for dish in full_data:
                    label_annotations = dish["label_annotations"]
                    label_annotations += dish["web_entities"]

                    dish_weight = 0.5
                    for item in label_annotations:
                        if (item in source_labels):
                            if (label_stats[item] > 0):
                                this_weight = label_stats[item]
                                dish_weight = dish_weight * this_weight / (dish_weight*this_weight + (1-dish_weight)*(1-this_weight))
                                
                    if (dish_weight == 1):
                        dish_weight = 0

                    full_data["dish_weight"] = dish_weight


                #сортируем
                sorted_dict = sorted(full_data.items(), key=lambda x: x["dish_weight"])   
                #json_s = str(json.dumps(sorted_dict[:4]))
                json_s = json.dumps(label_annotations)


            else:
                #out_s += "Error: " + queue_dict["status"]
                pass
    except Exception as e:
        pass

    start_response('200 OK', [('Content-Type','text/json; charset=utf-8')])
    b = out_s.encode('utf-8')
    return [b]