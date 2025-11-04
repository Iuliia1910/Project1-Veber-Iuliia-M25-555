install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

project:
	poetry run python -m labyrinth_game.main

package-install:
	poetry install
