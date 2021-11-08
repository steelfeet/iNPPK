import urllib3,charset_normalizer,idna,PIL
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


from kivy.config import ConfigParser
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')


from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp

from kivymd.uix.label import MDLabel


#нажимающееся изображение
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class ImageButton(ButtonBehavior, Image):
    pass



Builder.load_file('ui.kv')

#переменные, глобальные между окнами
dishes_list = []
result_type = 0
selected_pop = ""
wp_id = 0


def toFixed(numObj, digits=2):
    numObj = float(numObj)
    return float(f"{numObj:.{digits}f}")





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

        #проверка наличия логина ТМ или ВК
        
        try:
            if (len(self._app.user_data["tm_id"]) < 1) and (len(self._app.user_data["vk_id"]) < 1):
                MainApp.get_running_app().screen_manager.get_screen("settings_list").ids.mdl_notify.text = "Введите данные для авторизации"
            else:
                db_request = {}
                db_request['action'] = 'show_wp_id'
                db_request['tm_id'] = self._app.user_data["tm_id"]
                db_request['vk_id'] = self._app.user_data["vk_id"]
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
                db_json = json.dumps(db_request)
                page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
                t = requests.get(page_url, headers = headers)
                
                if (t.text.isdigit):
                    self.ids.mdl_notify.text = "Авторизация успешна. WP_ID:" + t.text
                    wp_id = int(t.text)

                else:
                    self.ids.mdl_notify.text = "Неавторизован. WP_ID:" + t.text

        except:
            self.ids.mdl_notify.text = "Введите данные для авторизации"




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
#exec(open(os.path.join(basedir, "ui/dish/dish_list.py"), "rt", encoding="utf-8").read())
class DishList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        try:
            if (len(self._app.user_data["tm_id"]) < 1) and (len(self._app.user_data["vk_id"]) < 1):
                self._app.screen_manager.current = 'settings_list'
            else:
                db_request = {}
                db_request['code'] = 'dish'
                db_request['action'] = 'last'
                db_request['tm_id'] = self._app.user_data["tm_id"]
                db_request['vk_id'] = self._app.user_data["vk_id"]
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
                db_json = json.dumps(db_request)
                if (self._app.user_data["is_model"]):
                    page_url = "https://steelfeet.ru/app/get_1.php?q=" + db_json
                else:
                    page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
                print("запрос последних: " + page_url)
                t = requests.get(page_url, headers = headers)


                #рекомендация
                try:
                    items_list = json.loads(t.text)
                    wp_id = items_list["wp_id"]

                    items_list_last = items_list["rec"]

                    dish = items_list_last[0]
                    source = str(dish['image_uri']).replace("\\", "")
                    self.ids.image_reccom_0.source = source
                    self.ids.title_reccom_0.text = dish['title'][:21]

                    dish = items_list_last[1]
                    source = str(dish['image_uri']).replace("\\", "")
                    self.ids.image_reccom_1.source = source
                    self.ids.title_reccom_1.text = dish['title'][:21]

                    dish = items_list_last[2]
                    source = str(dish['image_uri']).replace("\\", "")
                    self.ids.image_reccom_2.source = source
                    self.ids.title_reccom_2.text = dish['title'][:21]

                except Exception as e:
                    print(traceback.format_exc())




            #последние
            try:
                items_list = json.loads(t.text)
                items_list_last = items_list["last"]

                dish = items_list_last[0]
                source = str(dish['image_uri']).replace("\\", "")
                self.ids.image_0.source = source
                self.ids.title_0.text = dish['title'][:21]

                dish = items_list_last[1]
                source = str(dish['image_uri']).replace("\\", "")
                self.ids.image_1.source = source
                self.ids.title_1.text = dish['title'][:21]

                dish = items_list_last[2]
                source = str(dish['image_uri']).replace("\\", "")
                self.ids.image_2.source = source
                self.ids.title_2.text = dish['title'][:21]

            except Exception as e:
                print(traceback.format_exc())

        except:
            self._app.screen_manager.current = 'settings_list'







    #выбираем показ камеры или текстового поля для ввода ссылки на картинку
    def select_prod(self):
        if (self._app.user_data["is_prod"]):
            self._app.screen_manager.current = 'photo_food_camera'
        else:
            self._app.screen_manager.current = 'photo_food_imuri'
















