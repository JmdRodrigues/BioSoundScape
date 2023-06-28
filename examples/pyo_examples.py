import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Navigation Example")
        self.setGeometry(100, 100, 400, 200)

        # Create a main widget and layout
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        # Create a label and button in the main widget
        self.label = QLabel("Main Page", self.main_widget)
        self.layout.addWidget(self.label)
        self.next_button = QPushButton("Next", self.main_widget)
        self.next_button.clicked.connect(self.nextClicked)
        self.layout.addWidget(self.next_button)

        # Set the main widget as the central widget
        self.setCentralWidget(self.main_widget)

        # Create a new page widget
        self.next_page = QWidget(self)
        self.next_layout = QVBoxLayout(self.next_page)

        # Create a label and button in the new page widget
        self.next_label = QLabel("Next Page", self.next_page)
        self.next_layout.addWidget(self.next_label)
        self.back_button = QPushButton("Back", self.next_page)
        self.back_button.clicked.connect(self.backClicked)
        self.next_layout.addWidget(self.back_button)

    def nextClicked(self):
        # Set the new page widget as the central widget
        self.setCentralWidget(self.next_page)
        # self.main_widget.deleteLater()

    def backClicked(self):
        # Set the main widget as the central widget
        self.setCentralWidget(self.main_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
