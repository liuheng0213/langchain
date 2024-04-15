import requests

api_key = '78Jz1QOG-rZPeseqjCcSpw'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'url': 'https://www.linkedin.com/in/hengliu1984/',
   }
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)



print(response)