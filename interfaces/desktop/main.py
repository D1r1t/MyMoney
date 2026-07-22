import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTabWidget
)
from pages.categories_page import CategoriesPage
from pages.main_page import MainPage

from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Семейный бюджет")
        self.setMinimumSize(1200, 800)

        tabs = QTabWidget()
        tabs.addTab(MainPage(), "Главная")
        tabs.addTab(CategoriesPage(), "Категории")

        #central = QWidget()
        self.setCentralWidget(tabs)

        self.layout = QVBoxLayout(tabs)
        self.setContentsMargins(20,20,20,20)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    apply_stylesheet(app, theme="dark_amber.xml")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())