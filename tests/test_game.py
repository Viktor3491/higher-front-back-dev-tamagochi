"""Тесты для проекта «Тамагочи-кликер»."""
import pytest

from game.clicker import SimpleRandomClicker
from game.exceptions import (
    NotEnoughMoney,
    TamagochiIsGone,
)
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


@pytest.fixture
def tamagochi() -> SimpleTamagochi:
    """Свежий питомец для каждого теста."""
    return SimpleTamagochi()


@pytest.fixture
def clicker() -> SimpleRandomClicker:
    """Кликер с диапазоном 10–20 монет."""
    return SimpleRandomClicker(10, 20)


@pytest.fixture
def game(
    tamagochi: SimpleTamagochi,
    clicker: SimpleRandomClicker,
) -> SimpleGame:
    """Игра со стандартным набором еды и лекарств."""
    return SimpleGame(
        tamagochi,
        clicker,
        all_food=[
            Food(name='Бургер', satiety=20, price=40),
            Food(name='Яблоко', satiety=10, price=15),
        ],
        all_medicine=[
            Medicine(
                name='Ибупрофен',
                price=30,
                heal_hp=20,
                number_of_uses=2,
            ),
        ],
    )


# ----------------------------- Модели ------------------------------------


def test_food_attributes() -> None:
    food = Food(name='Яблоко', satiety=10, price=15)
    assert food.name == 'Яблоко'
    assert food.satiety == 10
    assert food.price == 15


def test_medicine_is_empty() -> None:
    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=2,
    )
    assert not medicine.is_empty()
    medicine.uses = 2
    assert medicine.is_empty()


# ----------------------------- Кликер ------------------------------------


def test_clicker_income_in_range() -> None:
    clicker = SimpleRandomClicker(10, 20)
    for _ in range(50):
        clicker.click()
        assert 10 <= clicker.income_per_click <= 20


def test_clicker_bad_range() -> None:
    with pytest.raises(ValueError):
        SimpleRandomClicker(20, 10)


# ---------------------------- Тамагочи -----------------------------------


def test_status_keys(tamagochi: SimpleTamagochi) -> None:
    keys = set(tamagochi.status)
    assert {'hunger', 'fatigue', 'hp', 'energy'} <= keys


def test_tamagochi_alive_at_start(
    tamagochi: SimpleTamagochi,
) -> None:
    assert tamagochi.is_alive()
    assert not tamagochi.is_sick()


def test_feeding_reduces_hunger(
    tamagochi: SimpleTamagochi,
) -> None:
    before = tamagochi.status['hunger']
    tamagochi.feed(Food(name='Яблоко', satiety=10, price=15))
    assert tamagochi.status['hunger'] < before


def test_update_increases_hunger(
    tamagochi: SimpleTamagochi,
) -> None:
    before = tamagochi.status['hunger']
    tamagochi.update()
    assert tamagochi.status['hunger'] > before


# ------------------------------ Игра -------------------------------------


def test_work_returns_int(game: SimpleGame) -> None:
    income = game.work()
    assert isinstance(income, int)
    assert income > 0


def test_buy_food_without_money(game: SimpleGame) -> None:
    with pytest.raises(NotEnoughMoney):
        game.buy_food()


def test_buy_food_and_feed(game: SimpleGame) -> None:
    for _ in range(5):
        game.work()
    game.buy_food()
    assert len(game.food) == 1
    game.feed_tamagochi()
    assert len(game.food) == 0


def test_heal_tamagochi(game: SimpleGame) -> None:
    for _ in range(5):
        game.work()
    game.buy_medicine()
    game.heal_tamagochi()
    assert not game.tamagochi.is_sick()


def test_death_raises(game: SimpleGame) -> None:
    tamagochi = game.tamagochi
    while tamagochi.is_alive():
        tamagochi.update()
    with pytest.raises(TamagochiIsGone):
        game.work()


def test_get_status_contains_coins(game: SimpleGame) -> None:
    status = game.get_status()
    assert 'coins' in status
    assert status['coins'] == 0
