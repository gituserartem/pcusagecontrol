from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QDialog, QMenu)
from FieldSelectionDialog import FieldSelectionDialog


class TableWidget(QTableWidget):
    """
    Класс реалізує функціонал базових таблиць інтерфейсу
    """
    def __init__(self, table_name, column_names, db_table_name, db_id_name):
        """
        :param table_name: назва таблиці
        :param column_names: поля таблиці
        :param db_table_name: назва таблиці у БД
        :param db_id_name: назва поля ID таблиці у БД
        """
        super(TableWidget, self).__init__()

        self.__table_name = table_name
        self.__column_names = column_names
        self.__db_table_name = db_table_name
        self.__db_id_name = db_id_name

        self.setFocusPolicy(Qt.NoFocus)

        self.setColumnCount(len(column_names))
        self.setHorizontalHeaderLabels(column_names)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSortingEnabled(True)
        self.horizontalHeader().setMaximumSectionSize(300)
        self.horizontalHeader().setMinimumSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(120)
        self.setFixedWidth(849)

        style = """
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                border: 0px solid #d3d3d3;
                selection-background-color: #a6a6a6;
            }

            QTableWidget::item {
                padding: 5px;
                border-bottom: 0px solid #d3d3d3;
            }

            QTableWidget::item:selected {
                background-color: #b6dbc8;
                color: black;
            }

            QHeaderView::section {
                background-color: #404040;
                color: white;
                padding: 5px;
                border: 0px solid #d3d3d3;
            }

            QHeaderView::section:checked {
                background-color: #242424;
                color: white;
            }
        """

        self.setStyleSheet(style)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self.visible_columns = list(range(len(column_names)))

    def _show_context_menu(self, pos):
        """
        Метод виконує подію показу конкестового меню
        :param pos: позиція визову
        :return:
        """
        menu = QMenu(self)
        action = menu.addAction("Обрати поля для відображення")
        action.triggered.connect(self._select_fields_action_triggered)

        menu.exec_(self.viewport().mapToGlobal(pos))

    def _select_fields_action_triggered(self):
        """
        Метод виконує подію показу вікна вибору полей для відображення
        """
        field_selection_dialog = FieldSelectionDialog(self.__column_names, self)
        result = field_selection_dialog.exec_()

        if result == QDialog.Accepted:
            selected_fields = field_selection_dialog.get_selected_fields()

            for col in range(self.columnCount()):
                header_item = self.horizontalHeaderItem(col)
                header_text = header_item.text()

                if header_text in selected_fields:
                    self.setColumnHidden(col, False)
                else:
                    self.setColumnHidden(col, True)

    def get_table_name(self):
        """
        Метод повертає назву таблиці
        :return: назва таблиці
        """
        return self.__table_name

    def get_column_names(self):
        """
        Метод повертає назви полів таблиці
        :return: назви полів таблиці
        """
        return self.__column_names

    def get_db_table_name(self):
        """
        Метод повертає назву таблиці у БД
        :return: назва таблиці у БД
        """
        return self.__db_table_name

    def get_db_id_name(self):
        """
        Метод повертає назву поля ID таблиці у БД
        :return: назва поля ID таблиці у БД
        """
        return self.__db_id_name

    def add_record(self, data):
        """
        Метод додає запис у таблицю
        :param data: дані для вводу
        :return:
        """
        self.setSortingEnabled(False)

        row_position = self.rowCount()
        self.insertRow(row_position)

        for col, value in enumerate(data):
            item = QTableWidgetItem()

            if self.__table_name == "Входи/Виходи":
                if col == 3 or col == 4:
                    value = QDate.fromString(value, 'yyyy-MM-dd')
            item.setData(Qt.EditRole, value)

            self.setItem(row_position, col, item)
            item.setFlags(item.flags() ^ 2)

        self.setSortingEnabled(True)

    def update_record(self, row, updated_data):
        """
        Метод оновлює запис у таблиці
        :param row: рядок для оновлення
        :param updated_data: нові дані
        :return:
        """
        self.setSortingEnabled(False)
        for col, value in enumerate(updated_data):
            item = self.item(row, col)
            if self.__table_name == "Входи/Виходи":
                if col == 3 or col == 4:
                    formatted_date = value
                    formatted_date = QDate.fromString(formatted_date, 'yyyy-MM-dd')
                    item.setData(Qt.EditRole, formatted_date)
                else:
                    item.setData(Qt.EditRole, value)
            else:
                item.setData(Qt.EditRole, value)

            self.setItem(row, col, item)
        self.setSortingEnabled(True)
