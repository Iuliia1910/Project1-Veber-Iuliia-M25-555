# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def move_player(game_state, direction):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if direction not in room_data['exits']:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = room_data['exits'][direction]

    # Проверка для входа в treasure_room
    if (
    next_room == 'treasure_room' and 'rusty_key' 
    not in game_state['player_inventory']
    ):
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return
    elif next_room == 'treasure_room':
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    describe_current_room(game_state)

    # Случайные события после перемещения
    random_event(game_state)

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Вы зажгли факел, стало светлее. Теперь лучше видно.")
    elif item_name == 'sword':
        print("Вы берёте меч в руки. Вы чувствуете себя уверенно.")
    elif item_name == 'bronze_box':
        print("Вы открываете бронзовую шкатулку...")
        if 'rusty_key' not in game_state['player_inventory']:
            print("Внутри вы находите ржавый ключ!")
            game_state['player_inventory'].append('rusty_key')
        else:
            print("Пусто, ключ уже у вас есть.")
    else:
        print("Вы не знаете, как использовать этот предмет.")

def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:")
        for item in inventory:
            print(f" - {item}")
    else:
        print("Ваш инвентарь пуст.")

