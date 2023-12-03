import re
import ast
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from DBfinder import DBfinder
from PopUpNotificationsImporter import PopUpNotificationsImporter


class ValidatedDialog(QDialog, DBfinder, PopUpNotificationsImporter):
    """
    Класс що забезпечує базові функції валідованих вікон
    """
    def __init__(self):
        super(ValidatedDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def _try_to_accept(self):
        """
        Абстрактний метод що забезпечить реалізацію у наслідкових класах реалізації поверхневої валідації сумісності
        :return: None
        """
        raise NotImplementedError("В дочірньому класі ValidatedDialog має бути реалізований метод _try_to_accept()")

    def _validation(self, table_name, column_name, db_table_name, db_table_id_name,
                    input_value, row_values, column_pos=-1):
        """
        Метод виконує валідацію даних у вікні вводу
        :param table_name: назва таблиці
        :param column_name: назви полей
        :param db_table_name: назва таблиці у БД
        :param db_table_id_name: назва поля ID таблиці у БД
        :param input_value: посилання на поле вводу
        :param row_values: інші значення у рядку
        :param column_pos: позиція ваоідованого елемента
        :return: bool
        """
        def fk_validation(fk_table):
            fk_db_table_name = str()
            fk_db_field_name = str()
            message_part = str()
            if fk_table == "Відділи":
                fk_db_table_name = "[Відділи]"
                fk_db_field_name = "[ID відділу]"
                message_part = "відділу"
            elif fk_table == "Працівники":
                fk_db_table_name = "[Працівники]"
                fk_db_field_name = "[ID працівника]"
                message_part = "працівника"
            elif fk_table == "Комп'ютери":
                fk_db_table_name = "[Комп'ютери]"
                fk_db_field_name = "[ID комп'ютера]"
                message_part = "комп'ютера"

            matches = bool(re.match(r'^[1-9]\d*$', input_value.text()))
            exists = self._db_find_element(fk_db_table_name, fk_db_field_name, input_value.text())
            print("input_value.text(): " + input_value.text())
            if not matches or not exists:

                error_text = "<b>Помилкове значення вводу</b>"
                if not matches:
                    error_text += "<br><br>ID повинен складати ціле позитивне число.<br>"
                elif not exists:
                    error_text += f"<br><br>Такого {message_part} не існує.<br>"

                self._show_warning(error_text)
                input_value.clear()
                return False
            else:
                return True

        def pk_validation(db_table, db_id_field):
            pk_value = input_value.text()
            matches = bool(re.match(r'^[1-9]\d*$', pk_value))
            already_exists = self._db_find_element(str(db_table), str(db_id_field), pk_value)
            print("input_value.text(): " + input_value.text())

            if not matches or already_exists:
                error_text = "<b>Помилкове значення вводу</b>"

                if not matches:
                    error_text += "<br><br>ID повинен складати ціле позитивне число.<br>"
                elif already_exists:
                    error_text += f"<br><br>Такий {db_id_field} вже існує.<br>"

                self._show_warning(error_text)
                input_value.clear()
                return False
            else:
                return True

        def phone_num_validation():
            matches = bool(re.match(r'^\+?\d{10,15}$', input_value.text()))
            print("input_value.text(): " + input_value.text())

            if not matches:
                error_text = """<b>Помилкове значення вводу</b>
                                <br><br>Номер телефону має складатись з від 10 до 15 цифр.<br>"""
                self._show_warning(error_text)
                input_value.clear()
                return False
            else:
                return True

        def full_name_validation():
            name_value = input_value.text()
            ucaps = "А-ЩЬЮЯҐІЇЄ"
            ulows = "а-щьюяїієґ"
            pattern_ukr = re.compile(
                rf'^[{ucaps}][{ulows}]+\s[{ucaps}][{ulows}]+\s[{ucaps}][{ulows}]+'
                rf'$|^[{ucaps}][{ulows}]+\s[{ucaps}][{ulows}]+$')
            pattern_eng = re.compile(r'^[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$|^[A-Z][a-z]+\s[A-Z][a-z]+$')
            matches_ukr = bool(re.match(pattern_ukr, name_value))
            matches_eng = bool(re.match(pattern_eng, name_value))

            if not matches_ukr and not matches_eng:
                error_text = """<b>Помилкове значення вводу</b>
                                <br><br>ПІБ має бути записане у коректній формі українською або англійською мовою."""
                self._show_warning(error_text)
                input_value.clear()
                return False
            else:
                return True

        def date_validation(row, pos):
            input_date = 0
            matches_value = False

            try:
                input_date = datetime.strptime(input_value.text(), '%Y-%m-%d').date()
                matches_format = True
            except ValueError:
                matches_format = False

            now = datetime.today().date()
            if matches_format:
                matches_value = input_date <= now
            if not matches_format or not matches_value:

                error_text = "<b>Помилкове значення вводу</b>"
                if not matches_format:
                    error_text += "<br><br>Дата повинна бути записана у форматі РРРР-ММ-ДД.<br>"
                elif not matches_value:
                    error_text += f"<br><br>Дата не може бути більше поточної.<br>"

                self._show_warning(error_text)
                input_value.clear()
                return False

            if column_name == "Дата входу" and row[pos+1].text():
                out_date = datetime.strptime(row[pos+1].text(), '%Y-%m-%d').date()
                in_date = input_date
                if in_date > out_date:
                    error_text = "<b>Помилкове значення вводу</b>"
                    error_text += "<br><br>Дата входу не може бути більше дати виходу.<br>"
                    self._show_warning(error_text)
                    input_value.clear()
                    return False
            elif column_name == "Дата виходу" and row[pos-1].text():
                in_date = datetime.strptime(row[pos-1].text(), '%Y-%m-%d').date()
                out_date = input_date
                if out_date < in_date:
                    error_text = "<b>Помилкове значення вводу</b>"
                    error_text += "<br><br>Дата виходу не може бути менше дати входу.<br>"
                    self._show_warning(error_text)
                    input_value.clear()
                    return False

            input_date = input_date.strftime('%Y-%m-%d')
            input_value.setText(input_date)
            return True

        def time_validation():
            try:
                input_time = datetime.strptime(input_value.text(), '%H:%M').time()
            except ValueError:
                error_text = """<b>Помилкове значення вводу</b>
                                <br><br>Час має бути записаним у форматі ГГ:ХХ.<br>"""
                self._show_warning(error_text)
                input_value.clear()
                return False
            input_time = input_time.strftime('%H:%M')
            input_value.setText(input_time)
            return True

        def datetime_validation():
            date_in = time_fields["Дата входу"]
            date_out = time_fields["Дата виходу"]
            time_in = time_fields["Час входу"]
            time_out = time_fields["Час виходу"]

            datetime_in = datetime.strptime(f"{date_in} {time_in}", '%Y-%m-%d %H:%M')
            datetime_out = datetime.strptime(f"{date_out} {time_out}", '%Y-%m-%d %H:%M')

            if datetime_out < datetime_in:
                error_text = """<b>Помилкове значення вводу</b>
                                <br><br>Дата, час виходу не можуть бути раніше входу.<br>"""
                self._show_warning(error_text)
                input_value.setFocus()
                row_values[5].clear()
                row_values[6].clear()
                return False

            current_datetime = datetime.now()

            if datetime_in > current_datetime or datetime_out > current_datetime:
                error_text = """<b>Помилкове значення вводу</b>
                                <br><br>Момент входу/виходу не може бути пізніше поточного часу.<br>"""
                self._show_warning(error_text)
                row_values[5].clear()
                row_values[6].clear()
                return False

        date_check = False
        time_check = False

        all_ids = ("ID відділу", "ID працівника", "ID комп'ютера", "ID В/В")
        if column_name == "ID відділу" and table_name != "Відділи":
            return fk_validation("Відділи")
        elif column_name == "ID працівника" and table_name != "Працівники":
            return fk_validation("Працівники")
        elif column_name == "ID комп'ютера" and table_name != "Комп'ютери":
            return fk_validation("Комп'ютери")
        elif column_name in all_ids:
            return pk_validation(db_table_name, db_table_id_name)
        elif column_name == "Контактний номер":
            return phone_num_validation()
        elif column_name == "ПІБ":
            return full_name_validation()
        elif column_name == "Дата входу" or column_name == "Дата виходу":
            date_check = date_validation(row_values, column_pos)
        elif column_name == "Час входу" or column_name == "Час виходу":
            time_check = time_validation()

        if date_check or time_check:
            time_fields = {
                "Дата входу": row_values[3].text(),
                "Дата виходу": row_values[4].text(),
                "Час входу": row_values[5].text(),
                "Час виходу": row_values[6].text()
            }

            if (
                    time_fields["Дата входу"] and
                    time_fields["Дата виходу"] and
                    time_fields["Час входу"] and
                    time_fields["Час виходу"]
            ):
                return datetime_validation()
        return True

    @staticmethod
    def _convert_str_to_type(data):
        """
        Метод конвертує рядкові дані у їх буквальний тип python
        :param data: рядок для обробки
        :return: Any, рядок у оновленому типі даних
        """
        value = str(data)
        if len(value) > 10:
            return value
        try:
            value = ast.literal_eval(data)
            return value
        except (SyntaxError, ValueError):
            return value

    @staticmethod
    def _are_time_intervals_overlap(start1, end1, start2, end2):
        """
        Метод перевіряє чи пересікаються часові інтервали
        :param start1: початоку інтервалу1
        :param end1: кінець інтервалу1
        :param start2: початоку інтервалу2
        :param end2: кінець інтервалу2
        :return: bool, пересікаються чи ні
        """
        return not ((end1 < start2) or (start1 > end2))

    def closeEvent(self, event):
        """
        Метод виконує обробку запиту на закриття вікна
        :param event: подія
        :return: None
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Підтвердження закриття")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Ви впевнені, що бажаєте закрити вікно вводу?<br><br>Всі зміни буть втрачені.")
        yes_button = msg_box.addButton("Так", QMessageBox.YesRole)
        no_button = msg_box.addButton("Ні", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            event.accept()
        else:
            event.ignore()
