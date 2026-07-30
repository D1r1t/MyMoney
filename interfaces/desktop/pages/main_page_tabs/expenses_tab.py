from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QHeaderView,
    QPushButton, QLabel, QMessageBox, QDateEdit,
    QSplitter, QCheckBox, QComboBox 
)

from PySide6.QtCore import QDate

import core.service.views_processing          as serv_view_proc
import core.service.account_processing        as serv_acc_proc 
import core.service.categories_processing     as serv_cat_proc

import pandas as pd

from core.exceptions import CategoryAlreadyExistsError, AppError
from widgets.table import BaseTable

# ================================================================================

class ExpansesTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)

        # фильтр дат
        filter_layout = QHBoxLayout()

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(
            -(QDate.currentDate().day() - 1)  # первый день месяца
        ))
        
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        

        btn = QPushButton("Обновить")
        btn.clicked.connect(self.load_expenses_data)

        self.acc_check = QCheckBox()

        self.accounts = QComboBox()
        self.accounts.setMinimumWidth(150)
        accounts = serv_acc_proc.get_all_accounts()
        for acc in accounts:
            self.accounts.addItem(str(acc.acc_name), acc)

        self.cat_check = QCheckBox()

        self.categories = QComboBox()
        self.categories.setMinimumWidth(150)
        categories = serv_cat_proc.get_all_categories()
        for cat in categories:
            self.categories.addItem(str(cat.cat_name), cat)

        filter_layout.addWidget(btn)
        filter_layout.addWidget(QLabel("С:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("По:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(self.acc_check)
        filter_layout.addWidget(self.accounts)
        filter_layout.addWidget(self.cat_check)
        filter_layout.addWidget(self.categories)

        filter_layout.addStretch()

        layout.addLayout(filter_layout)

        self.expenses = BaseTable(["Дата","Счет","Категория","Расход"])

        self.load_expenses_data()
        layout.addWidget(self.expenses)

# --------------------------------------------------------------------------------

    def load_expenses_data(self):
        table_data = serv_view_proc.get_expenses_by_day(
            self.date_from.date().toPython(), 
            self.date_to.date().toPython(),
            self.accounts.currentData() if self.acc_check.isChecked() else None,
            self.categories.currentData() if self.cat_check.isChecked() else None,
        )

        df = pd.DataFrame([
            {
                "Дата": row.rec_date.strftime("%d.%m.%Y"),
                "Счет": row.account.acc_name,
                "Категория": row.category.cat_name,
                "Траты": row.expense
            } 
            for row in table_data
        ])


        
        if self.acc_check.isChecked() == self.cat_check.isChecked():
            columns = ["Счет","Категория"]
        elif self.acc_check.isChecked():
            columns = ["Категория"]
        elif self.cat_check.isChecked():
            columns = ["Счет"]

        pivot_df = df.pivot_table(
            index = "Дата",   
            columns = columns,       
            values = "Траты",            
            aggfunc = "sum",             
            fill_value = 0             
        )

        pivot_df = pivot_df.reset_index()

        numeric_cols = pivot_df.select_dtypes(include="number").columns

        # итого по колонкам (строка внизу)
        total_row = pivot_df[numeric_cols].sum(axis=0)
        total_row["Дата"] = "Итого"
        total_row.update(pivot_df[numeric_cols].sum(axis=0).to_dict())
        
        pivot_df = pd.concat([pivot_df, pd.DataFrame([total_row])], ignore_index=True)

        # pivot_df = pivot_df.reset_index()
        # pivot_df.columns.names = [None, None]

        self.expenses.fill_from_dataframe(pivot_df)  