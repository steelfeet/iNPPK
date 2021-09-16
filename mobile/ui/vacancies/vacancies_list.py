import requests, json, traceback, urllib
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty



class VacanciesList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['action'] = "show_vacancy"
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        db_json = db_json.replace(" ", "")
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/mobile_vacancies.wsgi?q=" + str(db_json)
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print("response: " + t.text)

        items_list = json.loads(t.text)
        vacancies = items_list["vacancies"]
        print("vacancies[0]: " + vacancies[0])
        
        #выводим на активити
        self.ids.title_0.text = vacancies[0]["title"]
        self.ids.href_0.text = vacancies[0]["href"]

        self.ids.title_1.text = vacancies[1]["title"]
        self.ids.href_1.text = vacancies[1]["href"]

        self.ids.title_2.text = vacancies[2]["title"]
        self.ids.href_2.text = vacancies[2]["href"]

        self.ids.title_3.text = vacancies[3]["title"]
        self.ids.href_3.text = vacancies[3]["href"]

        self.ids.title_4.text = vacancies[4]["title"]
        self.ids.href_4.text = vacancies[4]["href"]
        