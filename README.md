# PyScrabble
A Scrabble® game implemented in Python.

## Gameplay
See the video below for example gameplay.

https://user-images.githubusercontent.com/25882507/148694573-8bdf2428-f0bd-4be2-a0b7-2e538bdef3fd.mov

## Features
- A fully terminal-based user interface
- Uses websockets to enable playing with friends over a network.
- Includes a move generation algorithm that powers move validation and computer opponents.

## Built with
- [SocketIO](https://socket.io) - for client-server communication
- [Redis](https://redis.io) - for storing game state and lobby data
- [ncurses](https://en.wikipedia.org/wiki/Ncurses) - for creating the terminal UI

## How to Play
### Create a lobby
1. Create a new game lobby by running `python run_network_game.py your_name`
2. Share the 4 digit room ID with other players (who have network access to your host machine)
3. Join an existing game lobby by running `python run_network_game.py your_name room_id`
4. Start the game, closing the lobby, once all players have joined

### Enter moves
1. Enter the direction, location, and word to play when prompted
2. Moves will be rejected per the official game rules
    - If the word does not exist in the game's `dictionary.txt`
    - If the word does not connect to an existing tile
    - If the player's rack is missing required tiles to play a word
3. Moves are scored according to tile values and board multiplier squares

## Installation
Use Python 3.7 or 3.8

Create a Python virtual environment, using `venv` or any alternative
```sh
~ python -m venv pyscrabble
~ cd pyscrabble
~ source bin/activate
```

Next clone this repo and install the dependencies
```sh
(pyscrabble) ~ git clone https://github.com/danesolberg/PyScrabble.git
(pyscrabble) ~ cd PyScrabble
(pyscrabble) ~ pip install -r requirements.txt
```

## Development Setup
PyScrabble uses Redis to manage game state and websocket connections, so a local Redis server must be started

### Install Redis with Homebrew
```sh
~ brew install redis
~ brew services start redis
```

### Run unit tests
```sh
(pyscrabble) ~ pytest
```

## Run games
Launch a local game via `python run_local_game.py` or a networked game via `python run_network_game.py your_name`
