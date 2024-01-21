import json
# Настройки среды

host = "https://reqres.in/"
port = 8080
get_json = "./src/get_dict.json"
post_json = "./src/post_dict.json"
error_json = "./src/error_dict.json"
update_json = "./src/update_dict.json"
timeout = 2

with open(get_json, encoding='utf-8') as json_file:
    GET_DICT = json.load(json_file)

with open(post_json, encoding='utf-8') as json_file:
    POST_DICT = json.load(json_file)

with open(error_json, encoding='utf-8') as json_file:
    ERROR_DICT = json.load(json_file)

with open(update_json, encoding='utf-8') as json_file:
    UPDATE_DICT = json.load(json_file)
