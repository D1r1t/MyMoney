from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QDateEdit,
    QSplitter 
)

from PySide6.QtCore import (
    QDate, Qt 
)

import core.service.account_processing        as serv_acc_proc 
import core.service.categories_processing     as serv_cat_proc
import core.service.moves_processing          as serv_mov_proc

from core.exceptions import CategoryAlreadyExistsError, AppError
from widgets.table import FullEditableTable
from widgets.form import AddDelSubmitForm

# ================================================================================

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
        btn.clicked.connect(self.load_moves_data)
        date_layout.addWidget(btn)

        date_layout.addStretch()

        layout.addLayout(date_layout)

        accounts = serv_acc_proc.get_all_accounts()
        categories = serv_cat_proc.get_all_categories()

        columns = {
            "_id": {"id":0, "hidden": True},
            "Дата": {"id":1, "type": "date"},
            "Плановая": {"id":2, "names":["План","Факт"],"values":[True, False]},
            "Счет": {"id":3,"names":[i.acc_name for i in accounts],"values":[i for i in accounts],"obj":"account", "obj_name":"acc_name"},
            "Вид": {"id":4, "names":["Приход","Расход"],"values":[True, False]},
            "Категория": {"id":5,"names":[i.cat_name for i in categories],"values":[i for i in categories],"obj":"category", "obj_name":"cat_name"},
            "Сумма": {"id":6, "type": "number"},
            "Комментарий": {"id":7} 
        }

        self.moves = FullEditableTable(columns)

        self.indexes = []

        submit_moves_btn = QPushButton("Сохранить изменения")
        add_move_btn     = QPushButton("Добавить строку")
        del_move_btn     = QPushButton("Удалить выделенные")

        submit_moves_btn.clicked.connect(self.submit_changes)
        add_move_btn.    clicked.connect(self.add_row)
        del_move_btn.    clicked.connect(self.delete_rows)

        moves_from = AddDelSubmitForm(self.moves, submit_moves_btn, add_move_btn, del_move_btn)
        empty_widget = QWidget()

        spli = QSplitter(Qt.Vertical)
        
        spli.addWidget(moves_from)
        spli.addWidget(empty_widget)

        layout.addWidget(spli)
        self.load_moves_data()

# --------------------------------------------------------------------------------

    def load_moves_data(self):
        table_data = serv_mov_proc.get_moves(
            self.date_from.date().toPython(), 
            self.date_to.date().toPython()
        )
        
        list_table_data = [
           [
                m.id,
                m.rec_date,
                m.plan_rec,
                m.account,   
                m.move_is_income,
                m.category,   
                m.move_sum,
                m.comment
            ]
            for m in table_data 
        ]

        self.moves.setRowCount(0) # очистка

        self.moves.fill(list_table_data)

        self.indexes = self.moves.get_current_ids("_id")

# --------------------------------------------------------------------------------
        
    def add_row(self):
        self.moves.add_empty_row()
        
# --------------------------------------------------------------------------------

    def delete_rows(self):
        self.moves.delete_selected_rows()

# --------------------------------------------------------------------------------

    def submit_changes(self):
        cur_date    = self.moves.get_all_data()
        cur_indexes = self.moves.get_current_ids("_id")
        
        for row in cur_date:
            if row["_id"] is None:
                serv_mov_proc.create_new_move(
                    plan_rec       = row["Плановая"], 
                    rec_date       = row["Дата"], 
                    account        = row["Счет"], 
                    move_is_income = row["Вид"], 
                    category       = row["Категория"], 
                    move_sum       = row["Сумма"], 
                    comment        = row["Комментарий"]
                )
            else:
                serv_mov_proc.update_move(
                    id             = int(row["_id"]),
                    plan_rec       = row["Плановая"], 
                    rec_date       = row["Дата"], 
                    account        = row["Счет"], 
                    move_is_income = row["Вид"], 
                    category       = row["Категория"], 
                    move_sum       = row["Сумма"], 
                    comment        = row["Комментарий"]
                )

        original_set_id = set(self.indexes)
        new_id_set      = set(cur_indexes)

        deleted_id_set = original_set_id - new_id_set
        for deleted_id in deleted_id_set:
            serv_mov_proc.delete_move(deleted_id)

        

