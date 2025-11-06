#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS, COMMANDS
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help, get_input, pseudo_random, trigger_trap, random_event
from labyrinth_game.player_actions import move_player, take_item, use_item, show_inventory

def process_command(game_state, command):
    parts = command.strip().lower().split()
    if not parts:
        return

    cmd = parts[0]
    arg = " ".join(parts[1:]) if len(parts) > 1 else None

    # Односложные направления можно использовать напрямую
    directions = ['north', 'south', 'east', 'west']
    if cmd in directions:
        move_player(game_state, cmd)
        return

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите, что вы хотите взять.")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет для использования.")
        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление.")
        case "solve":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("Выход из игры. До встречи!")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")

def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)

if __name__ == "__main__":
    main()

