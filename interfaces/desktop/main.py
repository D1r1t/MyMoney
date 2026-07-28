import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QVBoxLayout, QTabWidget
)

from pages.categories_page import CategoriesPage
from pages.main_page import MainPage
from pages.accounts_page import AccountsPage
from pages.currencies_page import CurrenciesPage
from pages.exchenge_rates_page import ExchangeRatesPage

from qt_material import apply_stylesheet

# ================================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Семейный бюджет")
        self.setMinimumSize(800, 600)

        tabs = QTabWidget()
        
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setDocumentMode(True)

        tabs.addTab(MainPage(), "Главная")
        tabs.addTab(CategoriesPage(), "Категории")
        tabs.addTab(AccountsPage(), "Счета")
        tabs.addTab(CurrenciesPage(), "Валюты")
        tabs.addTab(ExchangeRatesPage(), "Курсы")

        #central = QWidget()
        self.setCentralWidget(tabs)

        self.layout = QVBoxLayout(tabs)
        self.setContentsMargins(20,20,20,20)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    apply_stylesheet(app, theme="dark_lightgreen.xml")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())