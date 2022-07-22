import requests
import random
import string

def generate_user ():
  first_name = ''.join(random.sample(string.ascii_lowercase, random.randint(1, 10)))
  last_name = ''.join(random.sample(string.ascii_lowercase, random.randint(1, 10)))
  
  name = first_name + ' ' + last_name
  phone_number = '+91 ' + str(random.randint(5, 9)) + ''.join(random.sample(string.digits, 9))
  email = random.choices(population = [
    '',
    ''.join(
    random.sample(string.ascii_letters, random.randint(5, 10))) +
    '@' +
    random.choice(['gmail', 'yahoo', 'hotmail']) +
    '.' +
    random.choice(['com', 'net', 'org', 'edu'])
  ], weights = [0.2, 0.8], k = 1)[0]

  return {'name': name, 'phone_number': phone_number, 'email': email}

url = 'http://127.0.0.1:8000/api/user/'

for i in range(100):
  user = generate_user()
  r = requests.post(url, data = user)
  print(i, user)
  print(r.text)
