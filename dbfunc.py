import sqlite3

async def DBInit():
    DBConn = sqlite3.connect("UserDB.db")
    DBCursor = DBConn.cursor()
    DBCursor.execute("CREATE TABLE IF NOT EXISTS UserTable(username TEXT PRIMARY KEY, balance INTEGER)")
    DBConn.close()

async def DBRegister(username):
    DBConn = sqlite3.connect("UserDB.db")
    DBCursor = DBConn.cursor()
    try:
        DBCursor.execute("INSERT OR ABORT INTO UserTable VALUES ('{}', 10000)".format(username))
        DBConn.commit()
    except sqlite3.Error:
        DBConn.close()
        return False
    
    DBConn.close()
    return True

async def DBBalMod(username, operation, value):
    DBConn = sqlite3.connect("UserDB.db")
    DBCursor = DBConn.cursor()

    if operation == "Add":
        sign = "+"
    elif operation == "Subtract":
        sign = "-"
    elif operation == "Multiply":
        sign = "*"
    elif operation == "Divide":
        sign = "/"
    
    DBCursor.execute("UPDATE UserTable SET balance = balance {} {} WHERE username = '{}'".format(sign, value, username))
    DBConn.commit()
    DBConn.close()
