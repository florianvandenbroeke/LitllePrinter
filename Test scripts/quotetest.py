import requests

category = 'inspirational'
api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
KEY = "Fpg1VeRz4ELzZ1F+obZHXQ==7jDp8PXkGiEPzxk9"
response = requests.get(api_url, headers={'X-Api-Key': KEY})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)