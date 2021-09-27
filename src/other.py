from src.data_store import data_store

'''
Eg.

auth_register_v1("john.doe2@unsw.edu.au","password","John","Doe")
auth_register_v1("john.doe2@unsw.edu.au","password","Tom","Doe")
auth_register_v1("john.doe2@unsw.edu.au","password","Joseph","Doe")
auth_register_v1("john.doe2@unsw.edu.au","password","Weixuan","Doe")

print(data_store.get('names'))          # Will print: [Admin, John, Tom, Joseph, Weixuan]

clear_v1()

print(data_store.get('names'))          # Will print: [Admin]
'''

def clear_v1():

    """
    Clears all internal data for channels and users. This resets all data, and recreates 
    the initial object as per the specification.
    """
    
    store = data_store.get_data()

    store = {
        'users': [
            {   # Example user
                'id' : 1,
                'names' : 'Admin',
                'name_lasts' : 'User',
                'emails' : 'admin_email@unsw.edu.au',
                'passwords': '123123',
                'handle' : 'AdminUser1234567891011'
            },
        ],
        'channels': [
            {
                'id': 1,
                'name' : 'channel1',
            },
            {
                'id': 2,
                'name' : 'channel2',
            },
        ], 
    }
    data_store.set(store)
