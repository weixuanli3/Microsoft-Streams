'''Contains function clear which clears all previously stored data'''
# from data_store import data_store, update_permanent_storage
from src.data_store import data_store, update_permanent_storage
from datetime import datetime

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
        'workspace_stats': {
            'channels_exist': [{'num_channels_exist': 0, 'time_stamp': datetime.now()}],
            'dms_exist': [{'num_dms_exist': 0, 'time_stamp': datetime.now()}],
            'messages_exist': [{'num_messages_exist': 0, 'time_stamp': datetime.now()}],
            'utilization_rate': 0
        }
    }
    data_store.set(store)

    update_permanent_storage()

    return {}
