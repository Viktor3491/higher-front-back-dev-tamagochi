"""Модуль с интерфейсом и реализацией класса игры."""
import random
from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    MedicineAlreadyUsed,
    NoFoodInBag,
    NoMedicineInBag,
    NotEnoughMoney,
    TamagochiIsGone,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализация игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Сходить на работу.

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Купить еду."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Купить лекарство."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Покормить питомца."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Вылечить питомца."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Уложить питомца отдыхать."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Получить полный статус игры."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Сумка с едой."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Сумка с лекарствами."""
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация игры «Тамагочи-кликер»."""

    CLICKS_PER_WORK = 5

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализация игры."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = 0

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Питомец (для клиентского кода)."""
        return self._tamagochi

    @property
    def clicker(self) -> AbstractClicker:
        """Кликер."""
        return self._clicker

    def work(self) -> int:
        """Сходить на работу — серия кликов.

        :return: суммарно заработанные монеты
        :raises TamagochiIsGone: если питомец мёртв
        """
        self._check_alive()
        total = 0
        for _ in range(self.CLICKS_PER_WORK):
            self._clicker.click()
            total += self._clicker.income_per_click
        self._coins += total
        return total

    def buy_food(self) -> None:
        """Купить случайную доступную еду.

        :raises NotEnoughMoney: если не хватает монет
        """
        self._check_alive()
        affordable = [
            f for f in self._all_food if f.price <= self._coins
        ]
        if not affordable:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки еды'
            )
        food = random.choice(affordable)
        self._coins -= food.price
        self._food.append(food)

    def buy_medicine(self) -> None:
        """Купить случайное доступное лекарство.

        :raises NotEnoughMoney: если не хватает монет
        """
        self._check_alive()
        affordable = [
            m for m in self._all_medicine if m.price <= self._coins
        ]
        if not affordable:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )
        medicine = random.choice(affordable)
        self._coins -= medicine.price
        self._medicine.append(medicine)

    def feed_tamagochi(self) -> None:
        """Покормить питомца первой едой из сумки.

        :raises NoFoodInBag: если в сумке нет еды
        """
        self._check_alive()
        if not self._food:
            raise NoFoodInBag('В сумке нет еды')
        food = self._food.pop(0)
        self._tamagochi.feed(food)

    def heal_tamagochi(self) -> None:
        """Вылечить питомца доступным лекарством.

        :raises NoMedicineInBag: если в сумке нет лекарств
        :raises MedicineAlreadyUsed: если все лекарства израсходованы
        """
        self._check_alive()
        usable = [m for m in self._medicine if not m.is_empty()]
        if not usable:
            if not self._medicine:
                raise NoMedicineInBag('В сумке нет лекарств')
            raise MedicineAlreadyUsed('Все лекарства израсходованы')
        self._tamagochi.heal(usable[0])

    def rest_tamagochi(self) -> None:
        """Уложить питомца отдыхать."""
        self._check_alive()
        self._tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self._check_alive()
        self._tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Получить полный статус (питомец + монеты)."""
        status: dict[str, Any] = dict(self._tamagochi.status)
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """Сумка с едой."""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с лекарствами."""
        return self._medicine

    def _check_alive(self) -> None:
        """Проверить, что питомец жив.

        :raises TamagochiIsGone: если питомец мёртв
        """
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone('Тамагочи погиб...')
