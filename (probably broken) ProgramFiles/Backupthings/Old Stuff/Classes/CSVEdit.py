import csv


class CSVWriter():

    def __init__(self, path, file):
        self.file = open(path+'/'+file+'.csv','a')
        self.header = False
        self.data = False
        self.writerMade = False

    def __writer(self):
        if not self.writerMade:
            self.writer = csv.DictWriter(self.file, fieldnames=self.header)
            self.writerMade = True
            return self.writer
        return self.writer

    def manualyMakeWriter(self):
        self.writer = csv.DictWriter(self.file, fieldnames=self.header)

    def writeHeader(self):
        if self.header:
            writer = self.__writer()
            writer.writeheader()
            self.header = True

    def writeData(self):
        if self.header and self.data:
            writer = self.__writer()
            for dic in self.data:
                writer.writerow(dic)

    def close(self):
        self.file.close()
        del self


class CSVReader():

    def __init__(self, path, file):
        self.file = open(path+'/'+file+'.csv','r')
        self.readerMade = False
        self.header = self.file.readline().split(',')
        self.header[-1] = self.header[-1][:-1]

    def __reader(self):
        if not self.readerMade:
            self.reader = csv.DictReader(self.file, fieldnames = self.header)
            return self.reader
        return self.reader

    def readData(self):
        reader = self.__reader()
        lis = [x for x in reader]
        del lis[0]
        return lis

    def close(self):
        self.file.close()

if __name__ == '__main__':
    x = CSVWriter('C:/Users/johnsonl/Desktop','test')
