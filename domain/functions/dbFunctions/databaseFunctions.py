######################
# Database functions #
######################

import sqlite3
from data.util.paths import database_path
from domain.functions.botFunctions.botMainFunctions import *


def createUsersTable():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (user_id int primary key, user_name varchar(20),user_status varchar(20),user_post varchar(10))')
    connection.commit()
    cursor.close()
    connection.close()


def createGroupsTable():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS groups (group_id int primary key, user_name varchar(20),chat_status varchar(20),swearing varchar(10))')
    connection.commit()
    cursor.close()
    connection.close()


# Saves user to database
def saveUser(user_id: int, user_name: str):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (user_id,user_name,user_status,user_post) VALUES ('%s','%s','%s','%s')" % (
                    user_id, user_name, "Clear", "User"))
            connection.commit()
            cursor.close()
            connection.close()
            log(f"User: {user_name} saved!")
        except Exception as e:
            log(f"Error when saving user: {e},chat id {user_id}")
            errorNotif(f"Error when saving user. Chat id {user_id}, userName: @{user_name}", e)
            sendErrorMessToUser(user_id)
    except Exception as e:
        log(f"Error when connecting to database: {e},chat id {user_id}")
        sendErrorMessToUser(user_id)
        errorNotif(f"Error when connecting to database,chat id {user_id}", e)


# Saves group to database
def saveGroup(group_id: int, user_name: str):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO groups (group_id,user_name,chat_status,swearing) VALUES ('%s','%s','%s','%s')" % (
                    group_id, user_name, "Clear", "allow"))
            connection.commit()
            cursor.close()
            connection.close()
            log(f"Group: {user_name} saved!")
        except Exception as e:
            log(f"Error when saving group: {e},chat id {group_id}")
            errorNotif(f"Error when saving group. Chat id {group_id}, userName: @{user_name}", e)
            sendErrorMessToUser(group_id)
    except Exception as e:
        log(f"Error when connecting to database: {e},chat id {group_id}")
        sendErrorMessToUser(group_id)
        errorNotif(f"Error when connecting to database,chat id {group_id}", e)


# Checks is user is saved on Database
def isUserInDb(user_id:int):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id='%s'" % user_id)

        res = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if res is None:
            return False
        else:
            changeUserState(user_id, "Clear")
            return True
    except Exception as e:
        log(f"Error when checking user in db: {e}")
        sendErrorMessToUser(user_id)
        errorNotif(f"Error when checking user in db, chat id {user_id}",e)


# Checks is group saved in db
def isGroupInDb(group_id:int):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT group_id FROM groups WHERE group_id='%s'" % group_id)

        res = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if res is None:
            return False
        else:
            changeGroupState(group_id, "Clear")
            return True
    except Exception as e:
        log(f"Error when checking group in db: {e}")
        sendErrorMessToUser(group_id)
        errorNotif(f"Error when checking group in db, chat id {group_id}", e)


# Changes user status
def changeUserState(user_id, user_state):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE users SET user_status = '%s' WHERE user_id = '%s'" % (user_state, user_id))
            connection.commit()
            cursor.close()
            connection.close()
            log(f" Status of {user_id} changed to {user_state}")
            return "success"
        except Exception as e:
            cursor.close()
            connection.close()
            log(f'Error when changing user status : {e}')
            return "failure"
    except Exception as e:
        log(f"Error when connecting to database and changing user status: {e}")
        errorNotif(f"Error when connecting to database and changing user status,chat id {user_id}", e)

# Changes group status
def changeGroupState(group_id, group_status):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE groups SET chat_status = '%s' WHERE group_id = '%s'" % (group_status, group_id))
            connection.commit()
            cursor.close()
            connection.close()
            log(f" Status of {group_id} changed to {group_status}")
            return "success"
        except Exception as e:
            cursor.close()
            connection.close()
            log(f'Error when changing group status : {e}')
            return "failure"
    except Exception as e:
        log(f"Error when connecting to database and changing group status: {e}")
        errorNotif(f"Error when connecting to database and changing group status,chat id {group_id}", e)
