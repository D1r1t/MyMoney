from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

import pandas as pd

class BaseTable(QTableWidget):
    def __init__(self, headers: list[str]):
        super().__init__()

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.horizontalHeader().setMinimumSectionSize(150)
        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )



    def fill(self, rows: list[list[str]]):
        self.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(value)))



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