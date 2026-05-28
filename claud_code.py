import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt6 Button & Label Widget")
        self.setMinimumWidth(400)

        # --- Row 1 ---
        self.button1 = QPushButton("Button 1")
        self.label1  = QLabel("Label 1")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.button1.clicked.connect(self.on_button1_clicked)

        row1 = QHBoxLayout()
        row1.addWidget(self.button1)
        row1.addWidget(self.label1)

        # --- Row 2 ---
        self.button2 = QPushButton("Button 2")
        self.label2  = QLabel("Label 2")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.button2.clicked.connect(self.on_button2_clicked)

        row2 = QHBoxLayout()
        row2.addWidget(self.button2)
        row2.addWidget(self.label2)

        # --- Row 3 ---
        self.button3 = QPushButton("Button 3")
        self.label3  = QLabel("Label 3")
        self.label3.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.button3.clicked.connect(self.on_button3_clicked)

        row3 = QHBoxLayout()
        row3.addWidget(self.button3)
        row3.addWidget(self.label3)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)

        self.setLayout(main_layout)

    def on_button1_clicked(self):
        self.label1.setText("Button 1 was clicked!")

    def on_button2_clicked(self):
        self.label2.setText("Button 2 was clicked!")

    def on_button3_clicked(self):
        self.label3.setText("Button 3 was clicked!")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()