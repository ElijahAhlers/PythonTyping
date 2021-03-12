import CSVFuncs as c
import os


allLessons = os.listdir(path='Lessons')
modeToBool = [(0,0),(1,0),(0,1)]
header = ['Part','Lesson','Backspace','Forced100','Time']

for lessonName in allLessons:
    print(lessonName)
    lesson = lessonName[12:-4]
    file = open('Lessons/'+lessonName,'r')
    listOfDicts = []
    for i,string in enumerate(file.read().split('\n')[1:],1):
        newDict = {}
        lis = string.split(',')
        if len(lis) > 1:
            lis[1] = int(lis[1][1:-1])
            lis[2] = int(lis[2][1:])
            newDict['Part'] = str(i)
            newDict['Lesson'] = lis[0][:-4]
            newDict['Backspace'] = str(modeToBool[lis[1]][0])
            newDict['Forced100'] = str(modeToBool[lis[1]][1])
            newDict['Time'] = str(lis[2])
            listOfDicts+=[newDict]
    c.writeNewCSVFile('CSVConfigs/'+lesson+'.csv',header,listOfDicts)
    file.close()
