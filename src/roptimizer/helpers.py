import re

def validateEmail(email):
    if len(email) > 5:
        if re.match('^[_.0-9a-z-+]+@([0-9a-z.-]){1,}\.[a-z]{2,4}$', email) != None:
            return True

    return False
