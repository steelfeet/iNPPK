import os, requests, json, re, traceback
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class ActionList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'last_actions'
        db_request['action'] = ''
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)
        items_list_now = json.loads(t.text)

        try:
            item = items_list_now[0]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_1.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']
        
            item = items_list_now[1]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_2.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']

            item = items_list_now[2]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_3.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']

            item = items_list_now[3]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_4.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']

            item = items_list_now[4]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_5.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']
        except:
            pass

        
        #рекомендация
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/reccom_action.php?q=" + db_json
        print("запрос рекомендации: " + page_url)
        t = requests.get(page_url, headers = headers)
            
        try:
            item = json.loads(t.text)
            self.ids.title_reccom.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']
        except Exception as e:
            print(traceback.format_exc())



    def add_action(self):
        action_text = self.ids.action_text.text
        db_request = {}
        db_request['code'] = 'add_action'
        db_request['action'] = 'add_action'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_3'] = str(action_text)
        db_request['data'] = "data_3=>action_text;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        self.on_enter()