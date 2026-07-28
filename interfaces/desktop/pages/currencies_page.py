from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDateEdit,
    QSplitter, QComboBox, QCheckBox 
)

from PySide6.QtCore import (
    QDate, Qt 
)

import core.service.currency_processing       as serv_cur_proc 
import core.service.account_processing        as serv_acc_proc 
import core.service.categories_processing     as serv_cat_proc
import core.service.exchange_rates_processing as serv_ex_rat_proc 
import core.service.moves_processing          as serv_mov_proc
import core.service.views_processing          as serv_view_proc

import pandas as pd

from core.exceptions import CategoryAlreadyExistsError, AppError
from widgets.table import BaseTable, FullEditableTable
from widgets.expander import Expander
from widgets.form import Form, AddDelSubmitForm

# ================================================================================

class CurrenciesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)

        layout.addWidget(QLabel("<h2>Валюты</h2>"))

        self.table = BaseTable(["Валюта", "Основная"])

        layout.addWidget(self.table)

        layout.addWidget(QLabel("<b>Добавить валюту:</b>"))
        
        form_layout = QHBoxLayout()

        self.cur_name = QLineEdit()
        self.cur_name.setPlaceholderText("Название валюты")

        self.is_main = QCheckBox()

        
        form_layout.addWidget(self.cur_name)
        form_layout.addWidget(self.is_main)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)
        

        self.load_data()

# --------------------------------------------------------------------------------

    def load_data(self):
        currencies = serv_cur_proc.get_all_currencies()
        self.table.fill([
            [cur.cur_name, cur.is_main] for cur in currencies
        ])

# --------------------------------------------------------------------------------

    def on_add(self):
        serv_cur_proc.create_new_currency(self.cur_name.text(), self.is_main.isChecked())
        
        self.load_data()