from socket import *
import time

# Define server port
SERVER_PORT = 5555

# Define status codes and phrases
STATUS_PLAYER_JOINED = 100
STATUS_INSTRUCTION = 101
STATUS_OK = 200
STATUS_GAME_OVER = 201
STATUS_YOUR_TURN = 303
STATUS_BAD_NUMBER = 400
STATUS_INVALID = 401

class GameManager:
    def __init__(self, player1_socket, player2_socket):
        self.player1 = player1_socket
        self.player2 = player2_socket
        self.current_number = 0

    def start_game(self):
        instructions = "Welcome! Each player takes turns adding numbers from 1 to 10. First to reach 100 wins."
        self.notify_player(STATUS_INSTRUCTION, instructions, self.player1)
        self.notify_player(STATUS_INSTRUCTION, instructions, self.player2)
        time.sleep(0.1)

        while True:
            self.player_turn(self.player1, self.player2)
            if self.current_number >= 100:
                self.game_over(self.player1, self.player2, "Congratulations! You win!", "Game over. You lose.")
                break

            self.player_turn(self.player2, self.player1)
            if self.current_number >= 100:
                self.game_over(self.player2, self.player1, "Congratulations! You win!", "Game over. You lose.")
                break

    def notify_player(self, status, message, player):
        player.send(f"{status} {message}".encode())

    def player_turn(self, current_player, other_player):
        self.notify_player(STATUS_YOUR_TURN, f"Your turn. Current number is {self.current_number}.", current_player)
        self.notify_player(STATUS_OK, f"Current number is {self.current_number}. Waiting for your turn...", other_player)

        while True:
            try:
                player_input = int(current_player.recv(1024).decode())
                if 1 <= player_input <= 10:
                    self.current_number += player_input
                    return
                else:
                    self.notify_player(STATUS_BAD_NUMBER, "Please enter a number between 1 and 10.", current_player)
            except ValueError:
                self.notify_player(STATUS_INVALID, "Invalid input. Please enter a number.", current_player)

    def game_over(self, winner, loser, win_message, lose_message):
        self.notify_player(STATUS_GAME_OVER, win_message, winner)
        self.notify_player(STATUS_GAME_OVER, lose_message, loser)

# Create a socket object
server_socket = socket(AF_INET, SOCK_STREAM)

try:
    # Bind the socket to the address
    server_socket.bind(("", SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(2)                     # Max players
    print("Waiting for players to connect...")

    # Accept the connection from player 1
    player1_socket, player1_address = server_socket.accept()
    print("Player 1 connected from:", player1_address)

    # Notify player 1 that they are player 1
    player1_socket.send(f"{STATUS_PLAYER_JOINED} You are Player 1. Please wait for another player to join...".encode())

    # Accept the connection from player 2
    player2_socket, player2_address = server_socket.accept()
    print("Player 2 connected from:", player2_address)

    # Notify player 2 that they are player 2
    player2_socket.send(f"{STATUS_PLAYER_JOINED} You are Player 2. Game starting...".encode())

    # Notify player 1 that player 2 has joined
    player1_socket.send(f"{STATUS_PLAYER_JOINED} Player 2 has joined. Game starting...".encode())

    game_manager = GameManager(player1_socket, player2_socket)
    print("Game is starting...")
    time.sleep(0.1)
    game_manager.start_game()

finally:
    print("\nServer shutting down...")
    # Close the sockets if they exist
    try:
        player1_socket.close()
        player2_socket.close()
    except NameError:
        pass
    server_socket.close()
