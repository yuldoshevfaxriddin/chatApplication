import sqlite3
import datetime

DB_NAME = "chat_application.db"

DB_TABLE_USERS = "users"
DB_TABLE_CHATS = "chats"
DB_TABLE_CHAT_USER = "chat_user"
DB_TABLE_SESSIONS = "sessions"
DB_TABLE_MESSAGES = "messages"

conn = sqlite3.connect(DB_NAME,check_same_thread=False)
cursor = conn.cursor()

# migratsiya qismi, malumotlar bazasini yaratish
def createTable()->sqlite3.Cursor:
    SQL_QUERY_USERS = f""" 
    CREATE TABLE `{DB_TABLE_USERS}` (
    id INTEGER PRIMARY KEY  AUTOINCREMENT , 
    name varchar(50),
    username varchar(100),
    password varchar(20),
    created_at varchar(20)
    );"""
    SQL_QUERY_CHATS = f""" 
    CREATE TABLE `{DB_TABLE_CHATS}` (
    id INTEGER PRIMARY KEY  AUTOINCREMENT , 
    chat varchar(30),
    created_at varchar(20)
    );"""
    SQL_QUERY_CHAT_USER = f""" 
    CREATE TABLE `{DB_TABLE_CHAT_USER}` (
    chat_id varchar(20),
    user_id varchar(20)
    );"""
    SQL_QUERY_SESSIONS = f""" 
    CREATE TABLE `{DB_TABLE_SESSIONS}` (
    id INTEGER PRIMARY KEY  AUTOINCREMENT ,
    user_id varchar(20),
    session varchar(36),
    device varchar(36),
    created_at varchar(20)
    );"""
    SQL_QUERY_MESSAGES = f""" 
    CREATE TABLE `{DB_TABLE_MESSAGES}` (
    id INTEGER PRIMARY KEY  AUTOINCREMENT ,
    user_id varchar(20),
    chat_id varchar(20),
    body text,
    created_at varchar(20)
    );"""

    cursor.execute(SQL_QUERY_USERS)
    cursor.execute(SQL_QUERY_CHATS)
    cursor.execute(SQL_QUERY_CHAT_USER)
    cursor.execute(SQL_QUERY_SESSIONS)
    cursor.execute(SQL_QUERY_MESSAGES)
    return cursor

# user qoshish
def insertUser(name,username,password):
    INSERT_USER_QUERY = f'''INSERT INTO {DB_TABLE_USERS} 
    (name, username, password, created_at )
    VALUES ('{name}','{username}','{password}','{datetime.datetime.now()}'); '''
    respons = cursor.execute(INSERT_USER_QUERY)
    conn.commit()
    return respons

def checkUser(username,password):
    SELECT_USER_QUERY = f'''SELECT * FROM {DB_TABLE_USERS} WHERE username='{username}' AND password='{password}';'''
    respons = cursor.execute(SELECT_USER_QUERY).fetchall()
    return respons

# chat qoshish
def insertChat(chat):
    INSERT_CHAT_QUERY = f'''INSERT INTO {DB_TABLE_CHATS} 
    (chat, created_at)
    VALUES ('{chat}','{datetime.datetime.now()}'); '''
    respons = cursor.execute(INSERT_CHAT_QUERY)
    conn.commit()
    return respons.execute(f'SELECT MAX(id) FROM {DB_TABLE_CHATS}').fetchone()[0]

# chat mavjud ekanligini tekshirish
def cheakCretedChat(chat):
    CHEAK_CHAT_QUERY = f'''SELECT * FROM {DB_TABLE_CHATS} WHERE chat='{chat}';'''
    respons = cursor.execute(CHEAK_CHAT_QUERY).fetchall()
    return len(respons)>0

# chat yaratish
def createChat(user_id_1,user_id_2):
    chat = str(user_id_1)+'-'+str(user_id_2)
    # bor bo'lsa True
    if not cheakCretedChat(chat):
        chat_id = insertChat(chat)
        return chat_id
    chat_id = cursor.execute(f"SELECT * FROM {DB_TABLE_CHATS} WHERE chat='{chat}'").fetchone()[0]
    return chat_id    

# sesionni yaratish
def creatSession(user_id,session,device):
    INSERT_SESSION_QUERY = f'''INSERT INTO {DB_TABLE_SESSIONS} 
    (user_id, session, device, created_at)
    VALUES ('{user_id}','{session}','{device}','{datetime.datetime.now()}'); '''
    respons = cursor.execute(INSERT_SESSION_QUERY)
    conn.commit()
    return respons.execute(f"SELECT * FROM {DB_TABLE_SESSIONS} WHERE device='{device}' AND user_id='{user_id}'").fetchall()

# update(yangilash) session
def updateSession(session_id,new_session):
    UPDATE_SESSION_QUERY = f"""UPDATE {DB_TABLE_SESSIONS} SET session = {new_session} WHERE id = '{session_id}' ;"""
    respons = cursor.execute(UPDATE_SESSION_QUERY)
    conn.commit()
    return respons.execute(f"SELECT * FROM {DB_TABLE_SESSIONS} WHERE id='{session_id}'").fetchall()

# insert messages
def insertMessage(user_id,chat_id,body):
    INSERT_MESSAGE_QUERY = f'''INSERT INTO {DB_TABLE_MESSAGES} 
    (user_id, chat_id, body, created_at)
    VALUES ('{user_id}','{chat_id}','{body}','{datetime.datetime.now()}'); '''
    respons = cursor.execute(INSERT_MESSAGE_QUERY)
    conn.commit()
    return respons


def getUsers():
    SELECT_USERS_QUERY = f'''SELECT * FROM {DB_TABLE_USERS}'''
    respons = cursor.execute(SELECT_USERS_QUERY).fetchall()
    return respons

def getChats():
    SELECT_USERS_QUERY = f'''SELECT * FROM {DB_TABLE_CHATS}'''
    respons = cursor.execute(SELECT_USERS_QUERY).fetchall()
    return respons

def getMessages():
    SELECT_MESSAGES_QUERY = f'''SELECT * FROM {DB_TABLE_MESSAGES}'''
    respons = cursor.execute(SELECT_MESSAGES_QUERY).fetchall()
    return respons

def userSeeder(n):
    # name username password
    for i in range(n):
        insertUser("Jon Doe","jon_doe","password")


if __name__=='__main__':
    # print(createTable()) # data bazani yaratish
    # userSeeder(3) # user yaratish
    # print(insertChat("1212121-12121"))
    # print(createChat(121212221,121221))
    # print(cheakCretedChat("1212121-12121"))
    # insertMessage(121,123123,"sdfsdfsdfdsfsd")
    print(getUsers())
    # print(getChats())
    # print(getMessages())
    # print(insertSession(12,"sdfsdfdsfdsfds","windows nt 5000"))




    conn.close()


