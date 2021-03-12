def writeNewCSVFile(file, header, data):
    file = open(file,'w')
    file.write(','.join(header)+'\n\n')
    for dic in data:
        values = dic.keys()
        writeStuff = ''
        for value in values:
            writeStuff+=str(dic[value])+','
        writeStuff = writeStuff[:-1]
        file.write(writeStuff+'\n')
    file.close()

def writeToCSVFile(file, listofthings):
    file = open(file,'a')
    [writeDic(file, dic) for dic in listofthings] if type(listofthings[0]) == type({}) else [writeLis(file, lis) for lis in listofthings]
    file.close()

def writeLis(openedfile, lis):
    openedfile.write(','.join(map(lambda x:str(x),lis))+'\n')

def writeDic(openedfile, dic):
    writeStuff = ''
    for key in dic.keys():
        writeStuff+=str(dic[key])+','
    writeStuff = writeStuff[:-1]
    openedfile.write(writeStuff+'\n')

def readCSVFile(file):
    file = open(file,'r')
    filelist = ''.join([line for line in file]).split('\n')
    filelist = [x.split(',') for x in filelist]
    file.close()
    appendingdic = {}
    listofdicts = []
    for i,lis in enumerate(filelist[2:-1],2):
        for num,key in enumerate(lis):
            appendingdic[key] = filelist[i][num]
        listofdicts+=[appendingdic]
    return listofdicts
