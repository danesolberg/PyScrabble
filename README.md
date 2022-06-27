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
1. Create a new game lobby by running `python run_network_game.py <your_name>`
2. Share the 4 digit room ID with other players (who have network access to your host machine)
3. Join an existing game lobby by running `python run_network_game.py <your_name> room_id`
4. Start the game, closing the lobby, once all players have joined

### Enter moves
1. Enter the direction, location, and word to play when prompted
2. Moves will be rejected per the official game rules
    - If the word does not exist in the game's `dictionary.txt`
    - If the word does not connect to an existing tile
    - If the player's rack is missing required tiles to play a word
3. Moves are scored according to tile values and board multiplier squares

## Run with Docker
Run the Docker application, which contains a Redis container and game server container, which are started automatically.
```sh
~ docker-compose up
[+] Running 2/0
 ⠿ Container pyscrabble-redis-1  Created    0.0s
 ⠿ Container pyscrabble-wss-1    Created    0.0s
Attaching to pyscrabble-redis-1, pyscrabble-wss-1
```

Launch the network game inside the game server.
```sh
~ docker exec -it pyscrabble-wss-1 python run_network_game.py <your_name>
```

## Development Setup
Use Python 3.7 or 3.8

Create a Python virtual environment, using `venv` or any alternative.
```sh
~ python -m venv pyscrabble
~ cd pyscrabble
~ source bin/activate
```

Next clone this repo and install the dependencies.
```sh
(pyscrabble) ~ git clone https://github.com/danesolberg/PyScrabble.git
(pyscrabble) ~ cd PyScrabble
(pyscrabble) ~ pip install -r requirements.txt
```

Install Redis (if required)
```sh
~ brew install redis
~ brew services start redis
```

Start the game server
```sh
(pyscrabble) ~ python start_server.py
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 734-552-454
(pid) wsgi starting up on http://0.0.0.0:5000
```

### Run unit tests
```sh
(pyscrabble) ~ pytest
```

## Run games
### Start local game
####
In development environment
```sh
(pyscrabble) ~ python run_local_game.py
```
####
In Docker container
```sh
~ docker exec -it pyscrabble-wss-1 python run_local_game.py
```

### Network game
To launch a network game (currently defaulting to localhost), first create a new game room.
```sh
(pyscrabble) ~ python run_network_game.py <your_name>
```
or
```sh
~ docker exec -it pyscrabble-wss-1 python run_network_game.py <your_name>
```

This will open a new game room and present a room code to share with up to three other players.

![Game room code](https://user-images.githubusercontent.com/25882507/174459547-0aa6c003-4dd5-4df3-9763-e61d30f86424.png)

Players can join this game by appending the room code as an argument to `run_network_game.py`.  In the image above, the room code is 4b82.
```sh
(pyscrabble) ~ python run_network_game.py <your_name> <room_code>
```
or
```sh
~ docker exec -it python run_network_game.py <your_name> <room_code>
```


