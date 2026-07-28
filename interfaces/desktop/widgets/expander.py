from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QSplitter
from PySide6.QtCore import Qt

# ================================================================================

class Expander(QWidget):
    def __init__(self, title: str, content: QWidget | QVBoxLayout, expanded=False):
        super().__init__()

        self.expanded = expanded

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        # self.layout.setSpacing(0)

         # кнопка-заголовок
        self.toggle_btn = QPushButton(f"{title}")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(expanded)
        self.toggle_btn.clicked.connect(self.on_toggle)
        self.layout.addWidget(self.toggle_btn, alignment = Qt.AlignmentFlag.AlignTop)

        if isinstance(content, QWidget):
            self.content_widget = content
        elif isinstance(content, QVBoxLayout):
            self.content_widget = QWidget()
            self.content_widget.setLayout(content)

        self.layout.addWidget(self.content_widget)
        self.content_widget.setVisible(self.expanded)

# --------------------------------------------------------------------------------

    def on_toggle(self, checked):
        self.content_widget.setVisible(checked)

        

