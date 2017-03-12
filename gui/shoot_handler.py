from random import randrange


class Field:
    def __init__(self):
        pass

    def pole(self, data):
        print('  А Б В Г Д Е Ж З И К')

        for a in range(10):
            stroka = str(a + 1) + '|'
            for n in range(10):
                stroka += str(data[a][n]) + '|'
            print(stroka)

if __name__ == '__main__':
    field = Field()
    # field.pole()
    list = [[1, 0, 0, 0, 0, 0, 0, 'x', 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, '.', 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
    field.pole(list)