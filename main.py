#!/usr/bin/env python3
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обработка команд игрока."""
    parts = command.strip().split()
    if not parts:
        return

    action = parts[0].lower()
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    match action:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            move_player(game_state, arg)
        case "take":
            if arg == "treasure_chest":
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            else:
                take_item(game_state, arg)
        case "use":
            use_item(game_state, arg)
        case "solve":
            # если игрок в treasure_room — пробуем открыть сундук
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            print("Вы покидаете лабиринт. До встречи!")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Попробуйте: look, go, take, use, solve, inventory, quit.")


def main():
    """Основной цикл игры."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()

