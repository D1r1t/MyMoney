from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDateEdit,
    QSplitter, QComboBox 
)

from PySide6.QtCore import (
    QDate, Qt 
)

import core.service.currency_processing       as serv_cur_proc 
import core.service.account_processing        as serv_acc_proc 
import core.service.categories_processing     as serv_cat_proc

from core.exceptions import CategoryAlreadyExistsError, AppError
from widgets.table import BaseTable

# ================================================================================

class AccountsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)

        layout.addWidget(QLabel("<h2>Счета</h2>"))

        self.table = BaseTable(["Счет", "Валюта"])

        layout.addWidget(self.table)

        layout.addWidget(QLabel("<b>Добавить счет:</b>"))
        
        form_layout = QHBoxLayout()

        self.acc_name = QLineEdit()
        self.acc_name.setPlaceholderText("Название счета")

        self.currency = QComboBox()
        self.currency.setMinimumWidth(150)
        currencies = serv_cur_proc.get_all_currencies()
        for cur in currencies:
            self.currency.addItem(str(cur.cur_name), cur)
        
        form_layout.addWidget(self.acc_name)
        form_layout.addWidget(self.currency)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)
        

        self.load_data()

# --------------------------------------------------------------------------------

    def load_data(self):
        accounts = serv_acc_proc.get_all_accounts()
        self.table.fill([
            [acc.acc_name, acc.currency.cur_name] for acc in accounts
        ])

# --------------------------------------------------------------------------------

    def on_add(self):
        serv_acc_proc.create_new_account(self.acc_name.text(), self.currency.currentData())
        self.load_data()