from PyQt5.QtCore import Qt, QDateTime, QRect
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QSpinBox, QFileDialog
from ValidatedDialog import ValidatedDialog


class AddRecordsDialog(ValidatedDialog):
    """
    Класс діалогового вікна додавання записів
    """
    def __init__(self, table):
        """
        :param table: посилання на відповідну таблицю, в яку треба вставити дані
        """
        super(AddRecordsDialog, self).__init__()
        self.setWindowTitle("Додати запис")
        self.setModal(True)
        self.setFixedSize(600, 128)

        self.__table = table                                # Посилання на таблицю
        self.__table_name = table.get_table_name()          # Назва таблиці
        self.__column_names = table.get_column_names()      # Назви рядків таблиці

        self.__form_layout = QVBoxLayout(self)              # Макет форми
        self.__input_layout = QVBoxLayout(self)             # Макет вхідних даних

        count_layout = QHBoxLayout(self)                    # Макет вибору кількості записів
        self.__spin_box = QSpinBox()                        # Вікно прокрутки для вибору кількості записів
        self.__spin_box.setMinimum(1)
        self.__spin_box.setMaximum(10)
        self.__spin_box.valueChanged.connect(self.__spin_changed)
        count_label = QLabel("Оберіть кількість записів: ", self)
        count_layout.setContentsMargins(0, 0, 400, 0)
        count_layout.setGeometry(QRect(120, 500, 111, 300))
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.__spin_box, alignment=Qt.AlignLeft)

        # Знаходимо останній ID таблиці для автоматичного формування ID у формі
        self.__last_id = self._db_find_max_id(table.get_db_table_name(), table.get_db_id_name())
        self.__form_layout.addLayout(count_layout)
        self.__file_list = []

        # Список зберігає усі поля вводу з їх даними
        self.__input_rows = []

        self.__insert_first_row()

        # Створюємо кнопки
        self.__add_buttons = QHBoxLayout()
        self.__submit_button = QPushButton("Додати", self)
        self.__submit_button.setFixedSize(60, 25)
        self.__submit_button.setEnabled(False)
        self.__submit_button.clicked.connect(self._try_to_accept)
        add_file_button = QPushButton("Додати з файлу", self)
        add_file_button.setFixedSize(100, 25)
        add_file_button.clicked.connect(self.__add_from_file)
        self.__add_buttons.addWidget(add_file_button, alignment=Qt.AlignRight)
        self.__add_buttons.addWidget(self.__submit_button, alignment=Qt.AlignRight)
        self.__add_buttons.setContentsMargins(400, 0, 0, 0)

        self.__form_layout.addLayout(self.__input_layout)
        self.__form_layout.addLayout(self.__add_buttons)

    def __insert_first_row(self):
        """
        Метод формує перший рядок вікна додавання записів
        :return: None
        """
        cols_count = len(self.__column_names)
        row = [-1] * cols_count
        input_row_layout = QHBoxLayout(self)
        input_row_layout.addWidget(QLabel("1  ", self), alignment=Qt.AlignBottom)
        for i in range(cols_count):
            print(self.__column_names[i])
            first_row_block = QVBoxLayout(self)
            column_label = QLabel(self.__column_names[i], self)
            line_edit = QLineEdit(self)
            if i == 0:
                line_edit.setText(str(int(self.__last_id) + 1))
            line_edit.editingFinished.connect(lambda: self.__spin_box.setDisabled(True))
            line_edit.editingFinished.connect(lambda j=i, value=line_edit:
                                              self._validation(self.__table_name, self.__column_names[j],
                                                               self.__table.get_db_table_name(),
                                                               self.__table.get_db_id_name(),
                                                               value, row, j))
            line_edit.textChanged.connect(self.__check_enable_button)
            row[i] = line_edit
            first_row_block.addWidget(column_label, alignment=Qt.AlignTop)
            first_row_block.addWidget(line_edit)

            input_row_layout.addLayout(first_row_block)
        self.__input_layout.addLayout(input_row_layout)
        self.__input_rows.append(row)
        print(self.__input_rows)

    def __insert_addition_rows(self):
        """
        Метод формує додаткові рядки вікна додавання записів
        :return: None
        """
        cols_count = len(self.__column_names)
        for i in range(1, self.__spin_box.value()):
            input_row_layout = QHBoxLayout(self)
            row = [-1] * cols_count
            if i != 9:
                input_row_layout.addWidget(QLabel(str(i + 1) + "  ", self))
            else:
                input_row_layout.addWidget(QLabel("10", self))
            for j in range(cols_count):
                line_edit = QLineEdit(self)
                if j == 0:
                    line_edit.setText(str(int(self.__last_id) + (i + 1)))

                line_edit.editingFinished.connect(lambda: self.__spin_box.setDisabled(True))
                line_edit.editingFinished.connect(lambda k=j, value=line_edit, r=row:
                                                  self._validation(self.__table_name, self.__column_names[k],
                                                                   self.__table.get_db_table_name(),
                                                                   self.__table.get_db_id_name(),
                                                                   value, r, k))
                line_edit.textChanged.connect(self.__check_enable_button)

                row[j] = line_edit
                input_row_layout.addWidget(line_edit)
            self.__input_layout.addLayout(input_row_layout)
            self.__input_rows.append(row)
        self.__form_layout.addLayout(self.__input_layout)
        self.__form_layout.addLayout(self.__add_buttons)

    def __spin_changed(self):
        """
        Метод формує вигляд вікна та кількість рядків вводу у випадку зміни значення поля прокруту
        :return: None
        """
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    clear_layout(item.layout())

        self.__input_rows.clear()
        self.__form_layout.removeWidget(self.__submit_button)
        clear_layout(self.__input_layout)
        new_width = 100 + 28 * self.__spin_box.value()
        self.setFixedHeight(new_width)

        self.__insert_first_row()
        self.__insert_addition_rows()

    def __check_enable_button(self):
        """
        Метод перевіряє умову становлення кнопки "додати" доступною та виконує відповідну дію
        :return: None
        """
        # Кнопка "додати" стає доступною лише якщо всі редаговані рядки містять текст
        enable_button = all(line_edit.text() for row in self.__input_rows for line_edit in row)
        self.__submit_button.setEnabled(enable_button)

    def __add_from_file(self):
        """
        Метод виконує відкриття вікна додавання даних з файлу та його подальше оперування
        :return: None
        """
        self._show_information("Умови формату", """Ваші дані мають бути записані у форматах: <br><br>
                                            [6, 'Відділ №6', '+380664255521', '2023-11-11', '11:25']<br>
                                            [7, 'Відділ №7', '+380994111121', '2023-11-12', '14:40']<br>
                                            [9, 'Відділ №9', '+380952222521', '2023-11-05', '19:40']<br><br>
                                            Кожен запис повинен заповнити кожне поле відповідної таблиці.""")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt);;All Files (*)",
                                               options=options)
        if fname:
            try:
                with open(fname, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        sublist = eval(line)
                        self.__file_list.append(sublist)
                    print(self.__file_list)
                    self.accept()
            except OSError:
                self._show_error(f"Не вдалося відкрити/прочитати файл: {fname}")
                return
            except SyntaxError:
                self._show_error(f"Помилка синтаксису у файлі: {fname}")
                return

    def _try_to_accept(self):
        """
        Метод виконує поверхневу валідацію сумісності з іншими даними таблиці
        :return: None
        """
        def check_for_overlapping_intervals():
            count = len(self.__input_rows)

            dt = []
            for i in range(count):
                date_in = str(self.__input_rows[i][3].text())
                date_out = str(self.__input_rows[i][4].text())
                time_in = str(self.__input_rows[i][5].text())
                time_out = str(self.__input_rows[i][6].text())

                datetime_in = QDateTime.fromString(f"{date_in}, {time_in}", 'yyyy-MM-dd, hh:mm')
                datetime_out = QDateTime.fromString(f"{date_out}, {time_out}", 'yyyy-MM-dd, hh:mm')
                dt.append((datetime_in, datetime_out))

            dt_table = self.__table.get_time_data()

            for i in range(count):
                check_id = self.__input_rows[i][2].text()
                for j in range(i + 1, count):
                    compare_id = self.__input_rows[j][2].text()
                    if check_id == compare_id:
                        if self._are_time_intervals_overlap(dt[i][0], dt[i][1], dt[j][0], dt[j][1]):
                            err_text = f"""<b>Помилкові дані</b>
                                             <br><br>Часові інтервали використання одного
                                              комп'ютера не мають пересікатись.<br>
                                             <br>ID комп'ютера: {check_id}
                                             <br>Конфліктні дані: рядки №{i + 1} та №{j + 1}"""
                            self._show_warning(err_text)
                            return True
                for j in range(len(dt_table)):
                    compare_id = dt_table[j][1]
                    if check_id == compare_id:
                        if self._are_time_intervals_overlap(dt[i][0], dt[i][1], dt_table[j][2], dt_table[j][3]):
                            err_text = f"""<b>Помилкові дані</b>
                                             <br><br>Часові інтервали використання 
                                             одного комп'ютера не мають пересікатись.<br>
                                             <br>ID комп'ютера: {check_id}
                                             <br>Конфліктні дані: рядок №{i + 1} та запис таблиці: 
                                             ID = {dt_table[j][0]}"""
                            self._show_warning(err_text)
                            return True
            return False

        unique_ids = set()
        for row in self.__input_rows:
            unique_ids.add(row[0].text())
        if len(unique_ids) < len(self.__input_rows):
            error_text = """<b>Помилкові дані</b>
                            <br><br>Усі ID мають бути унікальними.<br>"""
            self._show_warning(error_text)
            return
        elif self.__table_name == "Входи/Виходи":
            if check_for_overlapping_intervals():
                return
        self.accept()

    def get_record_data(self):
        """
        Метод виконує обробку вписаних даних
        :return: list даних для вставлення даних
        """
        if self.__file_list:
            source = "file"
            return [[self._convert_str_to_type(str(elem)) for elem in row] for row in self.__file_list], source
        else:
            source = "manual_input"
            return [[self._convert_str_to_type(str(elem.text())) for elem in row] for row in self.__input_rows], source
