import os, json, sys

def application(env, start_response):
 
    out_s = "Вы используете Python {}.{}.".format(sys.version_info.major, sys.version_info.minor) + "<br>"
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
    
    out_s += "Всего: " + str(len(full_data)) + "<br>"
    
    #полсчет статистики меток
    label_stats = {}
    summ_label = 0
    for data in full_data:
        label_annotations = data["label_annotations"]
        for label in label_annotations:
            try:
                label_stats[label] = label_stats[label] + 1
            except:
                label_stats[label] = 1
                summ_label += 1

        label_annotations = data["web_entities"]
        for label in label_annotations:
            try:
                label_stats[label] = label_stats[label] + 1
            except:
                label_stats[label] = 1
                summ_label += 1

    out_s += "Всего меток: " + str(summ_label) + "<br>"

    for label in label_stats:
        weight = label_stats[label] / summ_label
        #метка встречается более одного раза в одной картинке
        if (weight > 1):
            weight = 1
        weight = 1 - weight

        label_stats[label] = weight
        if (weight > 0.5):
            out_s += "<li>" + str(label) + ": " + str(weight)

    stat_filename = os.path.dirname(os.path.abspath(__file__)) + "/stat.json"
    with open(stat_filename, "w", encoding="utf-8") as file:
        json.dump(label_stats, file, indent=4, ensure_ascii=False)


    
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
    
    """
    #распознаем изображение
    credentials_file = os.path.dirname(os.path.abspath(__file__)) +  "/vision-nppk-25a4b3ee922c.json"
    print(credentials_file)
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image_uri = "https://eda.ru/img/eda/c620x415i/s2.eda.ru/StaticContent/Photos/120213182735/120213182923/p_O.jpg"
    response = client.annotate_image({'image': {'source': {'image_uri': image_uri}},  'features': [],})
    
    image_annotations = []
    for label in response.label_annotations:
        desc = str(label.description)
        image_annotations.append(desc)
    for label in response.web_detection.web_entities:
        desc = str(label.description)
        image_annotations.append(desc)
    for label in image_annotations:
        out_s += "<li>" + str(label)


    for data in full_data:
        label_annotations = data["label_annotations"]
    """

    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    b = out_s.encode('utf-8')
    return [b]