Added extra functions channel_kick_v1 and dm_kick_v1.
The input is a token, the channel/dm id and the user_id of the person being kicked
The function removes the user from the specified channel/dm.
An input error is raised when:
- channel/dm id isn't valid
- user_id is invalid
- the user of user_id is not part of the channel/dm

An access error is raised when:
- the token isn't valid
- the token is not in the channel/dm
- the token doesn't have permissions in the channel/dm