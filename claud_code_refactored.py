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

        # ---- main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)

        # --- Row 1 ---
        row_layout = QHBoxLayout()
        main_layout.addLayout(row_layout)

        widget       = QPushButton("Button 1")
        self.button1 = widget
        widget.clicked.connect( self.on_button1_clicked )
        row_layout.addWidget( widget )

        widget        = QLabel("Label 1")
        self.label1   = widget
        widget.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        row_layout.addWidget( widget )

        # --- Row 2 ---
        row_layout = QHBoxLayout()
        main_layout.addLayout(row_layout)

        widget       = QPushButton("Button 2")
        self.button2 = widget
        widget.clicked.connect( self.on_button2_clicked )
        row_layout.addWidget( widget )

        widget        = QLabel("Label 2")
        self.label2   = widget
        widget.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        row_layout.addWidget( widget )

        # --- Row 3 ---
        row_layout = QHBoxLayout()
        main_layout.addLayout(row_layout)

        widget       = QPushButton("Button 3")
        self.button1 = widget
        widget.clicked.connect( self.on_button3_clicked )
        row_layout.addWidget( widget )

        widget        = QLabel("Label 3")
        self.label3   = widget
        widget.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        row_layout.addWidget( widget )


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