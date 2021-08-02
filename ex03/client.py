import pandas as pd
import os
from model import *

def get_client_by_id(clientList, id):
    for client in clientList:
        if client.getID() == id:
            return client
    return None

def intro():
    print('\n')
    print('Enter *88 to search sim with suffixes are 88')
    print('Enter 0332* to search sim with prefixes are 0332')
    print('Enter 086*123 to search sim with prefixes are 086 and suffixes are 123')
    print('Enter *123* to search sim which contains 123')
    print('\n')

def signup():
    client_name = input('Enter Name: ')

    file = 'Assignment8_API/ex03/out/all_clients.csv'
    if os.path.exists(file):
        all_idList = get_all_client_id(file)
        client_id = max(all_idList) + 1
    else:
        all_idList = []
        client_id = 0
    client = Client(client_id, client_name)

    intro()
    sim = input('Enter Sim: ')
    client.add_sim(sim)
    print(client)    

    client.save_client('Assignment8_API/ex03/out/waiting_clients.csv')
    client.save_client('Assignment8_API/ex03/out/all_clients.csv')

    client.buySim = ''
    client.save_personal_file()

def drop_data(file, index, data):
    df = pd.read_csv(file)
    df = df.set_index(index)
    df = df.drop(data, axis = 0)
    df.to_csv(file)

def get_waiting_client_info(file):
    df = pd.read_csv(file)
    idList = list(df['id'])

    clientList = []
    for i in range(len(df)):
        client = Client(df['id'][i], df['name'][i])
        client.sim = df['sim'][i]
        clientList.append(client)

    return idList, clientList

def get_all_client_id(file):
    df = pd.read_csv(file)
    all_idList = list(df['id'])
    return all_idList

def act_client():
    print('Log in (1) / Sign up (2)')
    
    while True:
        file = 'Assignment8_API/ex03/out/waiting_clients.csv'
        if os.path.exists(file):        # check if the file is exist
            idList, clientList = get_waiting_client_info(file)
        else:
            idList = []
            clientList = []

        text = input('Enter (Enter 0 to exit): ')

        if text == '0':
            exit()
        elif text == '1':       # login
            client_id = int(input('Enter ID: '))
            assert type(client_id) == int           
            if client_id in idList:
                client = get_client_by_id(clientList, client_id)
                return client
            else:
                print('ID is not exist')
                    
        elif text == '2':
            signup()
        
        
        
            
   

