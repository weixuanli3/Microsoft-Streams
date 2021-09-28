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
        'users': [],
        'channels': [], 
    }
    data_store.set(store)
