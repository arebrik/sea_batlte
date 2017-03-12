# coding: utf-8
'''
---- Sea battle ----

Main program file.

'''
from api.NetAPI import NetInterface
from data.main import Data
from gui.shoot_handler import Field
from sys import exit

data = Data()
field = Field()
api = NetInterface()

h_key = {
    'А':0,
    'Б':1,
    'В':2,
    'Г':3,
    'Д':4,
    'Е':5,
    'Ж':6,
    'З':7,
    'И':8,
    'К':9,
}
    

def main():
    input('''

Hello! I am the game - @Sea battle@
    by python curs 2016-2017. IFMO.



Click Enter to start.

    ''')    

    data.data['my_boats'] = create_my_pole()
    data.data['enemy'] = create_enemy_pole()

    api_type = None
    while not api_type:
        answer = input('''

Print your choice. You are:

    1 - [c]lient
    2 - [s]erver

    ''')
        if answer in ('1', 'c'):
            start_client()
            api_type = 'client'
        elif answer in ('2', 's'):
            start_server()
            api_type = 'server'


def start_client():

    server= None
    while True:
        server = input('Print server address (like 192.168.0.1): ')
        srv_list = server.split('.')
        if len(srv_list)!= 4 or not all( s.isnumeric() for s in srv_list ):
            print('Oooops... Wrong server: {}'.format(server))
            continue
        api.ip = server
        api.test_connect()
        api.start_listen()
        print('OK. You are connecting to: {}...'.format(server))
        break

    data.players['my_name'] = make_my_name()
    api.send_user_name(data.players['my_name'])
    data.players['enemy_name'] = api.get_opponent_name()

    while True:
        print('Ход номер ', data.turn + 1)
        make_my_step()
        get_his_step()
        if is_end():
            print('Ты победил!!!')
            exit()
        data.up_turn()
        print_turn_result()


def start_server():
    data.players['my_name'] = make_my_name()

    print('Ожидаем подключение клиента...')
    api.start_listen()
    api.get_test_connect()
    data.players['enemy_name'] = api.get_opponent_name()
    print('Подключился игрок с именем {}'.format(data.players['enemy_name']))
    api.send_user_name(data.players['my_name'])

    while True:
        print('Ход номер ', data.turn + 1)
        get_his_step()
        if is_end():
            print('Ты проиграл!!!')
            exit()
        make_my_step()
        data.up_turn()

        print_turn_result()


def is_end():
    for string in data.data['my_boats']:
        if '1' in string:
            return False
    else:
        api.send_finish()
        return True


def make_my_step():
    while True:
        choice = input('Куда бьем(например а2)? \n')
        if check_coor_format(choice):
            api.send_point(choice)
            answer = api.get_answer()
            print('Результат: {}'.format(answer))
            remake_enemy_pole(choice, answer)
            break
        else:
            continue


def get_his_step():
    print('Ожидаем хода оппонента[{}]'.format(data.players['enemy_name']))
    opponent_choice = api.get_point()
    print('Оппонент походил на {}'.format(opponent_choice))
    if opponent_choice == 'terminate connection':
        print('Ты победил!!!')
        api.send_finish()
        exit()
    api.send_answer(check_point(opponent_choice))


def print_turn_result():
    print('Ваши[{}] корабли:'.format(data.players['my_name']))
    field.pole(data.data['my_boats'])
    print('Чужие[{}] корабли:'.format(data.players['enemy_name']))
    field.pole(data.data['enemy'])

def make_my_name():
    name = ''
    while len(name) == 0:
        name = input('Введите ваше имя: ')
    data.set_my_name(name)
    return name


def create_enemy_pole():
    return [['U' for x in range(10)] for y in range(10)]


def remake_enemy_pole(c, answer):
    coordinate = check_coor_format(c)
    if answer == 'попал':
        data.data['enemy'][coordinate[1]][coordinate[0]] = 'x'
    elif answer == 'мимо':
        data.data['enemy'][coordinate[1]][coordinate[0]] = '.'

def create_my_pole():
    ships = create_my_ships() #unkoment when work normaly!
    pole = [['0' if [x, y] not in ships else '1'
              for x in range(10)
              ]
             for y in range(10)
             ]
    return pole


def create_my_ships():
    print('Вам нужно расстивать 2 корабля')
    ships = []
    for i in range(2):
        if i % 3 == 0:
            ships += put_ship(3)
        else:
            ships += put_ship(2)
    return ships


def put_ship(layer):
    i = 0
    ship = []
    print('Собираем корабль с длинной {}'.format(layer))
    while i < layer:
        c = input('Введите {} координату: \n'.format(i))
        coordinate = check_coor_format(c)
        if coordinate:
            ship.append(coordinate)
        else:
            continue
        i += 1
    return ship


def check_coor_format(coordinate):
    try:
        coordinate = [coordinate[0].upper(), coordinate[1: len(coordinate)]]
        if (int(coordinate[1]) not in [i for i in range(1, 11)]
            or coordinate[0].upper() not in h_key):
            print('Не верный формат координаты {}!'.format(coordinate))
        else:
            return [h_key[coordinate[0]], int(coordinate[1]) - 1]
    except (TypeError, IndexError, ValueError):
        print('Не верный формат координаты {}!'.format(coordinate))


def check_point(point):
    c = check_coor_format(point)
    coordinate = data.data['my_boats'][c[1]][c[0]]
    if coordinate == '1':
        data.data['my_boats'][c[1]][c[0]] = 'x'
        return 'попал'
    elif coordinate == 'x':
        return 'уже подбил!'
    else:
        return 'мимо'

if __name__=='__main__':
    main()
