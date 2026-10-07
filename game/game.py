"""Модуль с интерфейсом и реализацией класса игры."""
from abc import ABC, abstractmethod
from copy import copy
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    MedicineIsEmpty,
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
        """Инициализация игры."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Сходить на работу."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self, food: Food | None = None) -> None:
        """Купить еду."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(
        self, medicine: Medicine | None = None
    ) -> None:
        """Купить лекарство."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, food: Food | None = None) -> None:
        """Покормить питомца."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(
        self, medicine: Medicine | None = None
    ) -> None:
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

    @property
    @abstractmethod
    def shop_food(self) -> list[Food]:
        """Ассортимент магазина еды."""
        raise NotImplementedError

    @property
    @abstractmethod
    def shop_medicine(self) -> list[Medicine]:
        """Ассортимент магазина лекарств."""
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
        """Сходить на работу — серия кликов."""
        self._check_alive()
        total = 0
        for _ in range(self.CLICKS_PER_WORK):
            self._clicker.click()
            total += self._clicker.income_per_click
        self._coins += total
        self._tick()
        return total

    def buy_food(self, food: Food | None = None) -> None:
        """Купить еду."""
        self._check_alive()
        affordable = [
            f for f in self._all_food if f.price <= self._coins
        ]
        if not affordable:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки еды'
            )
        if food is None:
            food = affordable[0]
        elif food not in affordable:
            raise NotEnoughMoney(
                'Эта еда недоступна для покупки'
            )
        self._coins -= food.price
        self._food.append(food)
        self._tick()

    def buy_medicine(
        self, medicine: Medicine | None = None
    ) -> None:
        """Купить лекарство."""
        self._check_alive()
        affordable = [
            m for m in self._all_medicine if m.price <= self._coins
        ]
        if not affordable:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )
        if medicine is None:
            medicine = affordable[0]
        elif medicine not in affordable:
            raise NotEnoughMoney(
                'Это лекарство недоступно для покупки'
            )
        # Копия, чтобы изменения `uses` не мутировали магазин.
        medicine_copy = copy(medicine)
        self._coins -= medicine_copy.price
        self._medicine.append(medicine_copy)
        self._tick()

    def feed_tamagochi(self, food: Food | None = None) -> None:
        """Покормить питомца."""
        self._check_alive()
        if not self._food:
            raise NoFoodInBag('В сумке нет еды')
        if food is None:
            food = self._food[0]
        elif food not in self._food:
            raise NoFoodInBag('Такой еды нет в сумке')
        self._food.remove(food)
        self._tamagochi.feed(food)
        self._tick()

    def heal_tamagochi(
        self, medicine: Medicine | None = None
    ) -> None:
        """Вылечить питомца."""
        self._check_alive()
        if not self._medicine:
            raise NoMedicineInBag('В сумке нет лекарств')
        if medicine is None:
            usable = [
                m for m in self._medicine if not m.is_empty()
            ]
            if not usable:
                raise MedicineIsEmpty(
                    'Все лекарства израсходованы'
                )
            medicine = usable[0]
        elif not any(m is medicine for m in self._medicine):
            raise NoMedicineInBag('Такого лекарства нет в сумке')
        if medicine.is_empty():
            raise MedicineIsEmpty('Лекарство закончилось')
        self._tamagochi.heal(medicine)
        self._tick()

    def rest_tamagochi(self) -> None:
        """Уложить питомца отдыхать."""
        self._check_alive()
        self._tamagochi.rest()
        self._tick()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self._check_alive()
        self._tamagochi.play()
        self._tick()

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

    @property
    def shop_food(self) -> list[Food]:
        """Ассортимент магазина еды."""
        return list(self._all_food)

    @property
    def shop_medicine(self) -> list[Medicine]:
        """Ассортимент магазина лекарств."""
        return list(self._all_medicine)

    def _check_alive(self) -> None:
        """Проверить, что питомец жив."""
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone('Тамагочи погиб...')

    def _tick(self) -> None:
        """Один игровой тик: обновление состояния и проверка смерти."""
        self._tamagochi.update()
        self._check_alive()
