import os, requests, json, base64, traceback, time
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

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




