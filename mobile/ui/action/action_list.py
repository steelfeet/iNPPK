import os, requests, json, re, traceback

from datetime import datetime


from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class ActionList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        global selected_pop

        db_request = {}
        db_request['code'] = 'actions'
        db_request['action'] = 'last'
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
        items_list = json.loads(t.text)
        items_list_last = items_list["last"]

        try:
            item = items_list_last[0]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_1.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']
        
            item = items_list_last[1]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_2.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']

            item = items_list_last[2]
            dt_object = datetime.fromtimestamp(int(item['date']))
            self.ids.title_3.text = dt_object.strftime("%d %b %H:%M") + " - " + item['data_3']

        except:
            pass

        
        #рекомендация
        items_dict_rec = items_list["rec"]
        print()
        print("items_dict_rec:")
        print(items_dict_rec)
        items_list_rec = list(items_dict_rec)
        print()
        print("items_list_rec:")
        print(items_list_rec)


        self.ids.title_reccom_0.text = items_list_rec[0]
        self.ids.title_reccom_1.text = items_list_rec[1]
        self.ids.title_reccom_2.text = items_list_rec[2]


        #популярное
        self.ids.action_text.text = selected_pop



    def add_action(self):
        action_text = self.ids.action_text.text
        db_request = {}
        db_request['code'] = 'actions'
        db_request['action'] = 'add'
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

        self.ids.action_text.text = ""

        self.on_enter()