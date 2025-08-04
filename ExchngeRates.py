import requests
import json
import pprint

key = '6f0ad3963902fb0d54e5e45a'


result = requests.get('https://open.er-api.com/v6/latest/USD')
data = json.loads(result.text)
p = pprint.PrettyPrinter(indent = 4)
p.pprint(data)