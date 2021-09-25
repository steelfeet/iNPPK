import os, requests, json, re, traceback
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class ReadList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'read'
        db_request['action'] = 'show'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)

        #отдельный бекенд для ссылок, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/mobile_read.wsgi?q=" + str(db_json)

        print("page_url: " + page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        items_list = json.loads(t.text)
        links = items_list["links"]

        
        #разбиваем title на две строчки
        good_titles = []
        for link in links:
            words = []
            words = link["title"]
            print("link[title] = " + link["title"])
            words = link["title"].split(" ")
            print(words)
            
            good_title = ""
            next_br = True
            for word in words:
                good_title = good_title + word + " "
                print(good_title)
                if (len(good_title) > 30):
                    if (next_br):
                        good_title = good_title + "\n"
                        next_br = False

            good_titles.append(good_title)
        
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