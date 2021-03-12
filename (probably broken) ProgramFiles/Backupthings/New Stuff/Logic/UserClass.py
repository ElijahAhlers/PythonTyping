from Logic.CSVFuncs import readCSVFile
import sys

class User():

    def __init__(self, username):
        historyfile = readCSVFile('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/'+username.lower()+'/history.csv')
        datafile = readCSVFile('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/'+username.lower()+'/data.csv')
        self.username = username
        self.historyDict = historyfile
        data = None if len(datafile) < 1 else datafile[0]
        self.firstName = data['FirstName']
        self.lastName = data['LastName']
        #self.registered = bool(int(data['Registered']))
        #self.registeredTo = data['RegisteredTo'] if self.registered else None
        del data

