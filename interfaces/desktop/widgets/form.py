from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSplitter
from PySide6.QtCore import Qt

# ================================================================================

class Form(QWidget):
    def __init__(self, widgets: list[QWidget] | QWidget):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        if isinstance(widgets, list):
            for widget in widgets:
                self.layout.addWidget(widget)
        elif isinstance(widgets, QWidget):
            self.layout.addWidget(widgets)

# ================================================================================

class SubmitForm(Form):
    def __init__(widgets: list[QWidget] | QWidget, submit_button: QPushButton):
        super().__init__(widgets)

        self.layout.addWidget(submit_button)
        
# ================================================================================

class AddDelSubmitForm(Form):
    def __init__(
        self, 
        widgets: list[QWidget] | QWidget, 
        submit_button: QPushButton,
        add_button: QPushButton,
        del_button: QPushButton
    ):
        super().__init__(widgets)

        button_box = QHBoxLayout()
        button_box.addWidget(add_button)
        button_box.addWidget(del_button)
        button_box.addWidget(submit_button)

        self.layout.addLayout(button_box)



