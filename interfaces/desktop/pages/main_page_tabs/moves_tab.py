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
from widgets.submit_form import Form

class MovesTab(QWidget):
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
        # btn.clicked.connect(self.load_expenses_data)
        btn.clicked.connect(self.load_moves_data)
        date_layout.addWidget(btn)

        date_layout.addStretch()

        layout.addLayout(date_layout)

        columns = {
            "_id": 0,
            "Дата": 1,
            "Плановая": 2,
            "Счет": 3,
            "Вид": 4,
            "Категория": 5,
            "Сумма": 6,
            "Комментарий": 7 
        }

        self.moves = BaseTable([{i} for i in columns.keys()], True)

        self.submit_moves_btn = QPushButton("Сохранить изменения")
        self.moves_from = Form(self.moves, self.submit_moves_btn)

        layout.addWidget(self.moves_from)



    def load_moves_data(self):
        table_data = serv_mov_proc.get_moves(
            self.date_from.date().toPython(), 
            self.date_to.date().toPython()
        )
        self.moves.setRowCount(0) # очистка

        for m in moves:
            self._add_row(
                id=            m.id,
                plan_rec=      m.plan_rec,
                rec_date=      m.rec_date.strftime("%d.%m.%Y"),
                account=       m.account,   
                move_is_income=m.move_is_income,
                category=      m.category,
                move_sum=      m.move_sum,
                comment=       m.comment
            )
        
    def _add_row(self, id=None, plan_rec=False, rec_date="",
        account=None, move_is_income=True,
        category=None, move_sum=0.0, comment=""
    ):
        
        row = self.moves.rowCount()
        self.moves.insertRow(row)

