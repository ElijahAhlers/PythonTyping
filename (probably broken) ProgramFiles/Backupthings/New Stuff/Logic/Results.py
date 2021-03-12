from Logic.CSVFuncs import *
from Logic.FindWorstFile import findBestFile
import sys
from datetime import date
import os



class Results():

    def __init__(self,day,user):
        self.firstname = user.firstName
        self.lastname = user.lastName
        self.name = day.lessonName
        self.todaysResults = {}
        self.totalIdleTime = 0
        self.lastResultAdded = None

    def addResults(self,lessonName,accuracy,wpm,idleTimeInLesson):
        self.lastResultAdded = lessonName
        self.todaysResults[lessonName] = {'accuracy':accuracy,'wpm':wpm,'idle time in lesson':idleTimeInLesson}
        
    def addIdleTimeFromResultsWindow(self,idleTimeInResultsWindow):
        self.todaysResults[self.lastResultAdded]['idle time in results window']=idleTimeInResultsWindow
        self.totalIdleTime+=idleTimeInResultsWindow

    def recordReslus(self):
        print('got here')
        allLessons = [x for x in self.todaysResults]
        
        todaysDate = date.today().strftime('%Y/%m/%d')
        todaysAccuracy = sum([self.todaysResults[x]['accuracy'] for x in allLessons]) // len(self.todaysResults)
        todaysWPM = sum([self.todaysResults[x]['wpm'] for x in allLessons]) // len(self.todaysResults)
        todaysIdleTimeInLesson = sum([self.todaysResults[x]['idle time in lesson'] for x in allLessons])
        todaysIdleTimeInResultsWindow = sum([self.todaysResults[x]['idle time in results window'] for x in allLessons])
        todaysTotalIdleTime = self.totalIdleTime
        
        self.bool = True
#        self.printOutResults(self.firstname,
#                                self.lastname,
#                                todaysDate,
#                                todaysAccuracy,
#                                todaysWPM,
#                                todaysIdleTimeInLesson,
#                                todaysIdleTimeInResultsWindow,
#                                todaysTotalIdleTime,
#                                header=self.bool)
        data = [{'last name'                   : self.lastname,
                'first name'                  : self.firstname,
                'date'                        : todaysDate,
                'accuracy'                    : todaysAccuracy,
                'wpm'                         : todaysWPM,
                'idle time in lesson'         : todaysIdleTimeInLesson,
                'idle time in results screen' : todaysIdleTimeInResultsWindow,
                'total idle time'             : todaysTotalIdleTime}]
        if self.bool:
            self.bool = not self.bool
        
        
        
        file = str('/'.join(sys.path[0].split('\\')[:-1]))+'/CSVToGrade/'+self.name+'.csv'
        if os.path.exists(file):
            header,olddata = readCSVFile(file,withHeader=True)
            
            didLessonOnceAlready = False
            
            index = -1
            for dic in olddata:
                index+=1
                if (dic['last name'],dic['first name'],dic['date']) == (data[0]['last name'],data[0]['first name'],data[0]['date']):
                    didLessonOnceAlready = True
                    print(findBestFile([['0',int(dic['accuracy']),int(dic['wpm'])],['1',int(data[0]['accuracy']),int(data[0]['wpm'])]])[0])
                    if findBestFile([['0',int(dic['accuracy']),int(dic['wpm'])],['1',int(data[0]['accuracy']),int(data[0]['wpm'])]])[0] == '1':
                        olddata.pop(index)
                        olddata+=data
                        olddata.sort(key=lambda x:x['last name'])
                    print(findBestFile([['0',int(dic['accuracy']),int(dic['wpm'])],['1',int(data[0]['accuracy']),int(data[0]['wpm'])]])[0])
                    break
            if not didLessonOnceAlready:
                olddata+=data
                olddata.sort(key=lambda x:x['last name'])
            
            data=olddata
            ting = True
            for dic in data:
                self.printOutResults(dic['first name'],dic['last name'],dic['date'],dic['accuracy'],dic['wpm'],dic['idle time in lesson'],dic['idle time in results screen'],dic['total idle time'],header=ting)
                ting = False
            
        
        writeNewCSVFile(file,['last name','first name','date','accuracy','wpm','idle time in lesson','idle time in results screen','total idle time'],data)

    def printOutResults(self,firstname,lastname,date,acc,wpm,iil,iir,total,header=True):
        if header:
            print(
"""
{:<12} | {:<10} | {:<20} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} |


""".format('First Name','Last Name','Date','Accuracy','WPM','Lesson','Results','Total'))
        print('{:<12} | {:<10} | {:<20} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} |'.format(firstname,lastname,date,acc,wpm,iil,iir,total))