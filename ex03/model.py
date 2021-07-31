import pandas as pd
import os
import datetime as dt

def save_data(file, data):
    df = pd.DataFrame(data)
    if not os.path.exists(file):
        df.to_csv(file, header = True, index = False)
    else:
        df.to_csv(file, header = None, mode = 'a', index = False)

class Client:
    def __init__(self, id, name) -> None:
        self.__id = id
        self.name = name
        self.sim = []       # filter sim
        self.buySim = []
    
    def getID(self):
        return self.__id

    def setID(self, id):
        self.__id = id

    def add_sim(self, sim):
        self.sim.append(sim)

    # each client has a personal data file
    def save_personal_file(self):
        data = {'id': self.__id, 'name': self.name, 'sim': self.sim, 'buy': self.buySim, 'datetime': dt.datetime.now()}
        file = 'Assignment8_API/ex03/out/client{}.csv'.format(self.__id)
        save_data(file, data)
    
    def save_client(self, file):
        data = {'id': self.__id, 'name': self.name, 'sim': self.sim, 'datetime': dt.datetime.now()}  
        save_data(file, data)
    
    def __repr__(self) -> str:
        return 'Client ID: {} | Name: {} | Sim: {}'.format(self.__id, self.name, self.sim)