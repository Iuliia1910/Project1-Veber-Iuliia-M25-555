import math
from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    if room['exits']:
        print("Выходы:", ", ".join(room['exits'].keys()))

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
        
        
def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)
        
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        chance = pseudo_random(game_state['steps_taken'], 10)
        if chance < 3:
            print("Вы попали в ловушку и погибли!")
            game_state['game_over'] = True
        else:
            print("Вы чудом уцелели.")


def random_event(game_state):
    # Событие с вероятностью 1/10
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'], 3)

    room = ROOMS[game_state['current_room']]

    if event_type == 0:
        print("Вы находите монетку на полу.")
        room['items'].append('coin')
    elif event_type == 1:
        print("Вы слышите странный шорох вокруг.")
        if 'sword' in game_state['player_inventory']:
            print("Ваш меч отпугнул нечто, что могло напасть.")
    elif event_type == 2:
        if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
            print("Внимание! В комнате опасно!")
            trigger_trap(game_state)

def solve_puzzle(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answers = room['puzzle']  # answers — список допустимых ответов
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    if user_answer in [a.lower() for a in answers]:
        print("Верно! Вы решили загадку.")
        room['puzzle'] = None
        # Можно добавить награду
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == 'trap_room':
            trigger_trap(game_state)

def attempt_open_treasure(game_state):

    room_name = game_state['current_room']
    room = ROOMS[room_name]

    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return

    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        ans = get_input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
        if ans == "да":
            user_code = get_input("Введите код: ").strip()
            if room['puzzle'] and user_code == str(room['puzzle'][1]):
                print("Вы угадали код! Сундук открыт!")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
    

