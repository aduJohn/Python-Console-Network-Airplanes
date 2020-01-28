_author = "Popescu Ionut-Alexandru"
import socket
import time
from termcolor import cprint
from Game import Player
from colorama import init
import os
if __name__ == '__main__':
    init()
    try:
        client_socket = socket.create_connection(('127.0.0.1', 5555))
    except socket.error as e:
        print(e)
        exit(-1)

    finished = False
    message_from_server = client_socket.recv(5 * 1024).decode('utf-8')
    print(message_from_server)
    while True:
        response = input('>')
        client_socket.send(response.encode('utf-8'))
        message_from_server = client_socket.recv(5 * 1024).decode(('utf-8'))
        print(message_from_server)
        if message_from_server == 'You entered the game please wait...\n':
            break

    your_player = Player(response)
    while not finished:
        try:
            print(your_player)
            cprint('Please enter your next move: (Example: A5)\n', 'white', attrs=['bold'])
            move = input('>')
            y = move[0] if len(move) > 1 else ':('
            x = move[1]+move[2] if len(move) > 2 else move[1] if len(move) == 2 else ':('
            if y not in ['A','B','C','D','E','F','G','H','I','J'] or x not in ['1','2','3','4','5','6','7','8','9','10']:
                cprint('Please enter a valid option!\n', 'white', attrs=['bold'])
            else:
                y = ord(move[0]) - ord('A')
                x = int(move[1] + move[2]) - 1 if len(move) > 2 else int(move[1]) - 1
                if your_player.players_view[x][y] != 0:
                    os.system('cls')
                    cprint("Please enter an option that you didn't enter before!\n", 'white', attrs=['bold'])
                else:
                    client_socket.send(move.encode('utf-8'))
                    message_from_server = client_socket.recv(5 * 1024).decode('utf-8')
                    if message_from_server in ['W', 'L']:
                        finished = True
                        if message_from_server == 'L':
                            winner = client_socket.recv(5 * 1024).decode('utf-8')
                    elif message_from_server == 'H':
                        os.system('cls')
                        cprint(f'PLANE DOWN AT {move}\n', 'white', 'on_yellow', attrs=['bold'])
                        your_player.plane_hit(x, y, message_from_server)
                    elif message_from_server == 'X':
                        os.system('cls')
                        cprint(f'PLANE HIT AT {move}\n', 'white', 'on_red', attrs=['bold'])
                        your_player.plane_hit(x, y, message_from_server)
                    else:
                        os.system('cls')
                        cprint(f'PLANE MISSED AT {move}\n', 'white', 'on_cyan', attrs=['bold'])
                        your_player.plane_hit(x, y, message_from_server)
        except socket.error as e:
            print(e)
            exit(-2)

    client_socket.close()
    if message_from_server == 'W':
        cprint('You won this game generation, please reconnect for a new contest!\n', 'white', attrs=['bold'])
    else:
        cprint(f'You lost this game generation, the winner was {winner}!\n', 'white', attrs=['bold'])

    input('Press any key to continue...')