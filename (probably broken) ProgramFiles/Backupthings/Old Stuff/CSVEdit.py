import csv


def MakeDayDataFile(filename, data):
    DayDataFileDict(filename, data) if type(data[0])==dict else DayDataFileList(filename,data)

def DayDataFileDict(filename, data):
    writer = startup(filename)
    for dictionary in data:
        writer.writerow(dictionary)

def DayDataFileList(filename, data):
    writer = startup(filename)
    for file,bspace,forced100,time in data:
        dictionary = {'File':str(file),
                      'Backspace':str(bspace),
                      'Forced100':str(forced100),
                      'Time':str(time)}
        writer.writerow(dictionary)

def startup(filename):
    columns = ['File', 'Time', 'Forced100', 'Backspace']
    file = open(filename+'.csv','w')
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    return writer

def MakeCSVFile(path, name, data):
    columns = list(data.keys())
    file = open(path+'/'+name+'.csv','w')
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerow(data)
    file.close()

def ReadDayDataFile(filename):
    columns = ['File', 'Time', 'Forced100', 'Backspace']
    file = open(filename+'.csv','r')
    reader = csv.DictReader(file, fieldnames=columns)
    listofdicts = []
    for line in reader:
        listofdicts.append(line)
    return listofdicts[-1]


if __name__ == '__main__':
    #MakeDayDataFile('newtest', [['name',False,False,200]])
    #print(ReadDayDataFile('newtest'))
    MakeCSVFile('X://Advanced Python/2019Typing/TypingFiles','LessonList',{'Name':'helkje','Location':'lkjkljlshe'})
    

