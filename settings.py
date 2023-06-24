import enum

TOKEN = "5693917053:AAE1Dvrni97ENKfHe9DgaMRn16kLAIoJhUs"
SUPER_USERS = [
    1134647131,
]

POSTS_CHAT = -1001954088938


class Notify(enum.IntEnum):
    POST_TAKEN = 1,
    RED_APPROVED = 2,
    RED_DECLINED = 3,

