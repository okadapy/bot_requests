import enum

TOKEN = ""
SUPER_USERS = [
    123456789,
]

POSTS_CHAT = 123456789


class Notify(enum.IntEnum):
    POST_TAKEN = (1,)
    RED_APPROVED = (2,)
    RED_DECLINED = 3
