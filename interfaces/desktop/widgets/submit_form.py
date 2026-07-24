from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QSplitter
from PySide6.QtCore import Qt

class Form(QWidget):
    def __init__(self, widgets: list[QWidget] | QWidget, submit_button: QPushButton):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        if isinstance(widgets, list):
            for widget in widgets:
                self.layout.addWidget(widget)
        elif isinstance(widgets, QWidget):
            self.layout.addWidget(widgets)

        self.layout.addWidget(submit_button)
        
