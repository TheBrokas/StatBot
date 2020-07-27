import json
with open('token.txt') as json_file:
    token_id = json.load(json_file)

print(token_id)