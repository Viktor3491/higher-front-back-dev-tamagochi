"""Кастомные исключения игры «Тамагочи»."""


class GameError(Exception):
    """Базовое исключение для всех ошибок игры."""


class NotEnoughMoney(GameError):
    """Недостаточно монет для совершения покупки."""


class NoFoodInBag(GameError):
    """В сумке нет еды, чтобы покормить питомца."""


class NoMedicineInBag(GameError):
    """В сумке нет лекарств, чтобы вылечить питомца."""


class MedicineAlreadyUsed(GameError):
    """Лекарство израсходовано полностью."""


class TamagochiIsGone(GameError):
    """Питомец погиб — игра окончена."""
