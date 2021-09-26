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
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [
        {   # Example user
            'id' : 1,
            'names' : 'Admin',
            'name_lasts' : 'User',
            'emails' : 'admin_email@unsw.edu.au',
            'passwords': '123123',
            'handle' : 'AdminUser1234567891011'
            'channels' : {
                1,
                2
            }
        },
    ],
    'channels': [
        {
            'chan_id': 1,
            'name': 1,
            'owner': 'owner1',
            'users' : {1, 2, 3}
            'public': True
        },
    ],
}

## YOU SHOULD MODIFY THIS OBJECT ABOVE

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


print('Loading Datastore...')

global data_store
data_store = Datastore()
