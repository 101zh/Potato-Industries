# Python Blacklist
A simple blacklist I made to help this bot (I guess). Load from this directory with `import utils.blacklistfunctions.py`.

# Why?
Blacklists within files will **not** save after bot gets shut down. 

# How to use the blacklist
Functions: `check_blacklist()`, `add_blacklist()`, `get_duration()`, and `remove_blacklist()`.

`check_blacklist(id)`: Checks the blacklist for a certain user ID. ID must be an integer.

`add_blacklist(id, duration)`: Adds a user ID to the blacklist for a certain number of seconds. 

`get_duration(id, humanize)`: Checks for how long the user ID in question is still blacklisted. Humanize is optional.

`remove_blacklist(id)`: Removes the user ID from the blacklist.
 
## Other helper Functions
`is_in_blacklist(id)`: Checks if a user has data in the blacklist.

`humanize_time(seconds)`: Humanizes seconds into minutes, hours, days, etc.
# Who is blacklisted right now?
Boxedflopper, for over 200 years.

lmao