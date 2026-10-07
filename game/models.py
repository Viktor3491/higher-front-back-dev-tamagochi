"""Модели игровых объектов — еда и лекарства."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель еды."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Красивое строковое представление еды."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц'
        )


@dataclass
class Medicine:
    """Модель лекарства."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверить, закончилось лекарство или нет."""
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Красивое строковое представление лекарства."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, '
            f'использований: '
            f'{self.number_of_uses - self.uses}/{self.number_of_uses}'
        )
