_author = "Popescu Ionut-Alexandru"
import socket
import threading
import pickle
import time
from Game import Game, Player

game = Game()
game_id = 1
my_lock = threading.Lock()
threads = []
game_finished = False
winner_thread = ''
winner_username = ''
e = threading.Event()
e.clear()
players = {}

def client_thread(client_socket):
    global my_lock, players,  game_id, e, winner_thread, game_finished, winner_username
    message = f'Welcome to the AirPlane Game! Current generation: #{game_id}\n' \
              f'Please enter your username:\n'
    client_socket.send(message.encode('utf-8'))

    while True:
        username = client_socket.recv(5 * 1024).decode('utf-8')
        if username in players.keys():
            message = f'Another player has this username, please try another one\n'
            client_socket.send(message.encode('utf-8'))
        else:
            message = f'You entered the game please wait...\n'
            client_socket.send(message.encode('utf-8'))
            players[username] = 3
            break

    while not game_finished:
        try:
            response = client_socket.recv(5 * 1024).decode('utf-8')
            y = ord(response[0]) - ord('A')
            x = int(response[1] + response[2]) - 1 if len(response) > 2 else int(response[1]) - 1
            if winner_thread == '':
                if game.game_board[x][y] in ['A', 'B', 'C']:
                    players[username] -= 1
                    if players[username] == 0:
                        my_lock.acquire()
                        game_finished = True
                        winner_thread = threading.get_ident()
                        winner_username = username
                        my_lock.release()
                    else:
                        message = 'H'
                        client_socket.send(message.encode('utf-8'))

                elif game.game_board[x][y] in [1, 2, 3]:
                    message = 'X'
                    client_socket.send(message.encode('utf-8'))
                else:
                    message = 'M'
                    client_socket.send(message.encode('utf-8'))
            else:
                break
        except socket.error as e:
            print(e)
            break

    if game_finished:
        if threading.get_ident() == winner_thread:
            message = 'W'
            client_socket.send(message.encode('utf-8'))
            print(f'The game from #{game_id} generation was won by {username}')
            e.set()
        else:
            message = f'L'
            client_socket.send(message.encode('utf-8'))
            message = f'{winner_username}'
            client_socket.send(message.encode('utf-8'))
            print(f'{username} lost...')

    time.sleep(1)
    print(f'{client_socket.getpeername()} disconnected')
    client_socket.close()


def reset_game():
    global game_id, game, threads, players, e, winner_thread, game_finished
    while True:
        my_lock.acquire()
        game.planes_placer()
        my_lock.release()
        print(f'Game generation #{game_id}')
        print(game)
        e.wait()
        for t in threads:
            t.join()
        my_lock.acquire()
        game_id += 1
        threads = []
        players = {}
        winner_thread = ''
        game_finished = False
        my_lock.release()
        e.clear()


if __name__ == "__main__":
    try:
        HOST = '127.0.0.1'
        PORT = 5555
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(15)
    except socket.error as e:
        print(e)
        exit(-1)

    t = threading.Thread(target=reset_game)
    t.daemon = True
    t.start()
    while True:
        client_socket, address = server_socket.accept()
        t = threading.Thread(target=client_thread, args=(client_socket, ))
        threads.append(t)
        t.start()
