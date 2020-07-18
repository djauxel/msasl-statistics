import os
import json

API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')

val_file = open('C:\\Projects\\msasl-statistics\\subsets\\validation\\MSASL_val.json')
json_data = json.load(val_file)
val_file.close()

classes = []

for item in json_data:
    # video = { "url": None, "label": None }
    print(item)