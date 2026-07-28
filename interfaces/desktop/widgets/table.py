from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from .delegates import ComboBoxDelegate, DateDelegate, NumberDelegate

import pandas as pd

# ================================================================================

class BaseTable(QTableWidget):
    def __init__(self, headers: list[str], editable = False):
        super().__init__()

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.horizontalHeader().setMinimumSectionSize(150)
        
        if editable:
            self.setEditTriggers(
                QTableWidget.EditTrigger.DoubleClicked |  # двойной клик
                QTableWidget.EditTrigger.AnyKeyPressed |  # нажатие любой клавиши
                QTableWidget.EditTrigger.SelectedClicked  # клик по уже выделенной ячейке
            ) 
            # Разрешаем копирование/вставку
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        else:
            self.setEditTriggers(
                QTableWidget.EditTrigger.NoEditTriggers
            )


        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

# --------------------------------------------------------------------------------

    def fill(self, rows: list[list[str]]):
        self.setRowCount(0) # cleanup
        self.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(value)))

# --------------------------------------------------------------------------------

    def fill_from_dataframe(self, df: pd.DataFrame):
        if isinstance(df.columns, pd.MultiIndex):
            # headers = [" / ".join(str(c) for c in col).strip() for col in df.columns]
            headers = []
            for col in df.columns:
                # убираем пустые части — для колонки "Дата" будет просто "Дата"
                parts = [str(c) for c in col if c != ""]
                headers.append(" /\n ".join(parts))
        else:
            headers = [str(col) for col in df.columns]

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setRowCount(len(df))

        for i, (_, row) in enumerate(df.iterrows()):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value) if pd.notna(value) else "")
                self.setItem(i, j, item)

# ================================================================================

class FullEditableTable(QTableWidget):
    def __init__(self, data: dict):
        super().__init__()
        self.data = data

        self.headers = list(self.data.keys())

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.horizontalHeader().setMinimumSectionSize(150)
        
        self.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked |      
            QTableWidget.EditTrigger.AnyKeyPressed |      
            QTableWidget.EditTrigger.SelectedClicked   
        ) 
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        for col, col_data in self.data.items():
            if "hidden" in col_data:
                if col_data["hidden"] == True:
                    self.setColumnHidden(col_data["id"], True)
            if "names" in col_data and "values" in col_data:
                self.setItemDelegateForColumn(
                    col_data["id"], 
                    ComboBoxDelegate(
                        items = col_data["names"],
                        objects = col_data["values"],
                        parent = self
                    )
                )
            if "type" in col_data:
                if col_data["type"] == "date":
                    self.setItemDelegateForColumn(
                        col_data["id"],
                        DateDelegate(parent = self)
                    )
                elif col_data["type"] == "number":
                    self.setItemDelegateForColumn(
                        col_data["id"],
                        NumberDelegate(parent = self)
                    )

# --------------------------------------------------------------------------------

    def fill(self, data: list):
        self.setRowCount(0) # cleanup
        self.setRowCount(len(data))

        struct = list(self.data.values())

        for i, row in enumerate(data):
            for j, col_struct in enumerate(struct):
                self.setItem(i, j, self._create_item(row[j], col_struct))

# --------------------------------------------------------------------------------

    def get_row_data(self, row: int) -> dict:
        struct = list(self.data.items())
        result = {}
        
        for col_name, col_struct in struct:
            item = self.item(row, col_struct["id"])
            if item is None:
                result[col_name] = None
                continue
            
            if "obj" in col_struct:
                result[col_name] = item.data(Qt.ItemDataRole.UserRole)
            elif "names" in col_struct:
                text = item.text()
                try:
                    idx = col_struct["names"].index(text)
                    result[col_name] = col_struct["values"][idx]
                except:
                    result[col_name] = text
            elif "type" in col_struct:
                if col_struct["type"] == "number":
                    result[col_name] = item.data(Qt.ItemDataRole.UserRole)
                elif col_struct["type"]  == "date":
                    result[col_name] = item.text()  
            else:
                result[col_name] = item.text()
        
        return result   

# --------------------------------------------------------------------------------

    def get_all_data(self) -> list[dict]:
        return [self.get_row_data(i) for i in range(self.rowCount())]

# --------------------------------------------------------------------------------

    def add_row_from_data(self, data: list):
        row = self.rowCount()
        self.insertRow(row)

        struct = list(self.data.values())

        for j, col_struct in enumerate(struct):
            self.setItem(row, j, self._create_item(data[j], col_struct))

# --------------------------------------------------------------------------------

    def add_empty_row(self):
        row = self.rowCount()
        self.insertRow(row)

# --------------------------------------------------------------------------------
    def _create_item(self, value, col_struct: dict):
        if "obj" in col_struct:
            obj_name = getattr(value, col_struct["obj_name"])
            item = QTableWidgetItem(str(obj_name))
            item.setData(Qt.ItemDataRole.UserRole, value)
            return item
        elif "names" in col_struct:
            try:
                idx = col_struct["values"].index(value)
                display = col_struct["names"][idx]
            except:
                display = str(value)
   
            return QTableWidgetItem(display)
        elif "type" in col_struct:
            if col_struct["type"] == "number":
                item = QTableWidgetItem(f"{float(value):,.2f}".replace(",", " "))
                item.setData(Qt.ItemDataRole.UserRole, value)
                return item
            elif col_struct["type"]  == "date":
                return QTableWidgetItem(str(value) if value is not None else "") 
        else:
            return QTableWidgetItem(str(value) if value is not None else "")

# --------------------------------------------------------------------------------

    def delete_selected_rows(self):
        rows = sorted(
            set(
                idx.row() for idx in self.selectedIndexes()
            ),
            reverse = True
        )

        for row in rows:
            self.removeRow(row)

# --------------------------------------------------------------------------------

    def get_current_ids(self, index_name: str) -> list[int]:
        idxs = []
        for row in self.get_all_data():
            idxs.append(row[index_name]) 

        return idxs   

