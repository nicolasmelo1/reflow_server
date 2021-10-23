import requests

response = requests.post('https://api.twilio.com/2010-04-01/Accounts/ACe88e46cbccb1c7f46770d8c44ab42d1b/Messages.json', data={
    'From': '+18453823693',
    'Body': 'Olá lucas',
    'To': '+5511970852396'
}, auth=('ACe88e46cbccb1c7f46770d8c44ab42d1b', 'b6d3fe53f82dbf6503d3f9fb62596851'))
print(response.status_code)
print(response.content)