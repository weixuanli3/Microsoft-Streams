Current assumptions for functions:

- The user should not have an overly long password
    - This will help with remembering and storing the password
    - At the moment there is no limit, and a user could enter an extrealy long password that may be 
      inconvenient to store.

- The user can have spaces in their password, but cannot have a password of all spaces.

- Assuming handle will always be of reasonable length due to number of ppl with the exact same name being low
    - (At the moment is susceptible to malicious users breaking the system by creating multiple of the same user)

- User names cannot have special characters (such as !@#$%^&*(){}[];;'"<>,./?| ect) but may have a dash and other 
  characters used in names. Since this is a university app, names should be the real names of students.

- Users can create channels with names that already exist (whether the channel is created by the user or by someone else), just like in the real world.

- Users cannot create channels with names that are empty spaces

- The tokens given will be strings

- The tokens given will be of valid length

- If owner is removed from a channel, the channel has no owner and cannot get one

- You cannot change the permission ID of a person to the permission ID that they already have
    - This is to prevent mistakes where you mean to change the ID of someone, but you missclick and select the wrong option. 

- The funciton message_sendlater will not allow a message less than one character like message_send

- Pinged users will get a notification everytime that particular message is editted