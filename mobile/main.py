import os
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


class IncrediblyCrudeClock():
    def update(self, elem, *largs):
        now = datetime.now()
        elem.text = now.strftime("%H:%M")
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_once(partial(crudeclock.update, elem), -1)






class DishList(Screen):
    def on_enter(self):
        data_foods = self.get_data_foods()
        self.set_list_foods(data_foods)

    def get_data_foods(self):
        return ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

    def set_list_foods(self, data_foods):
        for f, d in sorted(data_foods.items(), key=lambda x: x[1]):
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime(
                '%Y-%m-%d'))
            data = {'viewclass': 'Button', 'text': fd}
            if data not in self.ids.rv.data:
                self.ids.rv.data.append({'viewclass': 'Button', 'text': fd})


class PhotoFood(Screen):
    _app = ObjectProperty()

class PhotoFoodRec(Screen):
    _app = ObjectProperty()

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
        self.screen_manager = Factory.ManagerScreens()
        self.user_data = {}

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def get_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(MainApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

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