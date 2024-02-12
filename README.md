# The 100 Game: Client-Server Implementation

This is a simple client-server two-player game project, completed as part of the **01418351 Computer Communications and Cloud Computing Principles** course, implemented in Python using socket programming. Players take turns adding numbers from 1 to 10, with the first player to reach 100 declared the winner.

## Prerequisites
- Python 3.x

## Usage

### Running the Server
1. Open a terminal.
2. Navigate to the directory containing `server.py`.
3. Run the following command:
    ```sh
    python server.py
    ```
4. The server will start and wait for players to connect.

### Running the Client
1. Open a terminal.
2. Navigate to the directory containing `client.py`.
3. Run the following command:
    ```sh
    python client.py
    ```
4. The client will connect to the server and start the game.

## The Hundred Game Protocol (THGP)

### Status Code
- 100: Player joined
- 101: Instruction
- 200: OK, Waiting for the player's turn
- 303: Player's turn
- 400: The number is out of range
- 401: Invalid input

### Characteristic
- Turn-based Gameplay: Players take turns performing actions in the game, adding numbers from 1 to 10 to a running total.

- Numeric Input: Players input numbers from 1 to 10 during their turns.

- Goal-oriented: The objective of the game is to reach a total sum of 100 or more. The first player to achieve this goal wins the game.

- Client-Server Architecture: The game follows a client-server model, where one player acts as the server and the other as the client.

- Simple Communication Protocol: THGP defines a straightforward communication protocol between the client and server to facilitate gameplay.

### Transport Layer Service Model
We are using TCP (Transmission Control Protocol)

### Gameplay
1. Players are assigned numbers 1 and 2 upon connection.
2. Player 1 receives the first turn and enters a number from 1 to 10.
3. Player 2 then enters a number from 1 to 10.
4. The game continues until one player reaches 100 or more, declaring them the winner.
5. The losing player receives a message indicating the game is over.

### Additional Notes
- If a player enters an invalid input (not a number or not between 1 and 10), they will be prompted to enter again.
- The server and client will gracefully handle keyboard interrupts, shutting down the game properly.