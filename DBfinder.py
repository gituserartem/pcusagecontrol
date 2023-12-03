import sqlite3 as sq


class DBfinder:
    """
    Клас відповідає за реалізацію функцій пошуку у БД
    """
    @staticmethod
    def _db_find_element(table_name, column_name, elem):
        """
        Метод виконує пошук елемента за значенням у БД
        :param table_name: назва таблиці
        :param column_name: назва поля для пошуку
        :param elem: значення елемента
        :return: bool (існує чи не існує)
        """
        with sq.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?", (str(elem),))
            count = cur.fetchone()[0]
            print(count)
        return count > 0

    @staticmethod
    def _db_find_max_id(table_name, column_name):
        """
        Метод виконує пошук максимального елемента за полем
        :param table_name: назва таблиці
        :param column_name: назва поля для пошуку
        :return: Any, максимальне значення поля
        """
        with sq.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT MAX({column_name}) FROM {table_name}")
            max_id = cur.fetchone()[0]
            if not max_id:
                max_id = 0
        return max_id
