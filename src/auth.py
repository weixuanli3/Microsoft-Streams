#from data_store import data_store
#from error import InputError

from src.data_store import data_store
from src.error import InputError


import re  

def auth_login_v1(email, password):
    '''
    # Do some for loop that loops through the users list somehow and compares the given email to
    user_emails = user_info['emails']
    
    if (email in user_email):
        if (users[i]['password'] == password):
            return user[i]['u_id']
        else:
            # return an input error for the incorrect password
            
        
    # else return an input error for email not found 
    
    
    
    # found = 0
    # i = 0
    # while (found == 0):
    #     # reference some the user list
    #     if (users[i]['email'] == email):
    #         found == 1
    #         if (users[i]['password'] == password):
    #             return user[i]['u_id']
    #         else:
    #             ##Spit out an input error for the wrong password
    #         return 
        
    #     i+= 1
    
    ## return an input error for the email not being found
    return {
        'auth_user_id': 1,
    }
    '''

def auth_register_v1(email, password, name_first, name_last):

    # Used to check that the email is valid
    regex  = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    is_valid_email = re.match(regex, email)

    # Gets a dictionary for the emails ie: 'emails' : [...]
    user_emails = data_store.get('emails')
    is_not_already_registered = not email in user_emails['emails']

    is_valid_password = len(password) >= 6
    is_valid_name_first = len(name_first) >= 1 and len(name_first) <= 50
    is_valid_name_last = len(name_last) >= 1 and len(name_last) <= 50

    if not (is_valid_email and is_valid_password and is_valid_name_last and 
            is_valid_name_first and is_not_already_registered):
        # RAISE ERROR 
        raise InputError('Bad')
        
    else:
        # REGISTER USER
        user_data = data_store.get_data()['users']
        # User ID is just their place in the system for now
        new_user_id = len(user_data) + 1
        user_data.append({
            'id' : new_user_id,
            'names' : name_first,
            'name_lasts' : name_last,
            'emails' : email,
            'passwords': password
        })
        return {new_user_id}

