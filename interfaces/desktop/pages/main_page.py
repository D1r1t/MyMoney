from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QTableWidget, QLabel, QTabWidget 
)

from core.exceptions import CategoryAlreadyExistsError, AppError
from pages.main_page_tabs.expenses_tab import ExpansesTab
from pages.main_page_tabs.moves_tab import MovesTab

# ================================================================================

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.addWidget(QLabel("<h2>Главная</h2>"))

        tabs = QTabWidget()

        tabs.addTab(ExpansesTab(), "Расходы")
        tabs.addTab(MovesTab(), "Транзакции")

        layout.addWidget(tabs)        
        