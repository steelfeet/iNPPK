import requests, json, traceback, urllib
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty



class VacanciesList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = "vacancy"
        db_request['action'] = "show"
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        db_json = db_json.replace(" ", "")
        print(db_json)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/mobile_vacancies.wsgi?q=" + str(db_json)
        print(page_url)
        t = requests.get(page_url, headers = headers)

        items_list = json.loads(t.text)
        words = items_list["words"]
        words = dict(sorted(words.items(), key=lambda item: item[1]))
        print("words:")
        print(words)

        vacancies = items_list["vacancies"]
        print("vacancies:")
        print(vacancies)
        
        #разбиваем title на две строчки
        good_titles = []   
        for item in vacancies:
            words = item["title"].split(" ")
            
            good_title = ""
            next_br = True
            for word in words:
                good_title = good_title + word + " "
                if (len(good_title) > 20):
                    if (next_br):
                        good_title = good_title + "\n"
                        next_br = False
                        if (len(good_title) > 40):
                            #good_title = re.sub(r'[а-я]+\s?', '',good_title).strip()
                            break
            
            good_titles.append(good_title.strip())


        #выводим на активити
        self.ids.title_0.text = good_titles[0]
        #self.ids.href_0.text = vacancies[0]["href"]

        self.ids.title_1.text = good_titles[1]
        #self.ids.href_1.text = vacancies[1]["href"]

        self.ids.title_2.text = good_titles[2]
        #self.ids.href_2.text = vacancies[2]["href"]

        self.ids.title_3.text = good_titles[3]
        #self.ids.href_3.text = vacancies[3]["href"]

        self.ids.title_4.text = good_titles[4]
        #self.ids.href_4.text = vacancies[4]["href"]
        