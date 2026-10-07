"""Точка входа в игру «Тамагочи-кликер»."""
import os

from game.clicker import SimpleRandomClicker
from game.exceptions import (
    GameError,
    NotEnoughMoney,
    TamagochiIsGone,
)
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def clear_screen() -> None:
    """Очистить консоль (кроссплатформенно)."""
    os.system('cls' if os.name == 'nt' else 'clear')


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
        print(f'Сумка с едой: {game.food}')
        print(f'Сумка с лекарствами: {game.medicine}')

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, "
            f"усталость {status['fatigue']}, "
            f"здоровье {status['hp']}, "
            f"энергия {status['energy']}, "
            f"монет {status['coins']}\n"
        )

        if game.tamagochi.is_sick():
            print('======= Тамагочи болеет =======')
            print('==== Отдых действует менее эффективно ====')

        print('1. Пойти на работу')
        print('2. Купить еду')
        print('3. Купить лекарство')
        print('4. Покормить')
        print('5. Вылечить')
        print('6. Играть')
        print('7. Отдых')
        print('0. Выход')

        action = input('Выберите действие: ')

        try:
            match action:
                case '1':
                    income = game.work()
                    game.tamagochi.update()
                    output = f'Вы заработали {income} монет'
                case '2':
                    game.buy_food()
                    output = 'Еда куплена'
                case '3':
                    game.buy_medicine()
                    output = 'Лекарство куплено'
                case '4':
                    game.feed_tamagochi()
                    output = 'Питомец накормлен'
                case '5':
                    game.heal_tamagochi()
                    output = 'Питомец вылечен'
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
