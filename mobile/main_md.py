from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

Builder.load_file('ui_md.kv')



class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Рекомендации для студентов"
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager = Factory.ManagerScreens()

    def build(self):
        self.root = Factory.MenuScreen()
        return self.screen_manager

class SortedListFood(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Дневник питания"
        self.theme_cls.primary_palette = "Blue"


class AddFood(Screen):
    _app = ObjectProperty()


if __name__ == "__main__":
    MainApp().run()