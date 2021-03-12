#Python Standard Library
import os
from datetime import date

#Our Stuff
import CSVEdit as cr
import CSVFuncs as cw
import FindWorstFile as fwf
import sys


def makeMasterCSV():
    cw.writeNewCSVFile('/'.join(sys.path[0].split('\\')[:-1])+'/2019Typing/CSVToGrade/'+str(date.today())+'.csv',
                       ['Name','Lesson','IdleTime','Accuracy','WPM'],
                       listOfDicts(averageLessons(getBestFilesAndIdleTime())))
    
def getBestFilesAndIdleTime():
    usersToGrade = getRegisteredUsers()
    filepath = 'X:/Advanced Python/2019Typing/UserData/'
    filesToGrade = []
    data = []
    lisForSamsProgram = []
    currentuser = 0
    for user in usersToGrade:
        lessonsInFolder = os.listdir(path = filepath+user+'/History')
        for lesson in lessonsInFolder:
            if not lesson[:1] == '.':
                file = lesson[:-4]
                results = cr.CSVReader('/'.join(sys.path[0].split('\\')[:-1])+'/2019Typing/UserData/'+user+'/History',file)
                results = results.readData()
                for result in results:
                    lis1 = [result['Lesson'],result['Accuracy'],result['WPM']]
                    lisForSamsProgram.append(lis1)
                    usersscore = fwf.bestOfFiles(lisForSamsProgram)
        filesToGrade.append(usersscore)
        filesToGrade[currentuser].insert(0,getdaIdleTime())
        filesToGrade[currentuser].insert(0,file[10:])
        currentuser+=1
    return filesToGrade


def getRealName(user):
    name = cr.CSVReader('X:/Advanced Python/2019Typing/UserData/'+user,'data')
    name = name.readData()
    name = dict(name[0])
    name = name['FirstName']+' '+name['LastName']
    return name


def getRegisteredUsers():
    allUsers = cr.CSVReader('X:/Advanced Python/2019Typing/UserData','UsernameAndPassword')
    allUsers = allUsers.readData()
    registeredUsers = []
    for i in allUsers:
        if i['Registered'] == '1':
            registeredUsers.append(i['Username'])
    return registeredUsers
            
    
def getdaIdleTime():
    idletime = 99
    return idletime

def renameFile(file):
    pass

def averageLessons(lessons):
    stuffINeed = []
    count=0
    for day in lessons:
        accuracies = []
        wpms = []
        averages = []
        for accuracy in day[2:]:
            accuracies.append(int(accuracy[1]))
        for wpm in day[2:]:
            wpms.append(int(wpm[2]))
        averageAccuracy = sum(accuracies)/len(accuracies)
        averageWPM = sum(wpms)/len(wpms)
        averages.append(averageAccuracy)
        averages.append(averageWPM)
        day.insert(2,averages)
        stuffINeed.append(day[:3])
    for person in getRegisteredUsers():
        stuffINeed[count].insert(0,getRealName(person))
        count+=1
    return stuffINeed

def listOfDicts(listoflists):
    lisofDicts = []
    for lis in listoflists:
        lisofDicts.append({'Name':lis[0],'Lesson':lis[1],'Idle Time':lis[2],'Accuracy':lis[3][0],'WPM':lis[3][1]})
    return lisofDicts  
    
if __name__ == '__main__':
    makeMasterCSV()
    
