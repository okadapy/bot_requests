import random
from sqlite3 import connect


class Suggestion:
    def __init__(self, photo, fandom, character, uid):
        self.photo = photo
        self.fandom = fandom
        self.character = character
        self.uid = uid

    def write(self):
        con = connect("master.db")
        con.cursor().execute(
            f"INSERT INTO suggestions(uid, photo, fandom, character) VALUES ("
            f"{self.uid},"
            f"'{self.photo}',"
            f"'{self.fandom}',"
            f"'{self.character}');"
        )
        con.commit()
        con.close()


def init_db():
    con = connect("master.db")
    con.cursor().execute(
        "CREATE TABLE IF NOT EXISTS suggestions(id INTEGER PRIMARY KEY,"
        "uid LONG NOT NULL,"
        "photo TEXT NOT NULL,"
        "fandom TEXT NOT NULL,"
        "character TEXT NOT NULL,"
        "taken BOOL,"
        "red_db_id LONG);"
    )
    con.cursor().execute(
        "CREATE TABLE IF NOT EXISTS redactors(id INTEGER PRIMARY KEY,"
        "uname TEXT NOT NULL,"
        "tg_id LONG UNIQUE);"
    )
    con.cursor().execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,"
        "uname TEXT NOT NULL,"
        "tg_id LONG NOT NULL UNIQUE);"
    )
    con.commit()
    con.close()


def create_user(username, userid):
    con = connect("master.db")
    con.execute(
        f"INSERT OR IGNORE INTO users(uname, tg_id) VALUES ('{username}', {userid})"
    )
    con.commit()
    con.close()


def getuid(userid):
    con = connect("master.db")
    res = con.execute(f"SELECT id FROM users WHERE tg_id = {userid}").fetchone()
    return int(res[0])


def get_rnd_post():
    con = connect("master.db")
    cur = con.cursor()
    return cur.execute(
        "SELECT * FROM suggestions WHERE taken IS NULL ORDER BY RANDOM()"
    ).fetchone()


def get_id(count):
    try:
        return random.randrange(1, count)
    except ValueError:
        return count


def reg(tg_id, uname):
    con = connect("master.db")
    con.cursor().execute(
        f"INSERT OR IGNORE INTO redactors(uname, tg_id)" f" VALUES ('{uname}', {tg_id})"
    )
    con.commit()
    con.close()


def if_red(tg_id):
    con = connect("master.db")
    return (
        con.cursor()
        .execute(f"SELECT COUNT(id) FROM redactors WHERE tg_id = {tg_id}")
        .fetchone()[0]
        == 1
    )


def get_usr(uid):
    con = connect("master.db")
    return con.execute(f"SELECT tg_id FROM users WHERE id = {uid}").fetchone()[0]


def set_taken(redid, postid):
    con = connect("master.db")
    con.cursor().execute(
        f"UPDATE OR IGNORE suggestions SET taken = TRUE, red_db_id = {redid} WHERE id = {postid}"
    )
    con.commit()
    con.close()
