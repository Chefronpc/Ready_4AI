import requests 
import json


# r = requests.get('http://httpbin.org/get')
# print(r.status_code)
# print()
# print(r.headers['content-type'])
# print()
# print(r.encoding)
# print()
# print(r.text)
# print()
# print(r.json())

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('http://httpbin.org/get', params=payload)
print()
print(r.url)
print()
print(r.json())
r_json = r.json()
args_key1 = r.json()['args']['key1']
print()
print(r_json['args'])
print()
print(args_key1)



# payload = {'some': 'data'}
# r = requests.post('http://httpbin.org/post', data=payload)
# print()
# print(r.text)

