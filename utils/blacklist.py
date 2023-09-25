"""
Helper functions for ThunderRedStar's file-based blacklist. I didn't work this out on my normal bot. I'm not that good at Python so please let me know about errors. 
"""
#holy
# --------------------------------------------- #
# Imports
import json
import time
import math
# --------------------------------------------- #

# --------------------------------------------- #
# Helpers
second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
week = 7 * day
month = 4.34857143 * week
year = 12 * month

def is_in_blacklist(id: int) -> bool:
    """
    Checks blacklist.json for the user specified.
    Inputs: id (integer)
    Output: bool
    """
    id = int(id)
    with open("utils/blacklist.json", "r") as blacklist_file:
        blacklist = json.load(blacklist_file)
    for user in blacklist:
        if user["id"] == id:
            return True
    return False

def humanize_time(seconds: int) -> str:
    """
    Humanizes seconds to a string of the biggest unit possible with time. Yes, it's unclean. Sorry.
    Inputs: seconds (integer)
    Output: string
    """
    seconds = int(seconds)
    negative = False
    if seconds < 0:
        negative = True
    seconds = abs(seconds)
    if (math.floor(seconds / year) == 0):
        if (math.floor(seconds / month) == 0):
            if (math.floor(seconds / week) == 0):
                if (math.floor(seconds / day) == 0):
                    if (math.floor(seconds / hour) == 0):
                        if (math.floor(seconds / minute) == 0):
                            return str(math.floor(seconds)) + " second" + ("s" if math.floor(seconds) != 1 else "") + (" ago" if negative == True else "")
                        return str(math.floor(seconds / minute)) + " minute" + ("s" if math.floor(seconds / minute) != 1 else "")+ (" ago" if negative == True else "")
                    return str(math.floor(seconds / hour)) + " hour" + ("s" if math.floor(seconds / hour) != 1 else "")+ (" ago" if negative == True else "")
                return str(math.floor(seconds / day)) + " day" + ("s" if math.floor(seconds / day) != 1 else "")+ (" ago" if negative == True else "")
            return str(math.floor(seconds / week)) + " week" + ("s" if math.floor(seconds / week) != 1 else "")+ (" ago" if negative == True else "")
        return str(math.floor(seconds / month)) + " month" + ("s" if math.floor(seconds / month) != 1 else "")+ (" ago" if negative == True else "")
    return str(math.floor(seconds / year)) + " year" + ("s" if math.floor(seconds / year) != 1 else "")+ (" ago" if negative == True else "")
# --------------------------------------------- #

# --------------------------------------------- #
# Main Functions

def check_blacklist(id: int) -> bool:
    """
    Checks blacklist.json for the user specified, and if found, checks if the time now is less than the time the user is blacklisted until.
    Inputs: id (integer)
    Output: bool
    """
    id = int(id)
    with open("utils/blacklist.json", "r") as blacklist_file:
        blacklist = json.load(blacklist_file)
    for user in blacklist:
        if user["id"] == id:
            if user["until"] > time.time():
                return True
    return False

def add_blacklist(id: int, duration: int) -> bool:
    """
    Checks blacklist.json for user specified, and if found, adds time to the blacklist duration. If user isn't found, add to blacklist and set duration of blacklist to that time.
    Input: id (integer), duration (integer), forever (boolean)
    Output: bool
    """
    duration = int(duration)
    id = int(id)
    with open("utils/blacklist.json", "r") as blacklist_file:
        blacklist = json.load(blacklist_file)
    if is_in_blacklist(id):
        for user in blacklist:
            if user["id"] == id:
                if user["until"] < time.time():
                    user["until"] = time.time() + duration
                else:
                    user["until"] += duration
    else:
        user = dict()
        user["id"] = id
        user["until"] = time.time() + duration
        blacklist.append(user)
    with open("utils/blacklist.json", "w") as f:
        json.dump(blacklist, f)
    return True

def get_duration(id: int, humanize: bool):
    """
    Returns duration of user blacklist. If not found, returns False.
    Input: id (integer), humanize (optional, boolean)
    Output: Integer, String, or False.
    """
    id = int(id)
    if humanize == None:
        humanize == False
    with open("utils/blacklist.json", "r") as blacklist_file:
        blacklist = json.load(blacklist_file)
    for user in blacklist:
        if user["id"] == id:
            if humanize == True:
                return humanize_time(round(user["until"] - time.time()))
            return round(user["until"] - time.time())
    return False

def remove_blacklist(id: int):
    """
    Checks blacklist.json for user specified, and if found, removes the user from the blacklist.
    Input: id (integer)
    """
    id = int(id)
    with open("utils/blacklist.json", "r") as blacklist_file:
        blacklist = json.load(blacklist_file)
    if is_in_blacklist(id):
        for user in blacklist:
            if user["id"] == id:
                blacklist.remove(user)
    with open("utils/blacklist.json", "w") as f:
        json.dump(blacklist, f)    
# --------------------------------------------- #
#woah
#