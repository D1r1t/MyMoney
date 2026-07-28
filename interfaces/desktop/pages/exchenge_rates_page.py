from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDateEdit,
    QSplitter, QComboBox, QCheckBox
)

from PySide6.QtCore import (
    QDate, Qt, QLocale
)

from PySide6.QtGui import (
    QDoubleValidator
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
from datetime import date, datetime

# ================================================================================

class ExchangeRatesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)

        layout.addWidget(QLabel("<h2>Курсы валют</h2>"))

        # фильтр дат
        date_layout = QHBoxLayout()

        date_layout.addWidget(QLabel("С:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(
            -(QDate.currentDate().day() - 1)  # первый день месяца
        ))
        date_layout.addWidget(self.date_from)

        date_layout.addWidget(QLabel("По:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_to)

        btn = QPushButton("Обновить")
        btn.clicked.connect(self.load_rates)
        date_layout.addWidget(btn)

        self.table = BaseTable(["Дата", "Расчетная", "Текущая", "Курс"])

        layout.addWidget(self.table)

        layout.addWidget(QLabel("<b>Добавить курс:</b>"))

        form_layout = QHBoxLayout()

        self.rate_date = QDateEdit()
        self.rate_date.setCalendarPopup(True)
        self.rate_date.setDate(QDate.currentDate())

        currencies = serv_cur_proc.get_all_currencies()

        self.main_currency = QComboBox()
        self.main_currency.setMinimumWidth(150)

        self.cur_currency = QComboBox()
        self.cur_currency.setMinimumWidth(150)
        
        for cur in currencies:
            self.cur_currency.addItem(str(cur.cur_name), cur)
            self.main_currency.addItem(str(cur.cur_name), cur)

        validator = QDoubleValidator(0, 9999999999, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        # устанавливаем точку как разделитель независимо от локали ОС
        locale = QLocale(QLocale.C)

        self.rate = QLineEdit()
        self.rate.setPlaceholderText("Курс")
        self.rate.setValidator(validator)

        
        form_layout.addWidget(self.rate_date)
        form_layout.addWidget(self.main_currency)
        form_layout.addWidget(self.cur_currency)
        form_layout.addWidget(self.rate)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)
        

        self.load_rates()

# --------------------------------------------------------------------------------

    def load_rates(self):
        rates = serv_ex_rat_proc.get_all_rates(
            self.date_from.date().toPython(),
            self.date_to.date().toPython()
        )

        self.table.fill([
            [
                rate.rate_date, 
                rate.main_currency.cur_name, 
                rate.current_currency.cur_name, 
                rate.rare
            ] for rate in rates
        ])

# --------------------------------------------------------------------------------

    def on_add(self):
        serv_ex_rat_proc.create_new_exchange_rate(
            self.rate_date.date().toPython(),
            self.main_currency.currentData(), 
            self.cur_currency.currentData(), 
            float(self.rate.text().replace(",","."))
        )
        self.load_rates()

        self.rate.clear()
