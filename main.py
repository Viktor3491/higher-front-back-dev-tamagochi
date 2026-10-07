"""Точка входа в игру «Тамагочи-кликер»."""
import os
from typing import Any

from game.clicker import SimpleRandomClicker
from game.exceptions import (
    GameError,
    NotEnoughMoney,
    TamagochiIsGone,
)
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi

MENU = (
    '1. Пойти на работу',
    '2. Купить еду',
    '3. Купить лекарство',
    '4. Покормить',
    '5. Вылечить',
    '6. Играть',
    '7. Отдых',
    '0. Выход',
)

INFO_TEMPLATE = (
    'Сумка с едой: {food}\n'
    'Сумка с лекарствами: {medicine}\n'
    '\nСтатус: голод {hunger}, усталость {fatigue}, '
    'здоровье {hp}, энергия {energy}, монет {coins}'
)

SICK_WARNING = (
    '======= Тамагочи болеет =======\n'
    '==== Отдых действует менее эффективно ===='
)


def clear_screen() -> None:
    """Очистить консоль (кроссплатформенно)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_item(options: list[Any]) -> Any | None:
    """Показать список и дать игроку выбрать элемент."""
    if not options:
        return None
    for index, item in enumerate(options, start=1):
        print(f'{index}. {item}')
    try:
        number = int(input('Введите номер: '))
    except ValueError:
        return None
    if 1 <= number <= len(options):
        return options[number - 1]
    return None


def render_info(game: SimpleGame) -> str:
    """Сформировать текстовое состояние игры."""
    status = game.get_status()
    status['food'] = game.food
    status['medicine'] = game.medicine
    return INFO_TEMPLATE.format(**status)


def main() -> None:
    """Запустить основной игровой цикл."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]
    all_medicine = [
        Medicine(
            name='Ибупрофен',
            price=30,
            heal_hp=20,
            number_of_uses=2,
        ),
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print('Добро пожаловать в Тамагочи-кликер!')
    output = ''

    while True:
        print(output)
        print(render_info(game))

        if game.tamagochi.is_sick():
            print(SICK_WARNING)

        print(MENU)

        action = input('Выберите действие: ')

        try:
            match action:
                case '1':
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case '2':
                    food = choose_item(game.shop_food)
                    if food is None:
                        output = 'Покупка отменена'
                    else:
                        game.buy_food(food)
                        output = f'Куплено: {food.name}'
                case '3':
                    medicine = choose_item(game.shop_medicine)
                    if medicine is None:
                        output = 'Покупка отменена'
                    else:
                        game.buy_medicine(medicine)
                        output = f'Куплено: {medicine.name}'
                case '4':
                    food = choose_item(game.food)
                    if food is None:
                        output = 'Кормление отменено'
                    else:
                        game.feed_tamagochi(food)
                        output = f'Питомец съел {food.name}'
                case '5':
                    medicine = choose_item(game.medicine)
                    if medicine is None:
                        output = 'Лечение отменено'
                    else:
                        game.heal_tamagochi(medicine)
                        output = f'Питомец вылечен {medicine.name}'
                case '6':
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case '7':
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case '0':
                    print('Игра завершена.')
                    return
                case _:
                    output = 'Неверная команда'
        except TamagochiIsGone as error:
            clear_screen()
            print(f'\n{error}')
            print('Игра окончена.')
            return
        except NotEnoughMoney as error:
            output = str(error)
        except GameError as error:
            output = f'Ошибка: {error}'

        clear_screen()


if __name__ == '__main__':
    main()
