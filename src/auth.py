import data_store
from error import InputError

import re  

def auth_login_v1(email, password):
    pass
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
    # Used to check that the email is correct
    regex  = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"

    user_info = data_store.get_data()
    user_emails = user_info['emails']

    is_not_already_registered = not email in user_emails

    is_valid_email = re.match(regex, email)
    is_valid_password = len(password) >= 6
    is_valid_name_first = len(name_first) >= 1 and len(name_first) <= 50
    is_valid_name_last = len(name_last) >= 1 and len(name_last) <= 50

    if not (is_valid_email and is_valid_password and is_valid_name_last and 
            is_valid_name_first and is_not_already_registered):
        # RAISE ERROR
        raise InputError()
        
    else:
        # REGISTER USER
        user_names = user_info['names']
        user_names.append(name_first)
        user_emails.append(email)

        

    
auth_register_v1("john.henderson@gmail.com", "123126", "John", "Doe")
print(data_store.get())