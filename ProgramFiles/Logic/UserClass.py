from Logic.CSVFuncs import readCSVFile
from Logic.UserDB import GetRegisteredUsers

class User():

    def __init__(self, username):
        historyfile = readCSVFile(open('Save Location.txt').read()+'UserData/'+username.lower()+'/history.csv')
        datafile = readCSVFile(open('Save Location.txt').read()+'UserData/'+username.lower()+'/data.csv')
        self.username = username
        self.historyDict = historyfile
        data = None if len(datafile) < 1 else datafile[0]
        self.firstName = data['FirstName']
        self.lastName = data['LastName']
        self.registered = self.username in GetRegisteredUsers()
        del data

