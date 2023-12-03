import sys
import sqlite3 as sq
import ast
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QIcon
from PyQt5.QtCore import Qt, QRect, QMetaObject
from PyQt5.QtWidgets import (QMainWindow, QWidget, QStackedWidget, QPushButton, QLabel,
                             QVBoxLayout, QDialog, QMessageBox,
                             QStackedLayout, QFrame)
from PopUpNotificationsImporter import PopUpNotificationsImporter
from TableWidget import TableWidget
from TableWidgetHistory import TableWidgetHistory
from UpdateRecordDialog import UpdateRecordDialog
from AddRecordsDialog import AddRecordsDialog
from StatsFrame import StatsFrame
from AboutProgramDialog import AboutProgramDialog


class MainWindow(QMainWindow, PopUpNotificationsImporter):
    """
    Класс головного вікна, в якому зібрані усі інші створені класи та реалізована загальна логіка програми
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.__opendb()     # Створюємо, або ж відкриваємо таблицю

        self.setObjectName("MainWindow")
        self.setFixedSize(1000, 600)
        icon = QIcon("images\icon.ico")
        self.setWindowIcon(icon)

        self.__centralwidget = QFrame(self)     # Об'єкт, на якому розміщується весь інтерфейс
        self.__centralwidget.setObjectName("centralwidget")

        # Об'єкт, за домогою якого реалізується перемикання між вікном редагування таблиць та вікном статистики
        self.__stacked_interface = QStackedLayout(self)

        # Вікно, що буде містити таблиці
        self.__tables_frame = QFrame(self)

        # Вікно статистики
        self.__stats_frame = StatsFrame(self)

        # Об'єкт, за домогою якого реалізується перемикання між таблицями
        self.__stacked_tables = QStackedWidget(self.__tables_frame)

        self.__stacked_interface.addWidget(self.__stats_frame)
        self.__stacked_interface.addWidget(self.__tables_frame)
        self.__stacked_interface.setCurrentIndex(0)

        # Кожен об'єкт відповідає за свою таблицю
        self.__departments_table = TableWidget(
            "Відділи", ["ID відділу", "Назва відділу", "Адреса"], "[Відділи]", "[ID відділу]"
        )
        self.__employees_table = TableWidget(
            "Працівники", ["ID працівника", "ПІБ", "ID відділу", "Контактний номер"], "[Працівники]", "[ID працівника]"
        )
        self.__computers_table = TableWidget(
            "Комп'ютери", ["ID комп'ютера", "Модель", "ID відділу"], "[Комп'ютери]", "[ID комп'ютера]"
        )
        self.__history_table = TableWidgetHistory(
            "Входи/Виходи",
            ["ID В/В", "ID працівника", "ID комп'ютера", "Дата входу", "Дата виходу", "Час входу", "Час виходу"],
            "[Входи/Виходи]", "[ID В/В]"
        )

        self.__departments_table.setObjectName("departments_table")
        self.__employees_table.setObjectName("employees_table")
        self.__computers_table.setObjectName("computers_table")
        self.__history_table.setObjectName("history_table")

        # Додаємо створені таблиці у загальний віджет
        self.__stacked_tables.addWidget(self.__departments_table)
        self.__stacked_tables.addWidget(self.__employees_table)
        self.__stacked_tables.addWidget(self.__computers_table)
        self.__stacked_tables.addWidget(self.__history_table)

        # Об'єкт відповідає за меню у лівій частині екрану
        frame_menu = QWidget(self.__centralwidget)
        frame_menu.setGeometry(QRect(0, 0, 151, 600))
        frame_menu.setFixedWidth(151)
        frame_menu.setStyleSheet("background-color: rgb(80, 80, 80);")
        frame_menu.setObjectName("frame_menu")

        # Об'єкт відповідає за меню у лівій частині екрану
        menu_layout_widget = QWidget(frame_menu)
        menu_layout_widget.setGeometry(QRect(0, 0, 151, 350))
        menu_layout_widget.setObjectName("menu_layout_widget")
        menu_layout = QVBoxLayout(menu_layout_widget)
        menu_layout.setContentsMargins(5, 5, 5, 5)
        menu_layout.setSpacing(6)
        menu_layout.setObjectName("menu_layout")

        # Додаємо у меню картинку
        image_label = QLabel(menu_layout_widget)
        pixmap = QPixmap("images/computer_usage_control.png")
        pixmap = pixmap.transformed(QTransform().scale(0.1, 0.1), mode=Qt.SmoothTransformation)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.end()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignLeft)
        menu_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Створюємо кнопки меню
        self.__menuButtonDepartment = QPushButton(menu_layout_widget)
        self.__menuButtonEmployees = QPushButton(menu_layout_widget)
        self.__menuButtonPCs = QPushButton(menu_layout_widget)
        self.__menuButtonHistory = QPushButton(menu_layout_widget)
        self.__menuButtonStats = QPushButton(menu_layout_widget)
        self.__menuButtonAboutProgram = QPushButton(menu_layout_widget)

        # Встановлюємо стилі для натиснутих та ненатиснутих кнопок
        self.__menu_btn_pressed_style = """
            QPushButton {
                padding: 8px 16px;
                font: 81 9pt \"Wix Madefor Display ExtraBold\";
                text-align: left;
                text-decoration: none;
                color: #ffffff;
                background-color: #2980b9;
                border: 1px solid #2980b9;
                border-radius: 2px;
                transition: background-color 0.3s;
            }

            QPushButton:hover {
                background-color: #3498db;
                border: 1px solid #3498db;
            }
            
            QPushButton:pressed {
                background-color: #2980b9;
                border: 1px solid #2980b9;
            }
        """

        self.__menu_btn_not_pressed_style = """
            QPushButton {
                padding: 8px 16px;
                font: 81 9pt \"Wix Madefor Display ExtraBold\";
                text-align: left;
                text-decoration: none;
                color: #ffffff;
                background-color: #808080;
                border: 1px solid #808080;
                border-radius: 2px;
                transition: background-color 0.3s;
            }

            QPushButton:hover {
                background-color: #3498db;
                border: 1px solid #3498db;
            }
            
            QPushButton:pressed {
                background-color: #2980b9;
                border: 1px solid #2980b9;
            }
        """

        self.__set_menu_buttons(menu_layout)

        # Поле відповідає за збереження даних про натиснуту кнопку меню (щоб відображати тільки її натиснутою)
        self.__is_button_pressed = {
            self.__menuButtonDepartment: False,
            self.__menuButtonEmployees: False,
            self.__menuButtonPCs: False,
            self.__menuButtonHistory: False,
            self.__menuButtonStats: True
        }

        # Блок створює за Header відкритого вікна (назва таблиці)
        table_title = QLabel(self.__centralwidget)
        table_title.setGeometry(QRect(150, 0, 650+200, 41))
        table_title.setMargin(10)
        table_title.setStyleSheet("""background-color: rgb(197, 225, 255);
                                     font-family: "Geologica ExtraBold";
                                     font-size: 14pt;
                                     font-weight: bold;""")
        table_title.setObjectName("table_name")
        table_title.setText("Статистика")

        # Кнопки для оперуваня таблицею
        self.__buttonAdd = QPushButton(self.__tables_frame)
        self.__buttonUpdate = QPushButton(self.__tables_frame)
        self.__buttonDelete = QPushButton(self.__tables_frame)

        self.__buttonAdd.setObjectName("buttonAdd")
        self.__buttonUpdate.setObjectName("buttonUpdate")
        self.__buttonDelete.setObjectName("buttonDelete")
        self.__buttonUpdate.setEnabled(False)
        self.__buttonDelete.setEnabled(False)

        # Прив'язуємо події користувача зі зміни обраних комірок до оновлення стану кнопок "Оновити" та "Видалити"
        for i in range(self.__stacked_tables.count()):
            self.__stacked_tables.widget(i).itemSelectionChanged.connect(self.__update_button_update_state)
            self.__stacked_tables.widget(i).itemSelectionChanged.connect(self.__update_button_delete_state)
            self.__stacked_tables.widget(i).customContextMenuRequested.connect(self.__update_button_update_state)
            self.__stacked_tables.widget(i).customContextMenuRequested.connect(self.__update_button_delete_state)

        self.__buttonAdd.setStyleSheet("""
            QPushButton {
                background-color: rgb(98, 199, 96);
                font: 81 9pt \"Wix Madefor Display Regular\";
                color: rgb(0, 0, 0);
                border: 1px;
                border-radius: 3px;;
            }

            QPushButton:hover {
                background-color: #5aaf5a;  /* Pressed background color (a darker green) */
            }

            QPushButton:pressed {
                background-color: #70cc70;  /* Hover background color (lighter green) */
            }
        """)

        self.__buttonUpdate.setStyleSheet("""
            QPushButton {
                background-color: rgb(117, 154, 255);
                font: 81 9pt \"Wix Madefor Display Regular\";
                color: rgb(0, 0, 0);
                border: 1px;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: #768de5;  /* Pressed background color (a darker blue) */
            }

            QPushButton:pressed {
                background-color: #8c9eff;  /* Hover background color (lighter blue) */ 
            }

            QPushButton:disabled {
                background-color: #a0a0a0;  /* Disabled background color (gray) */
                color: #242424;  /* Disabled text color (gray) */
            }
        """)

        self.__buttonDelete.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
                font: 81 9pt \"Wix Madefor Display Regular\";
                background-color: rgb(217, 44, 47);
                border: 1px;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: rgb(200, 0, 0);  /* Pressed background color (a darker red) */
            }

            QPushButton:pressed {
                background-color: #ff5c61;  /* Hover background color (a lighter red) */
            }

            QPushButton:disabled {
                background-color: #a0a0a0;  /* Disabled background color (gray) */
                color: #242424;  /* Disabled text color (gray) */
            }
        """)

        # Встановлюємо розміри та положення __tables_frame та його елементів
        self.__tables_frame.setGeometry(QRect(151, 0, 849, 580))
        self.__stacked_tables.setGeometry(QRect(0, 40, 849, 441))
        self.__buttonAdd.setGeometry(QRect(10, 500, 101, 31))
        self.__buttonUpdate.setGeometry(QRect(120, 500, 111, 31))
        self.__buttonDelete.setGeometry(QRect(530+200, 500, 111, 31))

        # Виводимо деякі об'єкти на передній план
        table_title.raise_()
        frame_menu.raise_()
        self.__buttonAdd.raise_()
        self.__buttonUpdate.raise_()
        self.__buttonDelete.raise_()

        self.setCentralWidget(self.__centralwidget)

        self.__set_standard_titles()
        QMetaObject.connectSlotsByName(self)

        # Прив'язуємо натискання кнопок до подій, які вони викликають
        self.__menuButtonDepartment.clicked.connect(lambda: self.__stacked_tables.setCurrentIndex(0))
        self.__menuButtonDepartment.clicked.connect(lambda: self.__stacked_interface.setCurrentIndex(1))
        self.__menuButtonDepartment.clicked.connect(lambda: table_title.setText("Відділи"))
        self.__menuButtonEmployees.clicked.connect(lambda: self.__stacked_tables.setCurrentIndex(1))
        self.__menuButtonEmployees.clicked.connect(lambda: self.__stacked_interface.setCurrentIndex(1))
        self.__menuButtonEmployees.clicked.connect(lambda: table_title.setText("Працівники"))
        self.__menuButtonPCs.clicked.connect(lambda: self.__stacked_tables.setCurrentIndex(2))
        self.__menuButtonPCs.clicked.connect(lambda: self.__stacked_interface.setCurrentIndex(1))
        self.__menuButtonPCs.clicked.connect(lambda: table_title.setText("Комп'ютери"))
        self.__menuButtonHistory.clicked.connect(lambda: self.__stacked_tables.setCurrentIndex(3))
        self.__menuButtonHistory.clicked.connect(lambda: self.__stacked_interface.setCurrentIndex(1))
        self.__menuButtonHistory.clicked.connect(lambda: table_title.setText("Входи/Виходи"))
        self.__menuButtonStats.clicked.connect(lambda: self.__stacked_interface.setCurrentIndex(0))
        self.__menuButtonStats.clicked.connect(lambda: table_title.setText("Статистика"))
        self.__menuButtonAboutProgram.clicked.connect(self.__show_about_program_dialog)

        self.__menuButtonDepartment.clicked.connect(self.__update_button_update_state)
        self.__menuButtonEmployees.clicked.connect(self.__update_button_update_state)
        self.__menuButtonPCs.clicked.connect(self.__update_button_update_state)
        self.__menuButtonHistory.clicked.connect(self.__update_button_update_state)
        self.__menuButtonHistory.clicked.connect(self.__update_button_update_state)

        self.__menuButtonDepartment.clicked.connect(self.__update_button_delete_state)
        self.__menuButtonEmployees.clicked.connect(self.__update_button_delete_state)
        self.__menuButtonPCs.clicked.connect(self.__update_button_delete_state)
        self.__menuButtonHistory.clicked.connect(self.__update_button_delete_state)
        self.__menuButtonHistory.clicked.connect(self.__update_button_delete_state)

        self.__menuButtonDepartment.clicked.connect(
            lambda: self.__menu_button_click(self.__menuButtonDepartment))
        self.__menuButtonEmployees.clicked.connect(
            lambda: self.__menu_button_click(self.__menuButtonEmployees))
        self.__menuButtonPCs.clicked.connect(
            lambda: self.__menu_button_click(self.__menuButtonPCs))
        self.__menuButtonHistory.clicked.connect(
            lambda: self.__menu_button_click(self.__menuButtonHistory))
        self.__menuButtonStats.clicked.connect(
            lambda: self.__menu_button_click(self.__menuButtonStats))

        self.__buttonAdd.clicked.connect(self.__show_add_records_dialog)
        self.__buttonUpdate.clicked.connect(self.__show_update_record_dialog)
        self.__buttonDelete.clicked.connect(self.__delete_selected_rows)

        # Завантажуємо дані з бази даних у таблиці як завершальний етап ініціалізації вікна
        self.__load_data()

    def __show_update_record_dialog(self):
        """
        Метод викликає діалогове вікно оновлення запису та оперує його сценаріями
        :return: None
        """
        cur_table = self.__stacked_tables.currentWidget()   # Обираємо поточну таблицю
        selected_items = cur_table.selectedItems()          # Запам'ятовуємо вибрані елементи

        # Перевірка, чи вибрав користувач елементи лише 1 рядку
        is_one_row_selected = len(set(item.row() for item in selected_items)) == 1

        # Якщо обрано лише 1 рядок, запускаємо сценарій виклику діалогового віна
        if is_one_row_selected:
            # Дізнаємося індекс обраного рядка
            selected_row = selected_items[0].row()

            # Дістаємо дані з цього рядка для заповнення полей у рядку оновлення
            selected_row_data = [self.__convert_str_to_type(str(cur_table.item(selected_row, col).text()))
                                 for col in range(cur_table.columnCount())]

            # Створюємо та викликаємо вікно оновлення
            update_record_dialog = UpdateRecordDialog(cur_table, selected_row_data)
            result = update_record_dialog.exec_()

            if result == QDialog.Accepted:
                # Збираємо дані після прийнятого сценарію діалогового вікна
                updated_row_data = update_record_dialog.get_record_data()

                table_name = cur_table.get_db_table_name()
                table_id_name = cur_table.get_db_id_name()

                columns_to_update = []
                new_data = []

                # Цикл знаходить та запам'ятовує дані та назви полів, що були оновлені
                success = False
                for i in range(len(updated_row_data)):
                    if updated_row_data[i] != selected_row_data[i]:
                        columns_to_update.append(f"[{cur_table.get_column_names()[i]}]")
                        new_data.append(updated_row_data[i])
                if columns_to_update:
                    # Запам'ятовуємо ID записів для оновлення, викликаємо функцію з запитом до бази даних на видалення
                    id_to_update = selected_row_data[0]
                    success = self.__db_update_data(table_name, table_id_name,
                                                    columns_to_update, id_to_update, new_data)
                # Якщо помилок при роботі з базою даних не виникло, викликаємо функцію оновлення запису у табличці
                if success:
                    cur_table.update_record(selected_row, updated_row_data)
            update_record_dialog = None

    def __show_add_records_dialog(self):
        """
        Метод викликає діалогове вікно додавання записів та оперує його сценаріями
        :return: None
        """
        cur_table = self.__stacked_tables.currentWidget()

        add_records_dialog = AddRecordsDialog(cur_table)
        result = add_records_dialog.exec_()

        if result == QDialog.Accepted:
            # Збираємо дані після прийнятого сценарію діалогового вікна, зокрема про джерело даних - введення чи файл
            record_data, source = add_records_dialog.get_record_data()
            success = self.__db_insert_data(cur_table.get_db_table_name(), record_data, source)

            # Якщо помилок при роботі з базою даних не виникло, викликаємо функцію додавання записів у табличку
            # для всіх доданих записів
            if success:
                for data in record_data:
                    cur_table.add_record(data)
        add_records_dialog = None

    def __delete_selected_rows(self):
        """
        Метод оперує сценаріями запиту на видалення запису
        :return: None
        """
        cur_table = self.__stacked_tables.currentWidget()
        selected_rows = set(item.row() for item in cur_table.selectedItems())

        if not selected_rows:   # Перевіряємо чи був вибраний хочаб 1 запис
            return

        # Створення вікна підтвердження видалення
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Підтвердження видалення")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Ви впевнені, що бажаєте видалити обрані записи?")

        # Додавання кнопок "Так" та "Ні"
        yes_button = msg_box.addButton("Так", QMessageBox.YesRole)
        no_button = msg_box.addButton("Ні", QMessageBox.NoRole)

        msg_box.setDefaultButton(no_button)
        msg_box.exec_()     # Запуск підтверджувального вікна

        # Запуск сценарію видалення, якщо користувач обрав "Так"
        if msg_box.clickedButton() == yes_button:
            # Будемо видаляти рядки в зворотньому порядку щоб уникнути
            # помилок зі зміною індексів під час видалення з таблички
            selected_rows = sorted(selected_rows, reverse=True)
            ids_to_delete = [cur_table.item(row, 0).text() for row in selected_rows]

            # Запускаємо видалення записів з бази даних
            success = self.__db_delete_data(cur_table.get_db_table_name(), cur_table.get_db_id_name(), ids_to_delete)
            if success:
                for row in selected_rows:   # Видалення даних з таблиці, якщо дані були успішно видалені в БД
                    cur_table.removeRow(row)

        # Оновлення станів кнопок оновлення та видалення відповідно до поточних обраних елементів
        self.__update_button_update_state()
        self.__update_button_delete_state()

    @staticmethod
    def __show_about_program_dialog():
        """
        Метод створює та викликає діалогове вікно "Про програму"
        :return: None
        """
        dialog = AboutProgramDialog()
        dialog.exec_()

    def __set_standard_titles(self):
        """
        Метод встановлює назви базових елементів вікна
        :return: None
        """
        self.setWindowTitle("Контроль часу використання комп'ютерів")
        self.__menuButtonDepartment.setText("Відділи")
        self.__menuButtonEmployees.setText("Працівники")
        self.__menuButtonPCs.setText("Комп'ютери")
        self.__menuButtonHistory.setText("Входи/Виходи")
        self.__menuButtonStats.setText("Статистика")
        self.__menuButtonAboutProgram.setText("Про програму")
        self.__buttonAdd.setText("Додати записи")
        self.__buttonUpdate.setText("Оновити запис")
        self.__buttonDelete.setText("Видалити записи")

    def __set_menu_buttons(self, menu_layout):
        """
        Метод налаштовує вигляд кнопок меню та додає у єдиний макет
        :return: None
        """
        self.__menuButtonDepartment.setStyleSheet(self.__menu_btn_not_pressed_style)
        self.__menuButtonEmployees.setStyleSheet(self.__menu_btn_not_pressed_style)
        self.__menuButtonPCs.setStyleSheet(self.__menu_btn_not_pressed_style)
        self.__menuButtonHistory.setStyleSheet(self.__menu_btn_not_pressed_style)
        self.__menuButtonStats.setStyleSheet(self.__menu_btn_pressed_style)
        self.__menuButtonAboutProgram.setStyleSheet(self.__menu_btn_not_pressed_style)

        menu_layout.addWidget(self.__menuButtonDepartment)
        menu_layout.addWidget(self.__menuButtonEmployees)
        menu_layout.addWidget(self.__menuButtonPCs)
        menu_layout.addWidget(self.__menuButtonHistory)
        menu_layout.addWidget(self.__menuButtonStats)
        menu_layout.addSpacing(100)
        menu_layout.addWidget(self.__menuButtonAboutProgram)

    def __menu_button_click(self, button):
        """
        Метод встановлює стан натиснутості для поточної кнопоки меню, що має бути зафіксованою після натискання
        :param button: кнопка, яку треба зафіксувати
        :return: None
        """
        for btn, is_pressed in self.__is_button_pressed.items():
            if btn == button:
                self.__is_button_pressed[btn] = True
                btn.setStyleSheet(self.__menu_btn_pressed_style)
            else:
                self.__is_button_pressed[btn] = False
                btn.setStyleSheet(self.__menu_btn_not_pressed_style)

    def __update_button_delete_state(self):
        """
        Метод перевіряє умову становлення доступною кнопки видалення записів
        :return: None
        """
        selected_items = self.__stacked_tables.currentWidget().selectedItems()
        # Перевірка, чи вибрано тільки один рядок
        is_at_least_1_row_selected = len(tuple(item.row() for item in selected_items)) >= 1
        self.__buttonDelete.setEnabled(is_at_least_1_row_selected)

    def __update_button_update_state(self):
        """
        Метод перевіряє умову становлення доступною кнопки оновлення записів
        :return: None
        """
        selected_items = self.__stacked_tables.currentWidget().selectedItems()
        is_only_one_row_selected = len(set(item.row() for item in selected_items)) == 1
        self.__buttonUpdate.setEnabled(is_only_one_row_selected)

    def __load_data(self):
        """
        Метод завантажує дані з бази даних до віджету таблиць
        :return: None
        """

        # Встановлюємо з'єднання з БД
        with sq.connect("database.db") as con:
            cur = con.cursor()  # Створюємро курсор для роботи з БД

            # Запускаємо запити до БД та встановляємо отримані дані у таблиці програми

            cur.execute("SELECT * FROM [Відділи]")
            rows = cur.fetchall()
            for row in rows:
                self.__departments_table.add_record(row)

            cur.execute("SELECT * FROM [Працівники]")
            rows = cur.fetchall()
            for row in rows:
                self.__employees_table.add_record(row)

            cur.execute("SELECT * FROM [Комп'ютери]")
            rows = cur.fetchall()
            for row in rows:
                self.__computers_table.add_record(row)

            cur.execute("SELECT * FROM [Входи/Виходи]")
            rows = cur.fetchall()
            for row in rows:
                self.__history_table.add_record(row)

    def closeEvent(self, event):
        """
        Метод встановлює поведінку програми після натискання користувача кнопки закриття програми
        :return: None
        """
        # Створюємо вікно перевірки запиту користувача на закриття
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Підтвердження виходу")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Ви впевнені, що бажаєте вийти із програми?")

        # Додавання кнопок "Так" та "Ні"
        yes_button = msg_box.addButton("Так", QMessageBox.YesRole)
        no_button = msg_box.addButton("Ні", QMessageBox.NoRole)

        # Встановлення значення за замовчуванням для кнопки "Ні"
        msg_box.setDefaultButton(no_button)

        # Відображення діалогового вікна та отримання відповіді
        msg_box.exec_()

        # Подія закриття виконується, якщо користувач підтвердив вибір
        if msg_box.clickedButton() == yes_button:
            event.accept()
        else:
            event.ignore()

    def __opendb(self):
        """
        Метод з'єднується, або ж автоматично створює БД, якщо вона не наявна та створює таблиці, якщо їх нема
        :return: None
        """
        try:
            with sq.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS [Відділи] (
                            [ID відділу] INTEGER PRIMARY KEY,
                            [Назва відділу] TEXT NOT NULL,
                            [Адреса] TEXT NOT NULL
                            );""")

                cur.execute("""
                            CREATE TABLE IF NOT EXISTS [Працівники] (
                            [ID працівника] INTEGER PRIMARY KEY,
                            [ПІБ] TEXT NOT NULL,
                            [ID відділу] INTEGER NOT NULL REFERENCES Відділи ([ID відділу]) 
                            ON UPDATE RESTRICT 
                            ON DELETE RESTRICT,
                            [Контактний номер] TEXT NOT NULL
                            );""")

                cur.execute("""
                            CREATE TABLE IF NOT EXISTS [Комп'ютери] (
                            [ID комп'ютера] INTEGER PRIMARY KEY,
                            [Модель] TEXT NOT NULL,
                            [ID відділу] INTEGER NOT NULL REFERENCES Відділи ([ID відділу])
                            ON UPDATE RESTRICT 
                            ON DELETE RESTRICT 
                            );""")

                cur.execute("""
                            CREATE TABLE IF NOT EXISTS [Входи/Виходи] (
                            [ID В/В] INTEGER PRIMARY KEY,
                            [ID працівника] INTEGER NOT NULL REFERENCES [Працівники] ([ID працівника]) 
                            ON DELETE RESTRICT,
                            [ID комп'ютера] INTEGER NOT NULL REFERENCES [Комп'ютери] ([ID комп'ютера]) 
                            ON UPDATE RESTRICT 
                            ON DELETE RESTRICT,
                            [Дата входу] TEXT NOT NULL,
                            [Дата виходу] TEXT NOT NULL,
                            [Час входу] TEXT NOT NULL,
                            [Час виходу] TEXT NOT NULL
                            )""")
        # Обробка помилок, якщо вони виникнуть, супроводжуємо відповідними повідомленнями про помилку
        except sq.Error as error:
            self._show_error(f"Помилка SQLite: {error}")
            sys.exit()
        except Exception as error:
            self._show_error(f"Трапилась неочікувана помилка: {error}")
            sys.exit()

    def __db_insert_data(self, table_name, data, source):
        """
        Метод вставляє дані у БД (1 чи більше рядків)
        :param table_name: назва таблиці для вставлення даних
        :param data: дані у форматі двовимірного масиву (один рядок відповідає одному рядку таблиці)
        :param source: джерело даних - файл або ручне введення (file, user_input)
        :return: True, False (успіх виконання запиту)
        """
        try:
            with sq.connect("database.db") as con:
                cur = con.cursor()
                placeholders = ','.join(['?'] * len(data[0]))

                # Формуємо запит вставлення
                query = f"INSERT INTO {table_name} VALUES ({placeholders})"

                cur.execute("PRAGMA foreign_keys = ON;")

                # Запускаємо запит
                cur.executemany(query, data)

                # Перевіряємо відповідність обмеженням NOT NULL
                cur.execute("PRAGMA integrity_check;")

                # Підтверджуємо зміни
                con.commit()
            self._show_success_notification("Записи були успішно додані до бази даних.")
            return True
        # Обробка помилок вставлення, якщо вони виникнуть
        except sq.Error as error:
            if source == "file":
                error_message = f"""<b>Помилка при додаванні записів:</b><br><br>
                                    Некоректний формат даних, або наявні конфліктні значення.<br><br>
                                    Детальний опис помилки:<br>
                                    {error}"""
            else:
                error_message = f"""<b>Помилка при додаванні записів:</b><br><br>
                                    {error}"""
            self._show_error(error_message)
            return False

    def __db_update_data(self, table_name, table_idcol_name, column_names, row_id, new_data):
        """
        Метод оновлює запис у БД (1 рядок)
        :param table_name: назва таблиці для оновлення даних
        :param table_idcol_name: назва поля ID таблиці
        :param column_names: назва оновлювального рядку
        :param row_id: назви оновлювальних рядків
        :param new_data: дані для оновлення
        :return: True, False (успіх виконання запиту)
        """
        try:
            with sq.connect("database.db") as con:
                cursor = con.cursor()

                # Формуємо запит оновлення
                update_query = f"UPDATE {table_name} SET "
                update_query += ", ".join(f"{column} = ?" for column in column_names)
                update_query += f" WHERE {table_idcol_name} = {row_id}"

                cursor.execute(update_query, new_data)
                con.commit()
            self._show_success_notification("Запис був успішно оновлений в базі даних.")
            return True
        except sq.Error as error:
            error_message = f"""<b>Помилка при видаленні записів:</b><br><br>
                                {error}"""
            self._show_error(error_message)
            return False

    def __db_delete_data(self, table_name, table_id_name, id_list):
        """
        Метод видаляє записи з БД (1 чи більше рядків)
        :param table_name: назва таблиці для видалення даних
        :param table_id_name: назва поля ID таблиці
        :param id_list: список ID записів,
        :return: True, False (успіх виконання запиту)
        """
        try:
            with sq.connect("database.db") as con:
                cur = con.cursor()

                # Створюємо рядок для перевірки умови IN
                placeholders = ','.join(['?'] * len(id_list))

                # Перевіряємо відповідність обмеженням на зовнішні ключі
                cur.execute("PRAGMA foreign_keys = ON;")

                # Формуємо запит для видалення рядків із заданими ID
                query = f"DELETE FROM {table_name} WHERE {table_id_name} IN ({placeholders})"

                cur.execute(query, id_list)
                con.commit()
            # Выводим уведомление об успешном удалении
            self._show_success_notification(f"""<b>Записи були успішно видалені з бази даних.</b><br><br>
                                          Кількість видалених записів: {len(id_list)}""")
            return True
        except sq.Error as error:
            error = str(error)
            error_message = "<b>Помилка при видаленні записів:</b><br><br>"
            if error == "FOREIGN KEY constraint failed":
                error_message += "Вказані записи містяться в інформації інших таблиць (FOREIGN KEY)"
            else:
                error_message += error
            self._show_error(error_message)
            return False

    @staticmethod
    def __convert_str_to_type(data):
        """
        Метод конвертує рядкові дані у їх буквальний тип python
        :param data: рядок для обробки
        :return: Any
        """
        value = str(data)
        if len(value) > 10:
            return value
        try:
            value = ast.literal_eval(str(data))
            return value
        # Обробка помилки, якщо дані не вдалося конвертувати
        except (SyntaxError, ValueError):
            return value
