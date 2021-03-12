#Python Standard Library
from datetime import date
import sys
from pprint import pprint

#Our Stuff
import CSVFuncs as cw

pathToMainDir = '/'.join(sys.path[0].split('\\')[:-1])

def getRegisteredUsers():
    allUsers = cw.readCSVFile(pathToMainDir+'/UserData/UsernameAndPassword.csv')
    registeredUsers = []
    for i in allUsers:
        if i['Registered'] == '1':
            registeredUsers.append(i['Username'])
    return registeredUsers

def getDataFromUser(username):
    print(username)
    path = pathToMainDir+'/UserData/'+username+'/data.csv'
    dic = cw.readCSVFile(path)
    return dic

def getHistoryFromUser(username):
    path = pathToMainDir+'/UserData/'+username+'/history.csv'
    dic = cw.readCSVFile(path)
    return dic

filename = str(date.today())+'.csv'
keys = ['LastName','FirstName','Date','Lesson','Accuracy','WPM','Idle Time']

listOfDicts = []
for user in getRegisteredUsers():
    name = getDataFromUser(user)[0]
    lastLesson = getHistoryFromUser(user)[-1]
    dictcombo = {}
    dictcombo.update(name)
    dictcombo.update(lastLesson)
    listOfDicts.append(dictcombo)
#pprint(listOfDicts)
cw.writeNewCSVFile(pathToMainDir+'/CSVToGrade/'+filename,keys,listOfDicts[:-1])

