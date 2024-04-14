from typing import Union
from datetime import timezone, datetime


class UsersData:
    __allUsersData = dict[str, dict[str, dict[str, Union[dict, int, str]]]]({})

    def __init__(self) -> None:
        self = self

    def __setitem__(self, key, value) -> None:
        self.__allUsersData.__setitem__(key, value)

    def __getitem__(self, key):
        return self.__allUsersData.__getitem__(key)

    def keys(self):
        return self.__allUsersData.keys()

    def items(self):
        return self.__allUsersData.items()

    def values(self):
        return self.__allUsersData.values()

    def __contains__(self, key: object) -> bool:
        return self.__allUsersData.__contains__(key)

    def __str__(self) -> str:
        return self.__allUsersData.__str__()

    def getAllUserData(self) -> dict[str, dict[str, dict[str, Union[dict, int, str]]]]:
        return self.__allUsersData

    def setAllUsersData(self, newData: dict) -> None:
        self.__allUsersData = newData


global usersDataWrapper
usersDataWrapper = UsersData()
global launch_time
launch_time = launch_time = datetime.now(timezone.utc)
