from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout
from ValidatedDialog import ValidatedDialog


class UpdateRecordDialog(ValidatedDialog):
    """
    Класс діалогового вікна додавання записів
    """
    def __init__(self, table, selected_row_data):
        """
        :param table: посилання на таблицю для оновлення
        :param selected_row_data: значення атрибутів рядку таблиці для оновлення
        """
        super(UpdateRecordDialog, self).__init__()
        self.setWindowTitle("Оновити запис")
        self.setModal(True)
        self.setFixedSize(600, 100)

        self.__table = table
        self.__table_name = table.get_table_name()
        self.__column_names = table.get_column_names()
        self.__selected_row_data = selected_row_data
        self.__beginning_id = selected_row_data[0]

        form_layout = QVBoxLayout(self)
        self.__input_layout = QVBoxLayout(self)

        self.__input_row = []
        self.__insert_first_row()

        self.__submit_button = QPushButton("Оновити", self)
        self.__submit_button.setFixedSize(75, 25)
        self.__submit_button.setEnabled(False)
        self.__submit_button.clicked.connect(self._try_to_accept)

        form_layout.addLayout(self.__input_layout)
        form_layout.addWidget(self.__submit_button, alignment=Qt.AlignRight)

    def __insert_first_row(self):
        """
        Метод формує перший рядок вікна додавання записів
        :return: None
        """

        cols_count = len(self.__column_names)
        input_row_layout = QHBoxLayout(self)

        for i in range(cols_count):
            first_row_block = QVBoxLayout(self)
            column_label = QLabel(self.__column_names[i], self)
            line_edit = QLineEdit(str(self.__selected_row_data[i]))  # Set initial data for update
            self.__input_row.append(line_edit)
            line_edit.editingFinished.connect(lambda j=i, value=line_edit:
                                              self._validation(self.__table_name, self.__column_names[j],
                                                               self.__table.get_db_table_name(),
                                                               self.__table.get_db_id_name(),
                                                               value, self.__input_row, j))
            line_edit.textChanged.connect(self.__check_enable_button)
            if i == 0:
                line_edit.editingFinished.connect(lambda le=line_edit: self.__fill_id_if_empty(le))
            first_row_block.addWidget(column_label, alignment=Qt.AlignTop)
            first_row_block.addWidget(line_edit)
            input_row_layout.addLayout(first_row_block)
        self.__input_layout.addLayout(input_row_layout)

    def __fill_id_if_empty(self, le):
        """
        Метод заповнює значення атрибуту ID, якщо він очистився
        :return: None
        """
        if not le.text():
            le.setText(str(self.__beginning_id))

    def __check_enable_button(self):
        """
        Метод перевіряє умову становлення кнопки "оновити" доступною та виконує відповідну дію
        :return: None
        """
        # Кнопка стає доступною лише якщо всі редаговані атрибути містять текст
        enable_button = all(line_edit.text() for line_edit in self.__input_row)
        self.__submit_button.setEnabled(enable_button)

    def _try_to_accept(self):
        """
        Метод виконує поверхневу валідацію сумісності з іншими даними таблиці
        :return: None
        """
        def check_for_overlapping_intervals():
            date_in = str(self.__input_row[3].text())
            date_out = str(self.__input_row[4].text())
            time_in = str(self.__input_row[5].text())
            time_out = str(self.__input_row[6].text())

            datetime_in = QDateTime.fromString(f"{date_in}, {time_in}", 'yyyy-MM-dd, hh:mm')
            datetime_out = QDateTime.fromString(f"{date_out}, {time_out}", 'yyyy-MM-dd, hh:mm')
            dt = (datetime_in, datetime_out)

            dt_table = self.__table.get_time_data()

            check_id = int(self.__beginning_id)
            check_pc_id = int(self.__input_row[2].text())
            for i in range(len(dt_table)):
                compare_id = int(dt_table[i][0])
                compare_pc_id = int(dt_table[i][1])
                if check_pc_id == compare_pc_id and check_id != compare_id:
                    if self._are_time_intervals_overlap(dt[0], dt[1], dt_table[i][2], dt_table[i][3]):
                        error_text = f"""<b>Помилкові дані</b>
                                         <br><br>Часові інтервали використання 
                                         одного комп'ютера не мають пересікатись.<br>
                                         <br>ID комп'ютера: {check_pc_id}
                                         <br>Конфліктний ID таблиці: {dt_table[i][0]}"""
                        self._show_warning(error_text)
                        return True
            return False

        if self.__table_name == "Входи/Виходи":
            if check_for_overlapping_intervals():
                return
        self.accept()

    def get_record_data(self):
        """
        Метод виконує обробку вписаних даних
        :return: list даних для оновлення даних
        """
        return [self._convert_str_to_type(str(elem.text())) for elem in self.__input_row]
