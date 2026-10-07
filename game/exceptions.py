"""Кастомные исключения игры «Тамагочи»."""


class GameError(Exception):
    """Базовое исключение для всех ошибок игры."""


class NotEnoughMoney(GameError):
    """Недостаточно монет для покупки."""


class NoFoodInBag(GameError):
    """В сумке нет такой еды."""


class NoMedicineInBag(GameError):
    """В сумке нет такого лекарства."""


class MedicineIsEmpty(GameError):
    """Лекарство израсходовано полностью."""


class TamagochiIsGone(GameError):
    """Питомец погиб — игра окончена."""