class PhotoFoodUri(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        self.ids.photo_emulation.text = ""

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
        self.ids.title_1.text = dish['title'][:20]
        #self.ids.data_1.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[1]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_2.source = source
        self.ids.title_2.text = dish['title'][:20]
        #self.ids.data_2.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[2]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_3.source = source
        self.ids.title_3.text = dish['title'][:20]
        #self.ids.data_3.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[3]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_4.source = source
        self.ids.title_4.text = dish['title'][:20]
        #self.ids.data_4.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."

        dish = dishes_list[4]
        source = str(dish['image_uri']).replace("\\", "")
        self.ids.rec_im_5.source = source
        self.ids.title_5.text = dish['title'][:20]
        #self.ids.data_5.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."



    def select_dish(self, dish_n ):
        dish_id = dishes_list[dish_n]['id']
        db_request = {}
        db_request['code'] = 'dish'
        db_request['action'] = 'add'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(dish_id)
        db_request['data'] = "data_1=>dish_id;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        print(page_url)
        t = requests.get(page_url, headers = headers)
        print(t.text)

        MainApp.get_running_app().screen_manager.current = 'dish_list'


class DishList2(Screen):
    _app = ObjectProperty()

#загружаем activity "Дневник питания"
#exec(open(os.path.join(basedir, "ui/dish/photo_food_camera.py"), "rt", encoding="utf-8").read())
class CameraClick(BoxLayout):
    pass


class PhotoFoodCamera(Screen):
    _app = ObjectProperty()

    def capture(self):
        global dishes_list, wp_id
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image_filename = "IMG_{}.png".format(timestr)
        camera.export_to_png(image_filename)
        print("Captured: " + image_filename)

        #https://stackoverflow.com/questions/29104107/upload-image-using-post-form-data-in-python-requests
        api_url = "https://steelfeet.ru/app/dish_photo.php"
        with open(image_filename, "rb") as f:
            im_bytes = f.read()        
        im_b64 = base64.b64encode(im_bytes).decode("utf8")
        
        
        payload = {"im_b64": im_b64, 'wp_id': wp_id}
        
        dishes_json = requests.post(api_url, data=payload)
        print("response: ")
        print(dishes_json.text)

        os.remove(image_filename)
        try:
            dishes_list = json.loads(dishes_json.text)
        except:
            pass
        MainApp.get_running_app().screen_manager.current = 'photo_food_rec'







#загружаем activity "Дневник событий"
#exec(open(os.path.join(basedir, "ui/action/action_list.py"), "rt", encoding="utf-8").read())
#exec(open(os.path.join(basedir, "ui/action/pop_actions_list.py"), "rt", encoding="utf-8").read())
class ActionList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        global selected_pop, wp_id
        if ((len(self._app.user_data["tm_id"]) < 1) and (len(self._app.user_data["vk_id"]) < 1)):
            self._app.screen_manager.current = 'settings_list'
        else:

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

            except:
                pass


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



#загружаем activity "Читательский дневник"
#exec(open(os.path.join(basedir, "ui/read/read_list.py"), "rt", encoding="utf-8").read())
import webbrowser




titles_id = {}
items_hrefs = {}


class ReadList(Screen):
    _app = ObjectProperty()
    
    def reload(self):
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/next_read.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)
        try:
            items_list = json.loads(t.text)
            exist_vacancies_query = items_list["exist_vacancies_query"]
            print()
            print("exist_vacancies_query")
            print(exist_vacancies_query)
        except:
            print()

        self.on_enter()    
    
    def on_enter(self):
        try:
            if (len(self._app.user_data["tm_id"]) < 1) and (len(self._app.user_data["vk_id"]) < 1):
                self._app.screen_manager.current = 'settings_list'
            else:
                db_request = {}
                db_request['code'] = 'read'
                db_request['action'] = 'show'
                db_request['tm_id'] = self._app.user_data["tm_id"]
                db_request['vk_id'] = self._app.user_data["vk_id"]
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
                db_json = json.dumps(db_request)
                
                page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/best_read.wsgi?q=" + str(db_json)
                t = requests.get(page_url, headers = headers)

                try:
                    items_list = json.loads(t.text)
                    links = items_list["reads"]
                    print()
                    print(items_list["words"])

                except:
                    print(t.text)
                
                #разбиваем title на две строчки
                n = 0
                good_titles = []   
                for item in links:
                    words = item["title"].split(" ")


                    good_title = ""
                    next_br = True
                    for word in words:
                        good_title = good_title + word + " "
                        if len(good_title) > 50:
                            break
                        if (len(good_title) > 25):
                            if (next_br):
                                good_title = good_title + "\n"
                                next_br = False
                                


                                
                                
                    
                    good_titles.append(good_title)
                    titles_id[n] = item["id"]
                    items_hrefs[n] = item["href"]
                    n = n + 1
                
                #выводим на активити
                self.ids.title_0.text = good_titles[0]
                #self.ids.href_0.text = links[0]["href"]

                self.ids.title_1.text = good_titles[1]
                #self.ids.href_1.text = links[1]["href"]

                self.ids.title_2.text = good_titles[2]
                #self.ids.href_2.text = links[2]["href"]

                self.ids.title_3.text = good_titles[3]
                #self.ids.href_3.text = links[3]["href"]

                self.ids.title_4.text = good_titles[4]
                #self.ids.href_4.text = links[4]["href"]















                page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/last_read.wsgi?q=" + str(db_json)
                t = requests.get(page_url, headers = headers)

                items_list = json.loads(t.text)
                links = items_list["reads"]
                
                
                #разбиваем title на две строчки
                for item in links:
                    words = item["title"].split(" ")

                    good_title = ""
                    next_br = True
                    for word in words:
                        good_title = good_title + word + " "
                        if len(good_title) > 50:
                            break
                        if (len(good_title) > 25):
                            if (next_br):
                                good_title = good_title + "\n"
                                next_br = False
                                
                    
                    good_titles.append(good_title)
                    titles_id[n] = item["id"]
                    items_hrefs[n] = item["href"]
                    n = n + 1
                
                #выводим на активити
                self.ids.title_5.text = good_titles[5]
                #self.ids.href_0.text = links[0]["href"]

                self.ids.title_6.text = good_titles[6]
                #self.ids.href_1.text = links[1]["href"]

                self.ids.title_7.text = good_titles[7]
                #self.ids.href_2.text = links[2]["href"]

                self.ids.title_8.text = good_titles[8]
                #self.ids.href_3.text = links[3]["href"]

                self.ids.title_9.text = good_titles[9]
                #self.ids.href_4.text = links[4]["href"]

        except:
            self._app.screen_manager.current = 'settings_list'









    def like_read(self, title_n):
        global titles_id
        try:
            print("read id:" + str(titles_id[title_n]))
            db_request = {}
            db_request['action'] = 'like_read'
            db_request['tm_id'] = self._app.user_data["tm_id"]
            db_request['vk_id'] = self._app.user_data["vk_id"]
            db_request['data_1'] = int(titles_id[title_n])
            db_request['data'] = "data_1=>read_id;"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            db_json = json.dumps(db_request, ensure_ascii=False)
            page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
            t = requests.get(page_url, headers = headers)

        except:
            print("titles_id:")
            print(titles_id)
        

    def dislike_read(self, title_n):
        global titles_id
        print("read id:" + str(titles_id[title_n]))
        
        db_request = {}
        db_request['action'] = 'dislike_read'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(titles_id[title_n])
        db_request['data'] = "data_1=>read_id;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        t = requests.get(page_url, headers = headers)



    def go_href(self, title_n):
        global items_hrefs
        print("read_href:" + str(items_hrefs[title_n]))
        webbrowser.open_new(str(items_hrefs[title_n]))


