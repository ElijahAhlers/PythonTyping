#'/'.join(sys.path[0].split('\\')[:-1])+
from CSVFuncs import readCSVFile as read
from CSVFuncs import writeNewCSVFile as write
from CSVFuncs import writeToCSVFile as addToFile
import os

#write('newUsers.csv',['First Name','Last Name','Password','Username','Registered'],[{'First Name':'Elijah','Last Name':'Ahlers','Username':'auto','Password':'yes','Registered':'0'}])
newUsers = read('newUsers.csv')
print(newUsers)
for firstName, lastName, username, password, registered in [item.values() for item in newUsers]:
    if not os.path.isdir(username):
        if username == 'auto':
            username = firstName.lower()+lastName.lower()
        os.mkdir(username)
        os.mkdir(username+'/History')
        os.mkdir(username+'/GamesHistory')
        write(username+'/data.csv',['FirstName','LastName'],[{'FirstName':firstName,'LastName':lastName}])
        write(username+'/history.csv',['Date','Lesson','Accuracy','WPM','Idle Time'],[])
        write(username+'/GamesHistory/LetterGame.csv',['Date','Score','Errors','Letters Left'],[])
        addToFile('UsernameAndPassword.csv',[[username, password, registered]])
