"""Модуль с интерфейсом и реализацией питомца-тамагочи."""
from abc import ABC, abstractmethod

from .exceptions import MedicineIsEmpty
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики питомца."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Уложить питомца отдыхать."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Словарь со всеми показателями питомца."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверить, болен ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Обновить состояние питомца (один игровой тик)."""
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простой питомец с механикой голода, усталости, HP и энергии."""

    MAX_STAT = 100
    MIN_STAT = 0

    START_HUNGER = 20
    START_FATIGUE = 20
    START_HP = 100
    START_ENERGY = 100

    HUNGER_PER_TICK = 5
    FATIGUE_PER_TICK = 5
    SICK_FATIGUE_EXTRA = 5
    SICK_HP_DAMAGE = 3
    STARVATION_HP_DAMAGE = 2
    HP_TO_GET_SICK = 30

    PLAY_FATIGUE_INCREASE = 10
    PLAY_ENERGY_REDUCE = 15
    PLAY_HUNGER_INCREASE = 5

    REST_FATIGUE_REDUCE = 20
    REST_ENERGY_RESTORE = 20
    REST_HUNGER_INCREASE = 5
    SICK_REST_COEFFICIENT = 0.5

    def __init__(self) -> None:
        """Инициализировать питомца стартовыми показателями."""
        self._hunger = self.START_HUNGER
        self._fatigue = self.START_FATIGUE
        self._hp = self.START_HP
        self._energy = self.START_ENERGY
        self._sick = False

    def feed(self, food: Food) -> None:
        """Накормить питомца.

        :param food: объект еды.
        """
        self._hunger = self._clamp(self._hunger - food.satiety)

    def play(self) -> None:
        """Поиграть с питомцем: растёт усталость, падает энергия."""
        self._fatigue = self._clamp(
            self._fatigue + self.PLAY_FATIGUE_INCREASE
        )
        self._energy = self._clamp(
            self._energy - self.PLAY_ENERGY_REDUCE
        )
        self._hunger = self._clamp(
            self._hunger + self.PLAY_HUNGER_INCREASE
        )

    def rest(self) -> None:
        """Уложить питомца отдыхать."""
        coefficient = (
            self.SICK_REST_COEFFICIENT if self._sick else 1.0
        )
        self._fatigue = self._clamp(
            self._fatigue - int(self.REST_FATIGUE_REDUCE * coefficient)
        )
        self._energy = self._clamp(
            self._energy + int(self.REST_ENERGY_RESTORE * coefficient)
        )
        self._hunger = self._clamp(
            self._hunger + self.REST_HUNGER_INCREASE
        )

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца."""
        if medicine.is_empty():
            raise MedicineIsEmpty('Лекарство закончилось')
        medicine.uses += 1
        self._hp = self._clamp(self._hp + medicine.heal_hp)
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Текущее состояние питомца."""
        return {
            'hunger': self._hunger,
            'fatigue': self._fatigue,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверить, болен ли питомец."""
        return self._sick

    def update(self) -> None:
        """Обновить состояние питомца за один игровой тик."""
        self._hunger = self._clamp(
            self._hunger + self.HUNGER_PER_TICK
        )
        self._fatigue = self._clamp(
            self._fatigue + self.FATIGUE_PER_TICK
        )

        if self._sick:
            self._hp -= self.SICK_HP_DAMAGE
            self._fatigue = self._clamp(
                self._fatigue + self.SICK_FATIGUE_EXTRA
            )

        if self._hunger >= self.MAX_STAT:
            self._hp -= self.STARVATION_HP_DAMAGE
        if self._fatigue >= self.MAX_STAT:
            self._hp -= self.STARVATION_HP_DAMAGE

        if self._hp < self.HP_TO_GET_SICK:
            self._sick = True

    @staticmethod
    def _clamp(value: int) -> int:
        """Ограничить значение диапазоном [0, 100]."""
        return max(
            SimpleTamagochi.MIN_STAT,
            min(SimpleTamagochi.MAX_STAT, value),
        )
