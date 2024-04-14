from typing import Any, Union


class UsersData:
    usersData = dict[str, dict[str, dict[str, Union[dict, int, str]]]]({})

    def __init__(self) -> None:
        self = self

    def __setitem__(self, key, value) -> None:
        self.usersData.__setitem__(key, value)

    def __getitem__(self, key):
        return self.usersData.__getitem__(key)

    def keys(self):
        return self.usersData.keys()

    def items(self):
        return self.usersData.items()

    def values(self):
        return self.usersData.values()

    def __contains__(self, key: object) -> bool:
        return self.usersData.__contains__(key)

    def __str__(self) -> str:
        return self.usersData.__str__()
