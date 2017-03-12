import pickle
import os


class Field:
    def __init__(self):
        self.coord = []

    def add(self, x, y):
        self.coord.append({'x': x, 'y': y})


class Data:
    DBNAME = 'db.pickle'

    def __init__(self):
        self.my = Field()
        self.my_boats = Field()
        self.enemy = Field()
        self.turn = 0
        self.players = {'my_name': '', 'enemy_name': ''}

        self.data = {
            'my': self.my,
            'enemy': self.enemy,
            'my_boats': self.my_boats,
            'turn': self.turn,
            'players': self.players
        }

    def save(self):
        with open(self.DBNAME, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        with open(self.DBNAME, 'rb') as f:
            self.data = pickle.load(f)
            self.my = self.data['my']
            self.my_boats = self.data['my_boats']
            self.enemy = self.data['enemy']
            self.turn = self.data['turn']
            self.players = self.data['players']

    def clean(self):
        os.remove(self.DBNAME)

    def set_my_name(self, name):
        self.players['my_name'] = name
        self.save()

    def up_turn(self):
        self.turn += 1
        self.save()