#загружаем activity "Вакансии"
#exec(open(os.path.join(basedir, "ui/vacancies/vacancies_list.py"), "rt", encoding="utf-8").read())
titles_id = {}
items_hrefs = {}


class VacanciesList(Screen):
    _app = ObjectProperty()


    def reload(self):
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/next_vacancies.wsgi?q=" + str(db_json)
        requests.get(page_url, headers = headers)
        self.on_enter()


    def on_enter(self):
        try:
            if (len(self._app.user_data["tm_id"]) < 1) and (len(self._app.user_data["vk_id"]) < 1):
                self._app.screen_manager.current = 'settings_list'
        except:
            self._app.screen_manager.current = 'settings_list'

        titles_id.clear
        #self.add_widget(ImageButton())
        print()
        db_request = {}
        db_request['action'] = "show"
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        db_json = db_json.replace(" ", "")
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/best_vacancies.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)

        items_list = json.loads(t.text)
        try:
            words = items_list["words"]
            words = dict(sorted(words.items(), key=lambda item: item[1]))
            print("words:")
            print(words)
        except:
            pass

        vacancies = items_list["vacancies"]
        print("vacancies:")
        print(vacancies)

        #разбиваем title на две строчки
        good_titles = []
        n = 0   
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
            titles_id[n] = item["id"]
            items_hrefs[n] = item["href"]
            n = n + 1


        
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





        db_request = {}
        db_request['action'] = "show"
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        
        #отдельный бекенд для вакансий, т.к. он на Python для поиска подходящих вакансий
        page_url = "https://studs.steelfeet.ru/_hack/2020-21/world-it-planet/847-hh-scrapper/last_vacancies.wsgi?q=" + str(db_json)
        t = requests.get(page_url, headers = headers)
        items_list = json.loads(t.text)
        vacancies = items_list["vacancies"]
        
        #разбиваем title на две строчки
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
            titles_id[n] = item["id"]
            items_hrefs[n] = item["href"]
            n = n + 1


        
        #выводим на активити
        self.ids.title_5.text = good_titles[5]
        #self.ids.href_0.text = vacancies[0]["href"]

        self.ids.title_6.text = good_titles[6]
        #self.ids.href_1.text = vacancies[1]["href"]

        self.ids.title_7.text = good_titles[7]
        #self.ids.href_2.text = vacancies[2]["href"]

        self.ids.title_8.text = good_titles[8]
        #self.ids.href_3.text = vacancies[3]["href"]

        self.ids.title_9.text = good_titles[9]
        #self.ids.href_4.text = vacancies[4]["href"]



    def like_vacancy(self, title_n):
        global titles_id
        try:
            print("vakancy id:" + str(titles_id[title_n]))
            db_request = {}
            db_request['action'] = 'like_vacancy'
            db_request['tm_id'] = self._app.user_data["tm_id"]
            db_request['vk_id'] = self._app.user_data["vk_id"]
            db_request['data_1'] = int(titles_id[title_n])
            db_request['data'] = "data_1=>vacancy_id;"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            db_json = json.dumps(db_request, ensure_ascii=False)
            page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
            t = requests.get(page_url, headers = headers)

        except:
            print("titles_id:")
            print(titles_id)
        

    def dislike_vacancy(self, title_n):
        global titles_id
        print("vakancy id:" + str(titles_id[title_n]))
        
        db_request = {}
        db_request['action'] = 'dislike_vacancy'
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        db_request['data_1'] = int(titles_id[title_n])
        db_request['data'] = "data_1=>vacancy_id;"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request, ensure_ascii=False)
        page_url = "https://steelfeet.ru/app/get.php?q=" + db_json
        t = requests.get(page_url, headers = headers)



    def go_href(self, title_n):
        global items_hrefs
        webbrowser.open_new(str(items_hrefs[title_n]))



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


    def build(self):
        self.root = Factory.MenuScreen()
        self.theme_cls.primary_palette = "Blue"
        self.get_value_from_config()

        return self.screen_manager

    def on_start(self):
        lbl = self.screen_manager.get_screen("menu").ids.toolbar_clock
        #Clock.schedule_once(partial(crudeclock.update, lbl), -1)

if __name__ == '__main__':
    MainApp().run()