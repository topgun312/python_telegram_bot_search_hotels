import sqlite3 as sql
from typing import List, Union, Any

db_file = 'hotels_db.db'

def sql_start() -> None:
    """
    Функция для создания БД и создания таблицы hotels_info.
    """
    with sql.connect(db_file) as base:
        cur = base.cursor()
    if cur:
        print('База данных подключена!')
    cur.execute('CREATE TABLE IF NOT EXISTS hotels_info'
                '(user_command, location, id, name, fonfoto, datetime)')


def sql_add_command(message: List[Union[str, Any]]) -> None:
    """
    Функция для записи данных в таблицу hotels_info.
    :param message: список данных для записи в таблицу.
    """
    with sql.connect(db_file) as base:
        cur = base.cursor()
        cur.execute('INSERT INTO hotels_info VALUES(?, ?, ?, ?, ?, ?)',
                        tuple(message))


def get_sql_db() -> List[str]:
    """
    Функция для получения данных из таблицы hotels_info.
    :return: список данных полученных из таблицы.
    """
    with sql.connect(db_file) as base:
        cur = base.cursor()
        string = f'SELECT * FROM hotels_info'
        cur.execute(string)
        return cur.fetchall()


def delete_info() -> None:
    """
    Функция для удаления данных с таблицы hotels_info.
    """
    with sql.connect(db_file) as base:
        cur = base.cursor()
        cur.execute('DELETE FROM hotels_info')