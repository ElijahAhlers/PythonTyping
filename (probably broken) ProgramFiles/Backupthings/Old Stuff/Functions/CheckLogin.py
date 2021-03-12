from Logic.Functions import UserDB as udb

def CheckCreds(username,password):
    '''Checks data entered in Username and password on the login screen.
    Parameters: (string,string)
    Returns: Boolean Authenticate, Current User'''
    UserData = udb.GetUsernamesAndPasswords()
    Authenticate = False
    
    for dictionary in UserData:
        if username == dictionary["Username"]:
            if password == dictionary["Password"]:
                Authenticate = True
                return Authenticate,username
            
    return False
        
            
            
    
