from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QHeaderView,
    QPushButton, QLabel, QMessageBox, QDateEdit,
    QSplitter 
)

from PySide6.QtCore import QDate

import core.service.views_processing as serv_view_proc

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
        btn.clicked.connect(self.load_expenses_data)
        # btn.clicked.connect(self.load_moves_data)
        date_layout.addWidget(btn)

        date_layout.addStretch()

        layout.addLayout(date_layout)

        self.expenses = BaseTable(["Дата","Счет","Категория","Расход"])
        # expenses_expander = Expander("Расходы", self.expenses)
        self.load_expenses_data()
        layout.addWidget(self.expenses)

# --------------------------------------------------------------------------------

    def load_expenses_data(self):
        table_data = serv_view_proc.get_expenses_by_day(
            self.date_from.date().toPython(), 
            self.date_to.date().toPython()
        )

        df = pd.DataFrame([
            {
                "Дата": row.rec_date.strftime("%d.%m.%Y"),
                "Счет": row.acc_name,
                "Категория": row.cat_name,
                "Траты": row.expense
            } 
            for row in table_data
        ])

        pivot_df = df.pivot_table(
            index = "Дата",   
            columns = ["Счет","Категория"],       
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