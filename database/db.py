import psycopg2
from config import db_connection

def connect_db():
    return psycopg2.connect(
        host=db_connection['host'],
        user=db_connection['user'],
        password=db_connection['password'],
        database=db_connection['db_name']
    )

def save_task(connection, user_id, name):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO todo_bot.public.data (user_id, task_name) VALUES (%s, %s) returning task_id"
            cursor.execute(query, (user_id, name))
            connection.commit()
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def del_task(connection, task_name):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM todo_bot.public.data WHERE task_name=%s"
            cursor.execute(query, [task_name])
            connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def show_tasks(connection, user_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT task_name FROM todo_bot.public.data WHERE user_id=%s"
            cursor.execute(query, [user_id])
            connection.commit()
            result = cursor.fetchall()
            if result:
                return result
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
