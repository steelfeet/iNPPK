import os, json, sys
virtual_env = os.path.expanduser('~/projects/world-it-planet/env')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this))


from google.oauth2 import service_account
from google.cloud import vision

#распознаем изображение
current_filename = os.path.dirname(os.path.abspath(__file__)) + "/current.json"
with open(current_filename, "r", encoding="utf-8") as f:
    queue_dict = json.load(f)



try:
    credentials_file = os.path.dirname(os.path.abspath(__file__)) +  "/vision-nppk-25a4b3ee922c.json"
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    client = vision.ImageAnnotatorClient(credentials=credentials)

    if (queue_dict["type"] == "href"):
        image_uri = queue_dict["image_uri"]
        response = client.annotate_image({'image': {'source': {'image_uri': image_uri}},  'features': [],})


    image_annotations = []
    for label in response.label_annotations:
        desc = str(label.description)
        image_annotations.append(desc)
    for label in response.web_detection.web_entities:
        desc = str(label.description)
        image_annotations.append(desc)

    queue_dict["labels"] = image_annotations
    queue_dict["status"] = "Ok"

except:
    queue_dict["status"] = "Error"

with open(current_filename, "w", encoding="utf-8") as file:
    json.dump(queue_dict, file, indent=4, ensure_ascii=False)
