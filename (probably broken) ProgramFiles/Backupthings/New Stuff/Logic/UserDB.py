import sys
import csv

def GetUsernamesAndPasswords():
    '''Reads Usernames and Passwords from their file and returns
    them as a list of dictionaries.  Each one looks like:
        OrderedDict([('Username',username), ('Password',password)])
    Parameters: None
    Returns: List of Dictionaries'''
    columns = ['Username','Password']
    file = open('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/UsernameAndPassword.csv','r')
    reader = csv.DictReader(file, fieldnames=columns)
    returningList = []
    for line in reader:
        returningList.append(line)
    return returningList[2:]

    
    
