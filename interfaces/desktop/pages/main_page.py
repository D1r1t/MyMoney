from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDateEdit,
    QSplitter 
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

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.addWidget(QLabel("<h2>Главная</h2>"))
        layout.addWidget(QLabel("<h3>Аналитика</h3>"))

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
        btn.clicked.connect(self.load_data)
        date_layout.addWidget(btn)

        date_layout.addStretch()

        layout.addLayout(date_layout)

        self.table = BaseTable(["Дата","Счет","Категория","Расход"])
        
        
        expenses_expander = Expander("Расходы", self.table, False)

        # splitter = QSplitter(Qt.Vertical)

        # bottom_widget = QWidget()

        # splitter.addWidget(expenses_expander)
        # splitter.addWidget(bottom_widget)  

        # splitter = QSplitter(Qt.Vertical)

        # splitter.addWidget(expenses_expander)

        # layout.addWidget(splitter)

        layout.addWidget(expenses_expander)

        layout.addStretch()

    def load_data(self):
        table_data = serv_view_proc.get_expenses_by_day(
            self.date_from.date().toPython(), 
            self.date_to.date().toPython()
        )
        # self.table.setRowCount(len(categories))
        # for i, cat in enumerate(categories):
        #     self.table.setItem(i, 0, QTableWidgetItem(cat.cat_name))

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

        self.table.fill_from_dataframe(pivot_df)    

        
