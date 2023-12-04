from PyQt5.QtWidgets import QMessageBox


class PopUpNotificationsImporter:
    """
    Класс реалізує функціонал показу інформаційних та повідомлень про помилки
    """
    @staticmethod
    def _show_information(title, message):
        """
        Показ інформаційного повідомлення
        :param title: назва вікна
        :param message: повідомлення
        :return: None
        """
        error = QMessageBox()
        error.setWindowTitle(title)
        error.setIcon(QMessageBox.Information)
        error.setStandardButtons(QMessageBox.Ok)
        error_text = message
        error.setText(error_text)
        error.exec_()

    @staticmethod
    def _show_warning(message):
        """
        Показ попереджувального повідомлення
        :param message: повідомлення
        :return: None
        """
        error = QMessageBox()
        error.setWindowTitle("Помилка")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error_text = message
        error.setText(error_text)
        error.exec_()

    @staticmethod
    def _show_success_notification(message):
        """
        Показ повідомлення про успіх
        :param message: повідомлення
        :return: None
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Успішне завершення операції")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def _show_error(message):
        """
        Показ повідомлення про помилку
        :param message: повідомлення
        :return: None
        """
        error = QMessageBox()
        error.setWindowTitle("Помилка")
        error.setIcon(QMessageBox.Critical)
        error.setStandardButtons(QMessageBox.Ok)
        error_text = message
        error.setText(error_text)
        error.exec_()
