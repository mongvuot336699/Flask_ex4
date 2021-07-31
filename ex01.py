'''
EXERCISE 01 (SHORT)
Write a program to crawl quotes from this URL: https://movie-quote-api.herokuapp.com/v1/quote/
The output should be stored on a csv file by using Pandas dataframe.
'''

import pandas as pd
import requests

def get_quote(url):
    response = requests.get(url)
    data = response.json()
    return data

def save_output(data):
    df = pd.DataFrame(data)
    df.to_csv('Assignment8_API/output/out_ex01.csv')

if __name__ == '__main__':
    url = 'https://movie-quote-api.herokuapp.com/v1/quote/'
    all_data = []
    for i in range(10):
        data = get_quote(url)
        all_data.append(data)
    save_output(all_data)


