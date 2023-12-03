from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QDialog


class AboutProgramDialog(QDialog):
    """
    Клас відповідає за діалогове вікно "Про програму"
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Про програму")
        self.setFixedSize(400, 400)

        # Об'єкт вікна з вкладинками
        tab_widget = QTabWidget()

        # Вкладка "Про программу"
        about_program_tab = QWidget()
        about_program_layout = QVBoxLayout()
        about_program_layout.addWidget(QLabel("Назва програми: Computer Usage Control"))
        about_program_layout.addWidget(QLabel("Версія програми: 1.0"))
        about_program_layout.addWidget(QLabel("Розробник: Воловик Артем Вікторович"))
        about_program_layout.addWidget(QLabel("Опис програми: ця програма призначена для моніторингу часу<br> "
                                              "використання комп'ютерів підприємства та підведення статистики."))
        about_program_layout.addSpacing(470)
        about_program_tab.setLayout(about_program_layout)
        tab_widget.addTab(about_program_tab, "Про программу")

        # Вкладка "Про розробника"
        about_developer_tab = QWidget()
        about_developer_layout = QVBoxLayout()
        about_developer_layout.addWidget(QLabel("Ім'я розробника: Воловик Артем Вікторович"))
        about_developer_layout.addWidget(QLabel("Місце навчання: ХНЕУ імені Семена Кузнеця"))
        about_developer_layout.addWidget(QLabel("Контактна інформація: artem.volovyk@hneu.net"))
        pixmap = QPixmap("images/developer_photo.jpg").scaledToHeight(250)
        photo = QLabel()
        photo.setPixmap(pixmap)
        about_developer_layout.addWidget(photo, alignment=Qt.AlignCenter)
        about_developer_tab.setLayout(about_developer_layout)
        tab_widget.addTab(about_developer_tab, "Про розробника")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)
