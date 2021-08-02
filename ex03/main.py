'''
EXERCISE 03 (MEDIUM)
There is a SIM store allowing clients to find their wanted sim. For example, clients
want sim card ending as their birthday or nice numbers (66, 88).
Write a program to crawl SIM data from Viettel
https://vietteltelecom.vn/api/get/sim. The program must run every day at 3PM to
append data into csv files based on clients and their wanted SIMs. The clients and
their wanted SIM format are stored in a csv file as the input.
Each client should have a separated csv file and updated until the client is not on
the list (The store have found a SIM for him)
'''

import requests
import schedule
import pandas as pd
from client import *
from model import *

def get_data(text):
    url = 'https://vietteltelecom.vn/api/get/sim'
    data = {'key_search': text, 'isdn_type': 22}
    response = requests.post(url, data)
    data = response.json()['data']
    return data

def append_sim():
    client_file = 'Assignment8_API/ex03/out/waiting_clients.csv'
    assert os.path.exists(client_file), 'No client file'

    df = pd.read_csv(client_file)
    simList = list(df['sim'])
    for sim in simList:
        data = get_data(sim)
        if data != []:
            for item in data:       # add filter to each item in data
                item['filter'] = sim
            save_data('Assignment8_API/ex03/out/sim.csv', data)

if __name__ == '__main__':
    while True:
        client = act_client()
        print(client)
        
        append_sim()
        assert os.path.exists('Assignment8_API/ex03/out/sim.csv'), 'No sim file'

        df = pd.read_csv('Assignment8_API/ex03/out/sim.csv')

        # print sims for client
        for i in range(len(df)):
            if df['filter'][i] == client.sim:
                print(df['isdn'][i])

        # client chooses sim he/she want
        option = True
        while option == True:
            sim = int(input('Enter sim which the client buy (Enter 0 if not buy): '))
            if sim == 0:
                option = False
            elif sim in list(df['isdn']):
                client.buySim.append(sim)
                print('You bought sim {}'.format(sim))

                # update sim's data, waiting client's data and personal client's data
                drop_data('Assignment8_API/ex03/out/sim.csv', 'isdn', sim)
                drop_data('Assignment8_API/ex03/out/waiting_clients.csv', 'id', client.getID())
                client.save_personal_file()
                option = False

schedule.every().day.at('15:00').do(append_sim)