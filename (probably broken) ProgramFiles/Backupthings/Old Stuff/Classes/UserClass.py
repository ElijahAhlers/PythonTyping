from Logic.Classes.CSVEdit import CSVReader

class User():

    def __init__(self, username):
        self.username = username
        self.filePath = 'X://Advanced Python/2019Typing/UserData/'+username.lower()
        self.historyDict = CSVReader(self.filePath,'history').readData()[-1]
        data = CSVReader(self.filePath,'data').readData()[0]
        self.firstName = data['FirstName']
        self.lastName = data['LastName']
        self.emailAdress = data['Email']
        #self.registered = bool(int(data['Registered']))
        #self.registeredTo = data['RegisteredTo'] if self.registered else None
        del data

