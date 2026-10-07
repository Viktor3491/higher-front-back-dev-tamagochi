"""Модуль с интерфейсом и реализацией питомца-тамагочи."""
from abc import ABC, abstractmethod

from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики питомца."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца.

        :param food: объект еды.
        """
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
        """Вылечить питомца.

        :param medicine: объект лекарства.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Получить словарь со всеми показателями питомца."""
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

    HUNGER_PER_TICK = 5
    FATIGUE_PER_TICK = 5
    SICK_FATIGUE_EXTRA = 5
    SICK_HP_DAMAGE = 3
    STARVATION_HP_DAMAGE = 2
    HP_TO_GET_SICK = 30

    def __init__(self) -> None:
        """Инициализировать питомца стартовыми показателями."""
        self._hunger = 20
        self._fatigue = 20
        self._hp = 100
        self._energy = 100
        self._sick = False

    def feed(self, food: Food) -> None:
        """Накормить питомца.

        :param food: объект еды.
        """
        self._hunger = self._clamp(self._hunger - food.satiety)

    def play(self) -> None:
        """Поиграть с питомцем: растёт усталость, падает энергия."""
        self._fatigue = self._clamp(self._fatigue + 10)
        self._energy = self._clamp(self._energy - 15)
        self._hunger = self._clamp(self._hunger + 5)

    def rest(self) -> None:
        """Уложить питомца отдыхать.

        Если питомец болен — эффективность отдыха снижена вдвое.
        """
        coefficient = 0.5 if self._sick else 1.0
        self._fatigue = self._clamp(
            self._fatigue - int(20 * coefficient)
        )
        self._energy = self._clamp(
            self._energy + int(20 * coefficient)
        )
        self._hunger = self._clamp(self._hunger + 5)

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца.

        :param medicine: объект лекарства.
        :raises ValueError: если лекарство уже израсходовано.
        """
        if medicine.is_empty():
            raise ValueError('Лекарство закончилось')
        medicine.uses += 1
        self._hp = self._clamp(self._hp + medicine.heal_hp)
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Получить текущее состояние питомца."""
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
        self._hunger = self._clamp(self._hunger + self.HUNGER_PER_TICK)
        self._fatigue = self._clamp(self._fatigue + self.FATIGUE_PER_TICK)

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
        """Ограничить значение диапазоном [0, 100].

        :param value: исходное значение.
        :return: значение в допустимых границах.
        """
        return max(
            SimpleTamagochi.MIN_STAT,
            min(SimpleTamagochi.MAX_STAT, value),
        )
