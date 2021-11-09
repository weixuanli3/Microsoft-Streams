import jwt
import shelve
from datetime import datetime

DATABASE_FILE_NAME = "src/data_base_files/database"

'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage: (By Hayden Smith)

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    # Will not work with current set up
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)

Example Storage: (Joseph)
    data = {
        'users': [
            {   # Example user
                'id' : 1,
                'names' : 'Admin',
                'name_lasts' : 'User',
                'emails' : 'admin_email@unsw.edu.au',
                'passwords': '123123',
                'handle' : 'AdminUser1234567891011',
                'channels' : [1, 2]
                'token': ["OLIUEFKSEJF.IEUFHKESF.Iuhflskejhf"],
                'is_removed' : False
                'reset_code' : False
            },
        ],
        'channels': [
            {
                'chan_id': 1,
                'name': 'Channel 1',
                'owner_id': [1],
                'users_id' : [1, 2, 3],
                'is_public': True
                'messages': []
            },
        ],
        'global_owners':[],
        'DMs' : [],
        'msgs' : []
    }
'''
## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [], 
    'global_owners': [],
    'DMs': [],
    'msgs' : [],
    'workspace_stats': {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': datetime.now()}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': datetime.now()}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': datetime.now()}],
        'utilization_rate': 0
    }
}

## YOU SHOULD MODIFY THIS OBJECT ABOVE

def get_u_id(token):
    '''given a token, return user ID Will raise error if token does not exist, so make sure to 
    only input valid tokens, or to try, except'''

    decoded_token = jwt.decode(token, "IAmNotSureReally", algorithms=["HS256"])
    return decoded_token['u_id']


class Datastore:
    def __init__(self):
        self.__store = initial_object

    '''
    Will return a subset of the database. Will return the names of all 
    users by default, but if you enter somehting as the specification, it will return that.
    Eg. If you want to print all user emails:

    user_emails = data_store.get('emails')
    
    for emails in user_emails:
        print(emails)
    '''
    def get(self, specification = 'names'):
        new_list = list()
        all_users = self.__store['users']
        for user in all_users:
            new_list.append(user[specification])
        return {specification : new_list}
    
    # Will return the whole database of channels and users
    def get_data(self):
      return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

global data_store
data_store = Datastore()

def update_permanent_storage():
    """Updates the permanent storage to contain the same content as in the datastore object"""
    filehandler = shelve.open(DATABASE_FILE_NAME)
    for item in data_store.get_data():
        # print("Storing:", data_store.get_data()[item])
        filehandler[item] = data_store.get_data()[item]
    filehandler.close()

def update_datastore_object():
    """
    Updates the datastore object to contain the same infomation as whats in the permanent storage
    Only runs if datastore contains more users than the data_store object.
    """

    filehandler = shelve.open(DATABASE_FILE_NAME)

    # If the database has nothing in it, then it does not contiue
    if len(filehandler) == 0:
        return

    # If the data_store object has more data than the data base, then it 
    # cannot continue
    if len(filehandler['users']) < len(data_store.get_data()['users']):
        return

    data_base = data_store.get_data()
    new_data_base = dict()

    for item in data_base:
        new_data_base[item] = filehandler[item]
        # print("fetching:",filehandler[item])

    filehandler.close()

    data_store.set(new_data_base)
    
update_datastore_object()
print('Loading Datastore...')
