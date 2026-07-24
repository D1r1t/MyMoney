from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDateEdit,
    QSplitter, QTabWidget 
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
from widgets.table import BaseTable
from widgets.expander import Expander
from widgets.submit_form import Form
from pages.main_page_tabs.expenses_tab import ExpansesTab
from pages.main_page_tabs.moves_tab import MovesTab

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
        