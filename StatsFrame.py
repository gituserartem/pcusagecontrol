import sqlite3 as sq
from datetime import datetime
from PyQt5.QtWidgets import (QPushButton, QLabel, QFrame, QDateTimeEdit)
from PyQt5.QtCore import QRect, Qt, QDateTime
from PopUpNotificationsImporter import PopUpNotificationsImporter


class StatsFrame(QFrame, PopUpNotificationsImporter):
    """
    Клас відповідає за формування вікна статистики
    """
    def __init__(self, parent=None):
        """
        :param parent: об'єкт, до якого буде прив'язаний фрейм статистики
        """
        super(StatsFrame, self).__init__(parent)
        self.setGeometry(QRect(151, 40, 851, 560))
        self.setStyleSheet("background-color: rgb(222, 222, 222);")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("stats_frame")

        total_time_frame = QFrame(self)
        total_time_frame.setGeometry(QRect(30, 90, 381, 201))
        total_time_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        total_time_frame.setFrameShape(QFrame.StyledPanel)
        total_time_frame.setFrameShadow(QFrame.Raised)
        total_time_frame.setObjectName("total_time_frame")
        tt_name = QLabel(total_time_frame)
        tt_name.setGeometry(QRect(70, 10, 241, 51))
        tt_name.setStyleSheet("font: 81 12pt \"Geologica ExtraBold\";")
        tt_name.setAlignment(Qt.AlignCenter)
        tt_name.setObjectName("tt_name")
        self.__tt_value = QLabel(total_time_frame)
        self.__tt_value.setGeometry(QRect(40, 80, 301, 51))
        self.__tt_value.setStyleSheet("font: 81 20pt \"Geologica ExtraBold\";\n"
                                      "color: rgb(0, 85, 255);")
        self.__tt_value.setAlignment(Qt.AlignCenter)
        self.__tt_value.setObjectName("tt_value")

        avg_pc_use_time_frame = QFrame(self)
        avg_pc_use_time_frame.setGeometry(QRect(440, 90, 381, 201))
        avg_pc_use_time_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        avg_pc_use_time_frame.setFrameShape(QFrame.StyledPanel)
        avg_pc_use_time_frame.setFrameShadow(QFrame.Raised)
        avg_pc_use_time_frame.setObjectName("avg_pc_use_time_frame")
        avgput_name = QLabel(avg_pc_use_time_frame)
        avgput_name.setGeometry(QRect(70, 10, 241, 51))
        avgput_name.setStyleSheet("font: 81 12pt \"Geologica ExtraBold\";")
        avgput_name.setAlignment(Qt.AlignCenter)
        avgput_name.setObjectName("avgput_name")
        self.__avgput_value = QLabel(avg_pc_use_time_frame)
        self.__avgput_value.setGeometry(QRect(40, 80, 301, 51))
        self.__avgput_value.setStyleSheet("font: 81 20pt \"Geologica ExtraBold\";\n"
                                          "color: rgb(255, 148, 17);")
        self.__avgput_value.setAlignment(Qt.AlignCenter)
        self.__avgput_value.setObjectName("avgput_value")
        avgput_total_count_caption = QLabel(avg_pc_use_time_frame)
        avgput_total_count_caption.setGeometry(QRect(20, 160, 201, 31))
        avgput_total_count_caption.setStyleSheet("font: 57 11pt \"Wix Madefor Display Medium\";")
        avgput_total_count_caption.setObjectName("avgput_total_count_caption")
        self.__avgput_total_count = QLabel(avg_pc_use_time_frame)
        self.__avgput_total_count.setGeometry(QRect(125, 160, 150, 31))
        self.__avgput_total_count.setStyleSheet("font: 81 11pt \"Wix Madefor Display ExtraBold\";")
        self.__avgput_total_count.setObjectName("avgput_total_count")

        avg_each_pc_use_time_frame = QFrame(self)
        avg_each_pc_use_time_frame.setGeometry(QRect(30, 320, 381, 201))
        avg_each_pc_use_time_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        avg_each_pc_use_time_frame.setFrameShape(QFrame.StyledPanel)
        avg_each_pc_use_time_frame.setFrameShadow(QFrame.Raised)
        avg_each_pc_use_time_frame.setObjectName("avg_each_pc_use_time_frame")
        avgeput_name = QLabel(avg_each_pc_use_time_frame)
        avgeput_name.setGeometry(QRect(70, 10, 241, 51))
        avgeput_name.setStyleSheet("font: 81 12pt \"Geologica ExtraBold\";")
        avgeput_name.setAlignment(Qt.AlignCenter)
        avgeput_name.setObjectName("avgeput_name")
        self.__avgeput_value = QLabel(avg_each_pc_use_time_frame)
        self.__avgeput_value.setGeometry(QRect(40, 80, 301, 51))
        self.__avgeput_value.setStyleSheet("font: 81 20pt \"Geologica ExtraBold\";\n"
                                           "color: rgb(0, 150, 0);")
        self.__avgeput_value.setAlignment(Qt.AlignCenter)
        self.__avgeput_value.setObjectName("avgeput_value")
        avgeput_total_count_caption = QLabel(avg_each_pc_use_time_frame)
        avgeput_total_count_caption.setGeometry(QRect(20, 160, 201, 31))
        avgeput_total_count_caption.setStyleSheet("font: 57 11pt \"Wix Madefor Display Medium\";")
        avgeput_total_count_caption.setObjectName("avgeput_total_count_caption")
        self.__avgeput_total_count = QLabel(avg_each_pc_use_time_frame)
        self.__avgeput_total_count.setGeometry(QRect(207, 160, 150, 31))
        self.__avgeput_total_count.setStyleSheet("font: 81 11pt \"Wix Madefor Display ExtraBold\";")
        self.__avgeput_total_count.setObjectName("avgeput_total_count")

        most_active_day_frame = QFrame(self)
        most_active_day_frame.setGeometry(QRect(440, 320, 381, 201))
        most_active_day_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        most_active_day_frame.setFrameShape(QFrame.StyledPanel)
        most_active_day_frame.setFrameShadow(QFrame.Raised)
        most_active_day_frame.setObjectName("most_active_day_frame")

        maday_name = QLabel(most_active_day_frame)
        maday_name.setGeometry(QRect(70, 10, 241, 51))
        maday_name.setStyleSheet("font: 81 12pt \"Geologica ExtraBold\";")
        maday_name.setAlignment(Qt.AlignCenter)
        maday_name.setObjectName("maday_name")
        self.__maday_value = QLabel(most_active_day_frame)
        self.__maday_value.setGeometry(QRect(40, 80, 301, 51))
        self.__maday_value.setStyleSheet("font: 81 20pt \"Geologica ExtraBold\";\n"
                                         "color: rgb(255, 0, 0);")
        self.__maday_value.setAlignment(Qt.AlignCenter)
        self.__maday_value.setObjectName("maday_value")
        maday_tt_name = QLabel(most_active_day_frame)
        maday_tt_name.setGeometry(QRect(20, 160, 250, 31))
        maday_tt_name.setStyleSheet("font: 57 11pt \"Wix Madefor Display Medium\";")
        maday_tt_name.setObjectName("maday_tt_name")
        self.__maday_tt = QLabel(most_active_day_frame)
        self.__maday_tt.setGeometry(QRect(260, 160, 120, 31))
        self.__maday_tt.setStyleSheet("font: 81 11pt \"Wix Madefor Display ExtraBold\";")
        self.__maday_tt.setObjectName("maday_tt")

        current_datetime = QDateTime.currentDateTime()
        self.__dtin_ledit = QDateTimeEdit(current_datetime.addMonths(-1), parent=self)
        self.__dtin_ledit.setGeometry(QRect(30, 50, 111, 25))
        self.__dtin_ledit.setObjectName("dtin_ledit")
        self.__dtout_ledit = QDateTimeEdit(current_datetime, parent=self)
        self.__dtout_ledit.setGeometry(QRect(170, 50, 111, 25))
        self.__dtout_ledit.setObjectName("dtout_ledit")

        self.__dt_apply_button = QPushButton(self)
        self.__dt_apply_button.setGeometry(QRect(30, 20, 111, 25))
        self.__dt_apply_button.setObjectName("dt_apply_button")
        self.__dt_apply_button.setFocusPolicy(Qt.NoFocus)
        dt_dash = QLabel(self)
        dt_dash.setGeometry(QRect(145, 55, 20, 16))
        dt_dash.setAlignment(Qt.AlignCenter)
        dt_dash.setObjectName("dt_dash")

        self.__apply_period()

        self.__dt_apply_button.clicked.connect(self.__apply_period)

        self.__dt_apply_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(50, 50, 50);
                        color: rgb(255, 255, 255);
                        border: 1px;
                        border-radius: 3px;
                        font: 81 9pt \"Wix Madefor Display Regular\";
                    }

                    QPushButton:hover {
                        background-color: rgb(70, 70, 70);  /* Pressed background color (a darker blue) */
                        color: rgb(255, 255, 255);
                    }

                    QPushButton:pressed {
                        background-color: rgb(0, 0, 0);  /* Hover background color (lighter blue) */
                    }

                    QPushButton:disabled {
                        background-color: #a0a0a0;  /* Disabled background color (gray) */
                        color: #242424;  /* Disabled text color (gray) */
                    }
                """)

        tt_name.setText("Загальний час\nвикористання комп\'ютерів")
        avgput_name.setText("Середня тривалість сесії")
        avgput_total_count_caption.setText("Всього сесій:")
        avgeput_name.setText("Середня тривалість\nвикористання 1 комп'ютера")
        avgeput_total_count_caption.setText("Всього унікальних сесій:")
        maday_name.setText("День запуску\nнайдовших сесій")
        maday_tt_name.setText("Загальний час запущених сесій:")
        self.__dt_apply_button.setText("Застосувати")
        dt_dash.setText("—")

    def __apply_period(self):
        """
        Метод відповідає за виконання сценарію застосування періоду
        :return: None
        """
        dtin_value = self.__dtin_ledit.dateTime()
        dtout_value = self.__dtout_ledit.dateTime()

        # Проверяем, если значение в dtout_ledit больше текущего времени или больше, чем значение в dtin_ledit
        current_datetime = QDateTime.currentDateTime()
        if dtout_value > current_datetime or dtin_value > current_datetime:
            error_text = f"""<b>Помилкові значення дати</b>
                             <br><br>Обрані моменти часу не можуть бути пізніше поточного.<br>"""
            self._show_warning(error_text)
        elif dtout_value < dtin_value:
            error_text = f"""<b>Помилкові значення дати</b>
                             <br><br>Кінець періоду не може бути раніше початку періоду.<br>"""
            self._show_warning(error_text)
        else:
            dtin_str = dtin_value.toString("yyyy-MM-dd HH:mm")
            dtout_str = dtout_value.toString("yyyy-MM-dd HH:mm")
            [success1, total_time] = self.__db_count_total_use_time(dtin_str, dtout_str)
            [success2, avg_time, sessions_count] = self.__db_count_avg_session_time(dtin_str, dtout_str)
            [success3, avg_pc_use_time, unique_sessions_count] = \
                self.__db_count_avg_each_pc_use_time(dtin_str, dtout_str)
            [success4, most_active_day, maday_total_time] = self.__db_count_the_most_active_day(dtin_str, dtout_str)
            if success1 and success2 and success3 and success4:
                self.__tt_value.setText(self.__seconds_to_hm(total_time))
                self.__avgput_value.setText(self.__seconds_to_hms(avg_time))
                self.__avgput_total_count.setText(str(sessions_count))
                self.__avgeput_value.setText(self.__seconds_to_hms(avg_pc_use_time))
                self.__avgeput_total_count.setText(str(unique_sessions_count))
                self.__maday_value.setText(most_active_day)
                self.__maday_tt.setText(self.__seconds_to_hm(maday_total_time))

    def __db_count_avg_each_pc_use_time(self, datetime_start, datetime_end):
        """
        Метод виконує підрахунок середнього часу використання кожного комп'ютера за періодом
        :param datetime_start: початок періоду
        :param datetime_end: кінець періоду
        :return: list - [успішність операції (bool), середній час використання комп'ютерів у секундах,
                        кількість унікальних сесій]
        """
        query = f"""SELECT COUNT(DISTINCT [ID комп'ютера])
                    FROM [Входи/Виходи]
                        WHERE NOT
                            (
                            (datetime([Дата виходу] || ' ' || [Час виходу]) < datetime('{datetime_start}'))
                            OR
                            (datetime([Дата входу] || ' ' || [Час входу]) > datetime('{datetime_end}'))
                            );"""
        try:
            total_time = self.__db_count_total_use_time(datetime_start, datetime_end)[1]
            with sq.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(query)
                unique_sessions_count = cur.fetchone()[0]

                if unique_sessions_count > 0:
                    average_time = total_time / unique_sessions_count
                else:
                    average_time = 0

            return [True, average_time, unique_sessions_count]
        except sq.Error as error:
            error_message = f"""Помилка при розрахунку середнього часу використання комп'ютера:<br><br>
                                {error}"""
            self._show_error(error_message)
            return [False, -1, -1]

    def __db_count_avg_session_time(self, datetime_start, datetime_end):
        """
        Метод виконує підрахунок середнього часу використання кожного комп'ютера за періодом
        :param datetime_start: початок періоду
        :param datetime_end: кінець періоду
        :return: list - [успішність операції (bool), середній час використання комп'ютерів у секундах, кількість сесій]
        """
        query = f"""SELECT COUNT(*) AS session_count
                    FROM [Входи/Виходи]
                        WHERE NOT
                            (
                            (datetime([Дата виходу] || ' ' || [Час виходу]) < datetime('{datetime_start}'))
                            OR
                            (datetime([Дата входу] || ' ' || [Час входу]) > datetime('{datetime_end}'))
                            );"""
        try:
            total_time = self.__db_count_total_use_time(datetime_start, datetime_end)[1]
            with sq.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(query)
                sessions_count = cur.fetchone()[0]

                if sessions_count > 0:
                    average_time = total_time / sessions_count
                else:
                    average_time = 0

            return [True, average_time, sessions_count]
        except sq.Error as error:
            error_message = f"""Помилка при розрахунку середнього часу використання комп'ютера:<br><br>
                                {error}"""
            self._show_error(error_message)
            return [False, -1, -1]

    def __db_count_total_use_time(self, datetime_start, datetime_end):
        """
        Метод виконує підрахунок загальний час використання комп'ютерів за періодом
        :param datetime_start: початок періоду
        :param datetime_end: кінець періоду
        :return: list - [успішність операції (bool), загальний час використання комп'ютерів у секундах]
        """
        query = f"""SELECT
                    SUM(
                        CASE
                            WHEN
                                datetime([Дата входу] || ' ' || [Час входу]) < datetime('{datetime_start}')
                                AND
                                datetime([Дата виходу] || ' ' || [Час виходу]) > datetime('{datetime_end}')
                            THEN
                                strftime('%s', datetime('{datetime_end}')) -
                                strftime('%s', datetime('{datetime_start}'))
                            WHEN
                                datetime([Дата входу] || ' ' || [Час входу]) >= datetime('{datetime_start}')
                                AND
                                datetime([Дата виходу] || ' ' || [Час виходу]) <= datetime('{datetime_end}')
                            THEN
                                strftime('%s', datetime([Дата виходу] || ' ' || [Час виходу])) -
                                strftime('%s', datetime([Дата входу] || ' ' || [Час входу]))
                            WHEN
                                (datetime([Дата входу] || ' ' || [Час входу]) < datetime('{datetime_start}'))
                            AND
                                (datetime([Дата виходу] || ' ' || [Час виходу]) <= datetime('{datetime_end}'))
                            THEN
                                strftime('%s', datetime([Дата виходу] || ' ' || [Час виходу])) -
                                strftime('%s', datetime([Дата входу] || ' ' || [Час входу])) -
                                (
                                strftime('%s', '{datetime_start}') -
                                strftime('%s', datetime([Дата входу] || ' ' || [Час входу]))
                                )
                            WHEN
                                (datetime([Дата входу] || ' ' || [Час входу]) >= datetime('{datetime_start}'))
                                AND
                                (datetime([Дата виходу] || ' ' || [Час виходу]) > datetime('{datetime_end}'))
                            THEN
                                strftime('%s', datetime([Дата виходу] || ' ' || [Час виходу])) -
                                strftime('%s', datetime([Дата входу] || ' ' || [Час входу])) -
                                (
                                strftime('%s', datetime([Дата виходу] || ' ' || [Час виходу])) -
                                strftime('%s', '{datetime_end}')
                                )
                            ELSE 0
                        END
                        ) AS session_duration
                    FROM [Входи/Виходи]
                        WHERE NOT
                            (
                            (datetime([Дата виходу] || ' ' || [Час виходу]) < datetime('{datetime_start}'))
                            OR
                            (datetime([Дата входу] || ' ' || [Час входу]) > datetime('{datetime_end}'))
                            );
                    """
        try:
            with sq.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(query)
                total_time = cur.fetchone()[0]
            if total_time:
                return [True, total_time]
            else:
                return [True, 0]
        except sq.Error as error:
            error_message = f"""Помилка при розрахунку загального часу використання комп'ютерів:<br><br>
                                {error}"""
            self._show_error(error_message)
            return [False, -1]

    def __db_count_the_most_active_day(self, datetime_start, datetime_end):
        """
        Метод знаходить найбільш активний на тривалості запущених сесій день
        :param datetime_start: початок періоду
        :param datetime_end: кінець періоду
        :return: list - [успішність операції (bool), найактивніший день, загальна тривалість сесій запущених цього дня]
        """
        query = f"""SELECT [Дата входу],
                        SUM(strftime('%s', datetime([Дата виходу] || ' ' || [Час виходу])) - 
                        strftime('%s', datetime([Дата входу] || ' ' || [Час входу]))) AS [Сума тривалостей сесій]
                        FROM [Входи/Виходи]
                        WHERE (datetime([Дата входу] || ' ' || [Час входу]) >= datetime('{datetime_start}')) 
                            AND (datetime([Дата виходу] || ' ' || [Час виходу]) <= datetime('{datetime_end}'))
                        GROUP BY [Дата входу]
                        ORDER BY [Сума тривалостей сесій] DESC
                        LIMIT 1;"""
        try:
            with sq.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(query)
                day, time = cur.fetchone()

            day = datetime.strptime(day, "%Y-%m-%d")
            day = day.strftime("%d.%m.%Y")
            return [True, day, time]
        except TypeError:
            return [True, "Відсутній", 0]
        except sq.Error as error:
            error_message = f"""Помилка при розрахунку найбільш активного дня:<br><br>
                                {error}"""
            self._show_error(error_message)
            return [False, -1, -1]

    @staticmethod
    def __seconds_to_hm(seconds):
        """
        Метод переводить секунди у ГГ:ХВ
        :param seconds: кількість секунд
        :return: str - значення годин та хвилин
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} год  {minutes} хв"

    @staticmethod
    def __seconds_to_hms(seconds):
        """
        Метод переводить секунди у ГГ:ХВ:СС
        :param seconds: кількість секунд
        :return: str - значення годин, хвилин та секунд
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int((seconds % 3600) % 60)
        return f"{hours} год  {minutes} хв  {seconds} сек"
