from helpers import apology


def checkValid(name, password, passchecker):    
    if not name or not password or not passchecker:
        return False        
    if password != passchecker:
        return False
    return True

def isEmpty(account, password, appname, url):
    if (not account or not password or not appname or not url):
        return True
    return False
