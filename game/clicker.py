"""Кликер — источник монет в игре."""
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализация кликера."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Доход, полученный за последний клик."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Совершить клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом за клик."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Инициализировать кликер."""
        if min_income < 0 or max_income < min_income:
            raise ValueError('Некорректный диапазон дохода кликера')
        self._min_income = min_income
        self._max_income = max_income
        self._last_income = 0

    @property
    def income_per_click(self) -> int:
        """Доход, полученный за последний клик."""
        return self._last_income

    def click(self) -> None:
        """Совершить клик: разыграть доход в диапазоне."""
        self._last_income = random.randint(
            self._min_income, self._max_income
        )
