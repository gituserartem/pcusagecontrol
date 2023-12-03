from TableWidget import TableWidget
from PyQt5.QtCore import QDateTime


class TableWidgetHistory(TableWidget):
    """
    Класс реалізує додавання функціоналу таблиці "Входи/Виходи" до функціоналу базової таблиці
    """
    def __init__(self, table_name, column_names, db_table_name, db_id_name):
        super(TableWidgetHistory, self).__init__(table_name, column_names, db_table_name, db_id_name)
        """
        :param table_name: назва таблиці
        :param column_names: поля таблиці
        :param db_table_name: назва таблиці у БД
        :param db_id_name: назва поля ID таблиці у БД
        """

    def get_time_data(self):
        """
        Метод виконує пошук часових даних таблиці
        :return: часові дані за кожним комп'ютером
        """
        history_data = []
        for i in range(self.rowCount()):
            use_id = self.item(i, 0).text()
            pc_id = self.item(i, 2).text()

            date_in = self.item(i, 3).text()
            date_out = self.item(i, 4).text()
            time_in = self.item(i, 5).text()
            time_out = self.item(i, 6).text()

            datetime_in = QDateTime.fromString(f"{date_in}, {time_in}", 'yyyy-MM-dd, hh:mm')
            datetime_out = QDateTime.fromString(f"{date_out}, {time_out}", 'yyyy-MM-dd, hh:mm')

            dt = (use_id, pc_id, datetime_in, datetime_out)
            history_data.append(dt)
        return history_data
