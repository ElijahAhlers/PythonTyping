from Logic.Classes.CSVEdit import CSVReader as cr
import sys


class Day():
    def __init__(self,LessonName, LessonLocation):
        self.files = cr('/'.join(sys.path[0].split('\\')[:-1])+'/TypingFiles/Lessons',LessonLocation).readData()
        self.lessonlist = []
        self.lessonName = LessonName

        for dic in self.files:
            self.lessonlist.append(
                Lesson(
                    open('/'.join(sys.path[0].split('\\')[:-1])+'/TypingFiles/LessonParts/'+
                         dic['Lesson']+'.txt','r').read(),bool(int(dic['Backspace'])),
                    bool(int(dic['Forced100'])), int(dic['Time']), dic['Lesson'], int(dic['Part'])
                    ))
        self.numOfLessons = len(self.lessonlist)
                    
            
class Lesson():
    def __init__(self, text, bspacemode, forced100, time, filename, part):
        self.text = text
        self.backspace = bspacemode
        self.forced100 = forced100
        self.time = time
        self.filename = filename
        self.part = part-1
