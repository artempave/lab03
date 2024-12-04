# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLabel, QLineEdit, QHBoxLayout, QMessageBox, QMenuBar
)
from Library.TranslateWord import TranslateWord
import matplotlib.pyplot as plt



class WordError(Exception):
    pass


class LanguageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Learning App")
        self.setGeometry(100, 100, 600, 400)

        self.words = []
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Слово", "Перевод"])
        layout.addWidget(self.table)

        self.word_input = QLineEdit(self)
        self.word_input.setPlaceholderText("Введите слово")
        layout.addWidget(self.word_input)

        add_button = QPushButton("Перевести", self)
        add_button.clicked.connect(self.add_word)
        layout.addWidget(add_button)

        graph_button = QPushButton("Показать график активности", self)
        graph_button.clicked.connect(self.show_graph)
        layout.addWidget(graph_button)

        self.log_label = QLabel("Лог активности:", self)
        layout.addWidget(self.log_label)

        main_widget.setLayout(layout)
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")

        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)

    def add_word(self):
        word = self.word_input.text().strip()
        trans = []
        tr = TranslateWord()
        tr.translate_word(word, "ru", "en", trans)
        translation = trans[0]
        try:
            if not word or not translation:
                raise WordError("Слово не может быть пустым.")
            self.words.append((word, translation))
            self.update_table()
            self.word_input.clear()
            self.log_activity(f"Добавлено: {word} - {translation}")
        except WordError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def update_table(self):
        self.table.setRowCount(len(self.words))
        for row, (word, translation) in enumerate(self.words):
            self.table.setItem(row, 0, QTableWidgetItem(word))
            self.table.setItem(row, 1, QTableWidgetItem(translation))

    def log_activity(self, message):
        self.log_label.setText(self.log_label.text() + f"\n{message}")

    def show_graph(self):
        words_count = len(self.words)
        labels = ['Слов', 'Переводов']
        sizes = [words_count, words_count]

        plt.bar(labels, sizes, color=['red', 'blue'])
        plt.title("Активность изучения слов")
        plt.xlabel("Категории")
        plt.ylabel("Количество")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LanguageApp()
    window.show()
    sys.exit(app.exec())

