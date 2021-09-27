import os, requests, json, re, traceback
import ast
import time
import math

from datetime import datetime
from functools import partial

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock
Clock.max_iteration = 20

from kivy.config import ConfigParser
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')


from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp

from kivymd.uix.label import MDLabel


Builder.load_file('ui.kv')

dishes_list = []
result_type = 0

def toFixed(numObj, digits=2):
    numObj = float(numObj)
    return float(f"{numObj:.{digits}f}")

class IncrediblyCrudeClock():
    def update(self, elem, *largs):
        now = datetime.now()
        elem.text = now.strftime("%H:%M")
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_once(partial(crudeclock.update, elem), -1)




class SettingsList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        try:
            MainApp.get_running_app().screen_manager.get_screen("settings_list").ids.tm_id.text = self._app.user_data["tm_id"]
        except:
            pass
        
        try:
            MainApp.get_running_app().screen_manager.get_screen("settings_list").ids.vk_id.text = self._app.user_data["vk_id"]
        except:
            pass

        try:
            MainApp.get_running_app().screen_manager.get_screen("settings_list").ids.is_model.active = self._app.user_data["is_model"]
        except:
            pass

        try:
            MainApp.get_running_app().screen_manager.get_screen("settings_list").ids.is_prod.active = self._app.user_data["is_prod"]
        except:
            pass



    def save_settings(self):
        self._app.user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        self._app.user_data["tm_id"] = self.ids.tm_id.text
        self._app.user_data["vk_id"] = self.ids.vk_id.text
        self._app.user_data["is_model"] = self.ids.is_model.active
        self._app.user_data["is_prod"] = self.ids.is_prod.active

        self._app.config.set('General', 'user_data', self._app.user_data)
        self._app.config.write()

        print(self._app.user_data)
        MainApp.get_running_app().screen_manager.current = 'menu'




#загружаем activity "Дневник питания"
basedir = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(basedir, "ui/dish/dish_list.py"), "rt", encoding="utf-8").read())

#загружаем activity "Дневник питания"
basedir = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(basedir, "ui/dish/photo_food_camera.py"), "rt", encoding="utf-8").read())



#загружаем activity "Дневник событий"
basedir = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(basedir, "ui/action/action_list.py"), "rt", encoding="utf-8").read())


#загружаем activity "Читательский дневник"
basedir = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(basedir, "ui/read/read_list.py"), "rt", encoding="utf-8").read())


#загружаем activity "Вакансии"
basedir = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(basedir, "ui/vacancies/vacancies_list.py"), "rt", encoding="utf-8").read())



class ResultList(Screen):
    _app = ObjectProperty()
    def add_result(self, res):
        global result_type
        result_type = res
        MainApp.get_running_app().screen_manager.current = 'add_result'


class AddResult(Screen):
    _app = ObjectProperty()
    def save_result(self, ball):
        global result_type
        
        db_request = {}
        db_request['code'] = 'add_result'
        db_request['action'] = 'add_result'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(result_type)
        db_request['data_2'] = int(ball)
        db_request['data'] = "data_1=>result_type; data_2=>ball;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)
        
        
        MainApp.get_running_app().screen_manager.current = 'result_list'




class MainApp(MDApp):
    def __init__(self, **kvargs):
        super(MainApp, self).__init__(**kvargs)
        self.config = ConfigParser()
        #self.user_data = {}
        self.screen_manager = Factory.ManagerScreens()

    def callback(self):
        #self.screen_manager.add_widget(SettingsList(name="settings_list"))
        self.screen_manager.current = "settings_list"


    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def get_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'inppk.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(MainApp, self).get_application_config(
            'inppk.ini'.format(self.directory))

    def build(self):
        self.root = Factory.MenuScreen()
        self.theme_cls.primary_palette = "Blue"
        self.get_value_from_config()

        return self.screen_manager

    def on_start(self):
        crudeclock = IncrediblyCrudeClock()
        lbl = self.screen_manager.get_screen("menu").ids.toolbar_clock
        #Clock.schedule_once(partial(crudeclock.update, lbl), -1)

if __name__ == '__main__':
    MainApp().run()