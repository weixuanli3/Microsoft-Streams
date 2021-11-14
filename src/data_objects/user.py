class User:
    def __init__(self, email, password, name_first, name_last) -> None:
        self._email = email
        self._password = password
        self._name_first = name_first
        self._name_last = name_last
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def name_first(self):
        return self._name_first
    
    @password.setter
    def name_first(self, name_first):
        self._name_first = name_first

    @property
    def name_last(self):
        return self._name_last
    
    @password.setter
    def name_last(self, name_last):
        self._name_last = name_last




new_user = User("@", "123123", "John", "Hen")
new_user.password = "Hello"
print(new_user.password)