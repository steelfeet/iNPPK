import os, requests, json, re
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
    
    def save_settings(self):
        self._app.user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        self._app.user_data["tm_id"] = self.ids.tm_id.text
        self._app.user_data["vk_id"] = self.ids.vk_id.text

        self._app.config.set('General', 'user_data', self._app.user_data)
        self._app.config.write()

        print(self._app.user_data)
        MainApp.get_running_app().screen_manager.current = 'menu'





class DishList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'last_dish'
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

        dishes_list_now = json.loads(t.text)

        dish = dishes_list_now[0]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.image_1.source = source
        self.ids.title_1.text = dish['title']
        self.ids.data_1.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list_now[1]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.image_2.source = source
        self.ids.title_2.text = dish['title']
        self.ids.data_2.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list_now[2]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.image_3.source = source
        self.ids.title_3.text = dish['title']
        self.ids.data_3.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."



class PhotoFoodS1Uri(Screen):
    _app = ObjectProperty()

    def send_uri(self):
        global dishes_list
        uri = self.ids.photo_emulation.text
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        page_url = "https://steelfeet.ru/app/dish_rec.php?imageUri="+uri
        dishes_json = requests.get(page_url, headers = headers)

        dishes_list = json.loads(dishes_json.text)
        MainApp.get_running_app().screen_manager.current = 'photo_food_rec'
      




class PhotoFood(Screen):
    _app = ObjectProperty()



class PhotoFoodRec(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        dish = dishes_list[0]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_1.source = source
        self.ids.title_1.text = dish['title']
        self.ids.data_1.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[1]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_2.source = source
        self.ids.title_2.text = dish['title']
        self.ids.data_2.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[2]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_3.source = source
        self.ids.title_3.text = dish['title']
        self.ids.data_3.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[3]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_4.source = source
        self.ids.title_4.text = dish['title']
        self.ids.data_4.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[4]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_5.source = source
        self.ids.title_5.text = dish['title']
        self.ids.data_5.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."



    def select_dish(self, dish_n ):
        dish_id = dishes_list[dish_n]['id']
        db_request = {}
        db_request['code'] = 'add_action'
        db_request['action'] = 'add_dish'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(dish_id)
        db_request['data'] = "data_1=>dish_id;"
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        MainApp.get_running_app().screen_manager.current = 'dish_list'


class DishList2(Screen):
    _app = ObjectProperty()



class ReadList(Screen):
    _app = ObjectProperty()


class ActionList(Screen):
    _app = ObjectProperty()


class MusicList(Screen):
    _app = ObjectProperty()


class SleepingMode(Screen):
    _app = ObjectProperty()

class ToDoList(Screen):
    _app = ObjectProperty()


class ResultList(Screen):
    _app = ObjectProperty()

class AddResult(Screen):
    _app = ObjectProperty()




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