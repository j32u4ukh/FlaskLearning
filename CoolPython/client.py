# import requests

# cookie_dict = {'name': 'python'}
# # res = requests.get('http://127.0.0.1:5000/users?name=kk&age=97', cookies=cookie_dict)

# formData = {
#     "name": "kk",
#     "age": "97"
# }
# jsonData = {
#     "name": "poly",
#     "age": 13
# }
# # res = requests.post('http://127.0.0.1:5000/users', data=formData)
# res = requests.post('http://127.0.0.1:5000/users', json=jsonData)
# print(res)

from werkzeug.security import generate_password_hash, check_password_hash
password = "9527"
for _ in range(3):
    password_hash = generate_password_hash(password)
    print(password_hash)
    result = check_password_hash(password_hash, "9527")
    print(result)