import os, requests, json, re, traceback
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


titles_id = {}
showed_items_ids = []
showed_items = []


class ReadList(Screen):
    _app = ObjectProperty()
    
    def reload(self):
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['showed_read'] = showed_items
        print()
        print(showed_items_ids)
        print()
        print(showed_items)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/next_read.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)
        try:
            items_list = json.loads(t.text)
            exist_vacancies_query = items_list["exist_vacancies_query"]
            print()
            print("exist_vacancies_query")
            print(exist_vacancies_query)
        except:
            print()

        showed_items_ids.clear
        showed_items.clear

        self.on_enter()    
    
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'read'
        db_request['action'] = 'show'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/best_read.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)

        try:
            items_list = json.loads(t.text)
            links = items_list["reads"]
            print()
            print(items_list["words"])

            print()
            print("showed_read_ids")
            print(items_list["showed_read_ids"])

        except:
            print(t.text)
        
        #разбиваем title на две строчки
        n = 0
        good_titles = []   
        for item in links:
            words = item["title"].split(" ")

            if (int(item["id"]) not in showed_items_ids):
                showed_item = {}
                showed_item["title"] = item["title"]
                showed_item["id"] = item["id"]
                showed_items_ids.append(int(item["id"]))
                showed_items.append(showed_item)

            good_title = ""
            next_br = True
            for word in words:
                good_title = good_title + word + " "
                if len(good_title) > 50:
                    break
                if (len(good_title) > 25):
                    if (next_br):
                        good_title = good_title + "\n"
                        next_br = False
                         


                        
                        
            
            good_titles.append(good_title)
            titles_id[n] = item["id"]
            n = n + 1
        
        #выводим на активити
        self.ids.title_0.text = good_titles[0]
        #self.ids.href_0.text = links[0]["href"]

        self.ids.title_1.text = good_titles[1]
        #self.ids.href_1.text = links[1]["href"]

        self.ids.title_2.text = good_titles[2]
        #self.ids.href_2.text = links[2]["href"]

        self.ids.title_3.text = good_titles[3]
        #self.ids.href_3.text = links[3]["href"]

        self.ids.title_4.text = good_titles[4]
        #self.ids.href_4.text = links[4]["href"]















        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/last_read.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)

        items_list = json.loads(t.text)
        links = items_list["reads"]
        
        
        #разбиваем title на две строчки
        for item in links:
            words = item["title"].split(" ")

            if (int(item["id"]) not in showed_items_ids):
                showed_item = {}
                showed_item["title"] = item["title"]
                showed_item["id"] = item["id"]
                showed_items_ids.append(int(item["id"]))
                showed_items.append(showed_item)

            good_title = ""
            next_br = True
            for word in words:
                good_title = good_title + word + " "
                if len(good_title) > 50:
                    break
                if (len(good_title) > 25):
                    if (next_br):
                        good_title = good_title + "\n"
                        next_br = False
                        
            
            good_titles.append(good_title)
            titles_id[n] = item["id"]
            n = n + 1
        
        #выводим на активити
        self.ids.title_5.text = good_titles[5]
        #self.ids.href_0.text = links[0]["href"]

        self.ids.title_6.text = good_titles[6]
        #self.ids.href_1.text = links[1]["href"]

        self.ids.title_7.text = good_titles[7]
        #self.ids.href_2.text = links[2]["href"]

        self.ids.title_8.text = good_titles[8]
        #self.ids.href_3.text = links[3]["href"]

        self.ids.title_9.text = good_titles[9]
        #self.ids.href_4.text = links[4]["href"]











    def like_read(self, title_n):
        global titles_id
        try:
            print("read id:" + str(titles_id[title_n]))
            db_request = {}
            db_request['action'] = 'like_read'
            db_request['tm_id'] = self._app.user_data["tm_id"]
            db_request['vk_id'] = self._app.user_data["vk_id"]
            db_request['data_1'] = int(titles_id[title_n])
            db_request['data'] = "data_1=>read_id;"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            db_json = json.dumps(db_request, ensure_ascii=False)
            page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
            t = requests.get(page_url, headers = headers)

        except:
            print("titles_id:")
            print(titles_id)
        

    def dislike_read(self, title_n):
        global titles_id
        print("read id:" + str(titles_id[title_n]))
        
        db_request = {}
        db_request['action'] = 'dislike_read'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(titles_id[title_n])
        db_request['data'] = "data_1=>read_id;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        t = requests.get(page_url, headers = headers)

