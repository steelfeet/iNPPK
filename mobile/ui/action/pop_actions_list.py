import os, requests, json, re, traceback

from datetime import datetime


from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

titles_id = {}


class PopActionsList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        titles_id.clear

        db_request = {}
        db_request['code'] = 'actions'
        db_request['action'] = 'pop'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print()
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print()
        print(t.text)

        try:
            items_list = json.loads(t.text)
            items_list_pop = items_list["pop"]
            pop_keys = list(items_list_pop)

            n = 0
            for pop_action in pop_keys:
                titles_id[n] = pop_action
                n = n + 1


            self.ids.title_0.text = pop_keys[0]
            self.ids.title_1.text = pop_keys[1]
            self.ids.title_2.text = pop_keys[2]
            self.ids.title_3.text = pop_keys[3]
            self.ids.title_4.text = pop_keys[4]


        except:
            pass

        
    def add_pop(self, title_n):
        global selected_pop
        selected_pop = str(titles_id[title_n])
        MainApp.get_running_app().screen_manager.current = 'action_list'


