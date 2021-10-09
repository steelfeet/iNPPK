import os, requests, json, re, traceback
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class DishList(Screen):
    _app = ObjectProperty()
    def on_enter(self):
        db_request = {}
        db_request['code'] = 'last_dish'
        db_request['action'] = ''
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

        calories_color = ""
        try:
            response_json = json.loads(t.text)
            dishes_list_now = response_json["last"]
            calories_color = response_json["calories"]
            dish = dishes_list_now[0]
            source = str(dish['image_uri']).replace("\\", "")
            self.ids.image_1.source = source
            self.ids.title_1.text = dish['title'][:21]
            self.ids.data_1.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."
        except Exception as e:
            print(traceback.format_exc())

        try:
            dish = dishes_list_now[1]
            source = str(dish['image_uri']).replace("\\", "")
            self.ids.image_2.source = source
            self.ids.title_2.text = dish['title'][:21]
            self.ids.data_2.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."
        except Exception as e:
            print(traceback.format_exc())

        try:
            dish = dishes_list_now[2]
            source = str(dish['image_uri']).replace("\\", "")
            self.ids.image_3.source = source
            self.ids.title_3.text = dish['title'][:21]
            self.ids.data_3.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."
        except Exception as e:
            print(traceback.format_exc())

        print("calories_color: " + calories_color)
        r, g, b = calories_color.split(",")
        r = toFixed(r)
        g = toFixed(g)
        b = toFixed(b)
        #self.ids.calories_color_butt.md_bg_color = r, g, b, 1


        #рекомендация
        db_request = {}
        db_request['tm_id'] = self._app.user_data["tm_id"]
        db_request['vk_id'] = self._app.user_data["vk_id"]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        db_json = json.dumps(db_request)
        if (self._app.user_data["is_model"]):
            page_url = "https://steelfeet.ru/app/reccom_1.php"
        else:
            page_url = "https://steelfeet.ru/app/reccom_dish.php?q=" + db_json
        print("запрос рекомендации: " + page_url)
        t = requests.get(page_url, headers = headers)
            
        try:
            dishes_list_now = json.loads(t.text)
            dish = dishes_list_now

            source = str(dish['image_uri']).replace("\\", "")
            self.ids.image_reccom.source = source
            self.ids.title_reccom.text = dish['title'][:21]
            self.ids.data_reccom.text = "Калорий: " + str(dish['calories']) + "; Б: " + str(dish['proteinContent']) + " г.; Ж: " + str(dish['fatContent']) + " г.; У: " + str(dish['carbohydrateContent']) + " г."
        except Exception as e:
            print(traceback.format_exc())

    #выбираем показ камеры или текстового поля для ввода ссылки на картинку
    def select_prod(self):
        if (self._app.user_data["is_prod"]):
            self._app.screen_manager.current = 'photo_food_camera'
        else:
            self._app.screen_manager.current = 'photo_food_s1_imuri'





class PhotoFoodS1Uri(Screen):
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
        db_request['code'] = 'add_action'
        db_request['action'] = 'add_dish'
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