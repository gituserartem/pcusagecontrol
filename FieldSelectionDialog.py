from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QDialog, QCheckBox)


class FieldSelectionDialog(QDialog):
    """
    Клас відповідає за формування вікна вибору полів для відображення
    """
    def __init__(self, column_names, parent=None):
        """
        :param column_names: назви полів таблиці
        :param parent: об'єкт, до якого буде прив'язане діалогове вікно 
        """
        super(FieldSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Оберіть поля")
        self.setModal(True)
        self.setFixedSize(200, 50 + len(column_names)*25)

        self.__column_names = column_names

        self.__checkbox_dict = {}
        self.__form_layout = QVBoxLayout(self)

        for column_name in self.__column_names:
            checkbox = QCheckBox(column_name, self)
            self.__checkbox_dict[column_name] = checkbox
            self.__form_layout.addWidget(checkbox)

        self.__submit_button = QPushButton("Застосувати", self)
        self.__submit_button.clicked.connect(self.accept)

        self.__form_layout.addWidget(self.__submit_button)

    def get_selected_fields(self):
        """
        Метод повертає назви обраних полів для відображення
        :return: повертає імена (ключі) тих елементів, чекбокси яких встановлені
        """
        return [column_name for column_name, checkbox in self.__checkbox_dict.items() if checkbox.isChecked()]
