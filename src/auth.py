from src.data_store import data_store
from src.error import InputError

def auth_login_v1(email, password):
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

def auth_register_v1(email, password, name_first, name_last):
    return {
        'auth_user_id': 1,
    }
