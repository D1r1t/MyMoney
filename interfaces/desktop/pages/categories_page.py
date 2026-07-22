from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox
)

import core.service.categories_processing as serv_cat_proc
from widgets.table import BaseTable
from core.exceptions import CategoryAlreadyExistsError, AppError

class CategoriesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        
        # заголовок
        layout.addWidget(QLabel("<h2>Категории</h2>"))

        # таблица
        # self.table = QTableWidget()
        # self.table.setColumnCount(1)
        # self.table.setHorizontalHeaderLabels(["Категории"])
        # self.table.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeMode.Stretch
        # )
        
        # self.table.setEditTriggers(
        #     QTableWidget.EditTrigger.NoEditTriggers
        # )

        # self.table.setSelectionBehavior(
        #     QTableWidget.SelectionBehavior.SelectRows
        # )
        self.table = BaseTable(["Категория"])

        
        layout.addWidget(self.table)

        # форма добавления
        layout.addWidget(QLabel("<b>Добавить категорию:</b>"))
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название категории")
        form_layout.addWidget(self.name_input)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)

        self.load_data()

    def load_data(self):
        categories = serv_cat_proc.get_all_categories()
        # self.table.setRowCount(len(categories))
        # for i, cat in enumerate(categories):
        #     self.table.setItem(i, 0, QTableWidgetItem(cat.cat_name))
        self.table.fill([
            [cat.cat_name] for cat in categories
        ])

    def on_add(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории")
            return
        
        try:
            serv_cat_proc.create_new_category(name)
            self.name_input.clear()
            self.load_data()
            QMessageBox.information(self, "Успех", f"Категория '{name}' добавлена!")
        except CategoryAlreadyExistsError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except AppError as e:
            QMessageBox.warning(self, "Ошибка", str(e))