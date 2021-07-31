'''
EXERCISE 02 (SHORT)
Write a program to shorten an input URL by using an external API. You could
consider to use this API: https://cleanuri.com/api/v1/shorten.
'''

import requests

def shorten_url(url):
    api = 'https://cleanuri.com/api/v1/shorten'
    data = {'url': url}
    response = requests.post(api, data)
    data = response.json()
    return data

if __name__ == '__main__':
    while True:
        url = input("Enter url (Enter 0 to exit): ")
        if url == '0':
            exit()
        try: 
            print(shorten_url(url))
        except AssertionError as e:
            print(e)

# https://www.fcbarcelona.com/en/football/first-team/players/4974/lionel-messi
