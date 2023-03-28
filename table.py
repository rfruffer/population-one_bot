import sqlite3

path = 'Table.db'

def createTables():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Gamers (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER UNIQUE,
        UserName TEXT,
        Status TEXT,
        Games INTEGER,
        KeyUser TEXT
    );
    ''')
    conn.commit()
    c.close()
    conn.close()

def setParticipant(UserId_,UserName_,Status_,Games_,KeyUser_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "INSERT OR IGNORE INTO Gamers (UserId,UserName,Status,Games,KeyUser) VALUES (?,?,?,?,?)"
    c.execute(sql, (UserId_,UserName_,Status_,Games_,KeyUser_,))
    conn.commit()
    c.close()
    conn.close()

def setStatus(UserId_, Status_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "UPDATE Gamers SET Status=? where UserId=?"
    c.execute(sql, (Status_,UserId_,))
    conn.commit()
    c.close()
    conn.close()

def setGames(UserId_, Games_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "UPDATE Gamers SET Games=? where UserId=?"
    c.execute(sql, (Games_,UserId_,))
    conn.commit()
    c.close()
    conn.close()

def isAdminMode():
    conn = sqlite3.connect(path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    sql = "SELECT * FROM Gamers WHERE UserId=0000"
    c.execute(sql)
    rows = c.fetchall()
    c.close()
    return (rows)

def delRow():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "DELETE FROM Gamers WHERE UserId=0000"
    c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

def getStatus(UserId_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Status FROM Gamers WHERE UserId=?"
    c.execute(sql, (UserId_,))
    rows = c.fetchone()
    if rows is not None:
        result = rows[0]
        c.close()
        return (result)
    c.close()
    return (rows)

def getUser(UserId_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT * FROM Gamers WHERE UserId=?"
    c.execute(sql, (UserId_,))
    rows = c.fetchall()
    c.close()
    return (rows)

def getGames(UserId_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Games FROM Gamers WHERE UserId=?"
    c.execute(sql, (UserId_,))
    rows = c.fetchone()[0]
    c.close()
    return (rows)

def getUserIds():
    conn = sqlite3.connect(path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    sql = "SELECT UserId as UserId FROM Gamers"
    c.execute(sql)
    rows = c.fetchall()
    c.close()
    return (','.join(str(x) for x in rows))

def getAllData():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Id as Id, UserId as UserId, UserName as UserName, Status as Status, Games as Games, KeyUser as KeyUser FROM Gamers"
    c.execute(sql)
    rows = c.fetchall()
    c.close()
    return (rows)

def updateKey(UserId_, KeyUser_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "UPDATE Gamers SET KeyUser=? where UserId=?"
    c.execute(sql, (KeyUser_, UserId_,))
    conn.commit()
    c.close()
    conn.close()
# ------------------------------------------------------
def createTableAwaiting():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Base (
        Userid INTEGER UNIQUE,
        Subscrib BOOLEAN
    );
    ''')
    conn.commit()
    c.close()
    conn.close()

def setUser(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "INSERT OR IGNORE INTO Base (Userid) VALUES (?)"
    c.execute(sql, (User_id,))
    conn.commit()
    c.close()
    conn.close()

def setSubscrib(Subscrib, User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "UPDATE Base SET Subscrib=? where Userid=?"
    c.execute(sql, (Subscrib, User_id,))
    conn.commit()
    c.close()
    conn.close()

def getSubmit(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Subscrib FROM Base where Userid = ?"
    c.execute(sql, (User_id,))
    rows = c.fetchone()
    c.close()
    return (rows)

def delUser(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "DELETE FROM Gamers WHERE UserId=?"
    c.execute(sql, (User_id,))
    conn.commit()
    c.close()
    conn.close()
# -----------------------------------------------
def createCount():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Users_list (
        Userid INTEGER UNIQUE,
        CurrentPage INTEGER
    );
    ''')
    conn.commit()
    c.close()
    conn.close()

def setUserPage(Userid_,CurrentPage_):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    # sql = "INSERT INTO Users_list (Userid, CurrentPage) VALUES(?,1) ON CONFLICT(Userid) DO UPDATE SET CurrentPage = ?"
    sql = "INSERT OR REPLACE INTO Users_list (Userid, CurrentPage) VALUES(?,?)"
    c.execute(sql, (Userid_,CurrentPage_,))
    conn.commit()
    c.close()
    conn.close()

def getCurrentPage(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT CurrentPage FROM Users_list where Userid = ?"
    c.execute(sql, (User_id,))
    rows = c.fetchone()[0]
    c.close()
    return (rows)

def getAllDataViaPage(CurrentPage_):
    coret = 0 if CurrentPage_ == 1 else (CurrentPage_ -1) * 15
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = '''SELECT Id as Id, 
                UserId as UserId, 
                UserName as UserName, 
                Status as Status, 
                Games as Games, 
                KeyUser as KeyUser 
            FROM Gamers
            ORDER BY UserName DESC
            LIMIT ?, 15;
'''
    c.execute(sql, (coret,))
    rows = c.fetchall()
    c.close()
    return (rows)
# -------------------------------------
def createNotifyTables():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Notify (
        Userid INTEGER UNIQUE,
        Subscrib BOOLEAN
    );
    ''')
    conn.commit()
    c.close()
    conn.close()

def getNotifyUsers(value):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Userid FROM Notify where Subscrib = ?"
    c.execute(sql, (value,))
    return (c.fetchall())

def setNotifyUser(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "INSERT OR IGNORE INTO Notify (Userid) VALUES (?)"
    c.execute(sql, (User_id,))
    conn.commit()
    c.close()
    conn.close()

def getSubmitNotify(User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "SELECT Subscrib FROM Notify where Userid = ?"
    c.execute(sql, (User_id,))
    return (c.fetchone())

def setSubscribNotify(Subscrib, User_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql = "UPDATE Notify SET Subscrib=? where Userid=?"
    c.execute(sql, (Subscrib, User_id,))
    conn.commit()
    c.close()
    conn.close()

