import sys

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
)

from search_db import search_db


class Search(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.search_field_label = QLabel("Іздеу сұранысы:", self)
        self.search_field_label.move(50, 10)

        self.search_field = QLineEdit("Іздеу сұранысты енгізіңіз", self)
        self.search_field.setFixedWidth(200)
        self.search_field.move(160, 10)

        self.tokenization_check_box = QCheckBox("Токенизация", self)
        self.tokenization_check_box.setFixedWidth(200)
        self.tokenization_check_box.move(50, 40)

        self.normalization_check_box = QCheckBox("Нормализация", self)
        self.normalization_check_box.setFixedWidth(200)
        self.normalization_check_box.setEnabled(False)
        self.normalization_check_box.move(50, 60)

        self.morph_check_box = QCheckBox("Морфологиялық талдау", self)
        self.morph_check_box.setFixedWidth(200)
        self.morph_check_box.setEnabled(False)
        self.morph_check_box.move(50, 80)

        self.search_button = QPushButton("Іздеу", self)
        self.search_button.setToolTip("Іздеу")
        self.search_button.move(150, 120)
        self.search_button.clicked.connect(self.search_button_click)

        self.result_field = QPlainTextEdit("Нәтижелер шығатын орны", self)
        self.result_field.setFixedWidth(320)
        self.result_field.setFixedHeight(350)
        self.result_field.move(50, 170)

        self.setGeometry(300, 300, 420, 550)
        self.setWindowTitle("Іздеу")
        self.show()

    def search_button_click(self):
        search_query = self.search_field.text()

        if self.tokenization_check_box.isChecked():
            search_result = search_db(query=search_query, mode="tokenized")
        else:
            search_result = search_db(query=search_query, mode="default")

        num_found = len(search_result)
        if self.tokenization_check_box.isChecked():
            output = "Tokenized search mode is on.\n\n"
        else:
            output = ""
        output += f"{num_found} құжат табылды.\n"
        output += "\n"
        for found_item in search_result:
            output += "url-адрес:\n" + found_item[0]
            output += "\n"
            output += "Тақырыптық бөлімі:\n" + found_item[1]
            output += "\n"
            output += "Құжат тақырыбы:\n" + found_item[2]
            output += "\n"
            output += "Уақыты:\n" + found_item[3]
            output += "\n"
            output += "\n"
        self.result_field.setPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Search()
    sys.exit(app.exec_())
