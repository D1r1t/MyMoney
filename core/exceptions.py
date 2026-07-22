from .models.currency import Currency

class AppError(Exception):
    pass

# ===ACCOUNTS_ERRORS===

class AccountError(AppError):
    def __init__(self, mess: str = "Ошибка чтения/записи счета"):
        super().__init__(mess)

class AccountAlreadyExistsError(AccountError):
    def __init__(self, name: str):
        super().__init__(f"Счёт '{name}' уже существует")

class AccountWasntFound(AccountError):
    def __init__(self, name: str):
        super().__init__(f"Счёт '{name}' не был найден")

# ===CURRENCIES_ERRORS===

class CurrencyError(AppError):
    def __init__(self, mess: str = "Ошибка чтения/записи валюты"):
        super().__init__(mess)

class CurrencyAlreadyExistsError(CurrencyError):
    def __init__(self, main_currency: Currency):
        super().__init__(f"Валюта '{main_currency.cur_name}' уже существует")

class CurrencyMainAlreadyExistsError(CurrencyError):
    def __init__(self, main_currency: Currency):
        super().__init__(f"Валюта '{main_currency.cur_name}' уже является основной")

# ===CATEGORIES_ERRORS===

class CategoryError(AppError):
    def __init__(self, mess: str = "Ошибка чтения/записи категории"):
        super().__init__(mess)

class CategoryAlreadyExistsError(CategoryError):
    def __init__(self, name: str):
        super().__init__(f"Категория '{name}' уже существует")

class CategoryWasntFound(AccountError):
    def __init__(self, name: str):
        super().__init__(f"Категория '{name}' не была найдена")

# ===EXCHANGE_RATES_ERRORS===

class ExchangeRatesError(AppError):
    def __init__(self, mess: str = "Ошибка чтения/записи курсов"):
        super().__init__(mess)

# ===MOVES_ERRORS===

class MovesError(AppError):
    def __init__(self, mess: str = "Ошибка чтения/записи транзакции"):
        super().__init__(mess)

class MoveDoesntExists(MovesError):
    def __init__(self, id: int):
        super().__init__(f"Движения с id {id} не было найдено")
