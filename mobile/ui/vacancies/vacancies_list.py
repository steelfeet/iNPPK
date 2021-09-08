import requests, json, traceback
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty



class VacanciesList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'last_vacancies'
        db_request['action'] = ''
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        try:
            items_list_now = json.loads(t.text)
            item = items_list_now[0]
            self.ids.title_1.text = item['data_4'][:30]
            self.ids.href_1.text = item['data_3']
        except:
            pass

        #рекомендация
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/reccom_read.php?q=" + db_json
        print("запрос рекомендации: " + page_url)
        t = requests.get(page_url, headers = headers)
            
        try:
            item = json.loads(t.text)
            self.ids.title_1.title_reccom = item['data_4']
            self.ids.href_1.title_reccom = item['data_3']
        except Exception as e:
            print(traceback.format_exc())

    def add_href(self):
        href_text = self.ids.href_text.text
        db_request = {}
        db_request['code'] = 'add_read'
        db_request['action'] = ''
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_3'] = str(href_text)
        db_request['data'] = "data_3=>href_text; data_4=>title"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        self.on_enter()