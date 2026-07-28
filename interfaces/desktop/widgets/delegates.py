# interfaces/desktop/widgets/delegate.py
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QDateEdit, QDoubleSpinBox
from PySide6.QtCore import Qt, QDate

# ================================================================================

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items: list, objects: list = None, parent=None):
        super().__init__(parent)
        self.items   = items    # список строк для отображения
        self.objects = objects  # список объектов (параллельный items)

# --------------------------------------------------------------------------------    

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.items)
        return combo

# --------------------------------------------------------------------------------

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.DisplayRole)
        if value in self.items:
            editor.setCurrentText(value)

# --------------------------------------------------------------------------------

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.ItemDataRole.DisplayRole)
        # прячем объект в UserRole
        if self.objects:
            obj = self.objects[self.items.index(editor.currentText())]
            model.setData(index, obj, Qt.ItemDataRole.UserRole)

# ================================================================================

class DateDelegate(QStyledItemDelegate):
    def __init__(self, format: str = "yyyy-MM-dd", parent = None):
        super().__init__(parent)
        self.format = format

# -------------------------------------------------------------------------------- 

    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)  # выпадающий календарь
        editor.setDisplayFormat(self.format)
        editor.setDate(QDate.currentDate()) 
        return editor

# -------------------------------------------------------------------------------- 

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.DisplayRole)
        if value:
            date = QDate.fromString(value, self.format)
            if date.isValid():
                editor.setDate(date)
        else:
            editor.setDate(QDate.currentDate())

# -------------------------------------------------------------------------------- 

    def setModelData(self, editor, model, index):
        # сохраняем строку для отображения
        model.setData(
            index,
            editor.date().toString(self.format),
            Qt.ItemDataRole.DisplayRole
        )
        # сохраняем объект date в UserRole
        model.setData(
            index,
            editor.date().toPython(),
            Qt.ItemDataRole.UserRole
        )

# ================================================================================

class NumberDelegate(QStyledItemDelegate):
    def __init__(
        self, 
        decimals: int = 2, 
        min_val: float = 0,
        max_val: float = 999_999_999,
        parent = None
    ):
        super().__init__(parent)
        self.decimals = decimals
        self.min_val  = min_val
        self.max_val  = max_val

# -------------------------------------------------------------------------------- 

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        editor.setDecimals(self.decimals)
        editor.setMinimum(self.min_val)
        editor.setMaximum(self.max_val)
        editor.setGroupSeparatorShown(True)
        return editor

# -------------------------------------------------------------------------------- 

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.UserRole)
        if value:
            editor.setValue(float(value))

# -------------------------------------------------------------------------------- 

    def setModelData(self, editor, model, index):
        value = editor.value()
        
        model.setData(
            index,
            f"{value:,.2f}".replace(",", " "),
            Qt.ItemDataRole.DisplayRole
        )
        # числовое значение в UserRole
        model.setData(
            index,
            value,
            Qt.ItemDataRole.UserRole
        )       