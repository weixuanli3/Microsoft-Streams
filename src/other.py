'''Contains function clear which clears all previously stored data'''
# from data_store import data_store, update_permanent_storage
from src.data_store import data_store, update_permanent_storage
from datetime import datetime
import os

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
    Clears all internal data for channels and users.

    This resets all data, and recreates
    the initial object as per the specification.

    Returns:
        An empty dictionary.
    """


    store = data_store.get_data()
    store = {
        'users': [],
        'channels': [],
        'global_owners' : [],
        'DMs': [],
        'msgs' : [],
        'workspace_stats': {}
    }
    data_store.set(store)

    remove_images()

    update_permanent_storage()

    return {}

def remove_images():
    files = [f for f in os.listdir("./src/images")]
    for f in files:
        if f != 'default.jpg':
            os.remove('./src/images/' + f)
    print(files)