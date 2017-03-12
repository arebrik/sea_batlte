import socket
from threading import Thread
from queue import Queue
from time import sleep

class NetInterface:
    '''
    For start listen, call start_listen method. This method run separate thread.
    For terminate thread, you must call send_finish method on both: client and server.
    this method sent to other side string "terminate connection" - use this as flag
    for close main thread.
    '''
    HOST = ''
    PORT_l = 50010
    PORT_s = 50010
    ip = ''
    is_localhost = False

    def __init__(self):

        self.q = Queue()
        self.srv_thread = Thread(target=self.listen)


    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT_l))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                if not self.ip:
                    self.ip = addr[0]
                    if self.ip == '127.0.0.1' and self.is_localhost == False: # костыль для localhost
                        self.PORT_s = 50005
                        self.is_localhost = True
                with conn:
                    data = conn.recv(1024).decode('utf-8')
                    self.q.put(data)
                    if data == 'terminate connection':
                        break

    def start_listen(self):
        if self.ip == '127.0.0.1': # костыль для localhost
            self.PORT_l = 50005
            self.is_localhost = True
        self.srv_thread.start()


    def __send(self, data:str):
        data = data.encode('utf-8')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.PORT_s))
            s.sendall(data)

    def test_connect(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.ip, self.PORT_s))
                s.sendall(b'test')
                s.close()
                break
            except ConnectionRefusedError:
                print('Error connection, retry on 5 sec')
                sleep(5)
                continue


    def send_point(self, data:str):
        self.__send(data)

    def send_answer(self, data:str):
        self.__send(data)
        
    def send_user_name(self, username:str):
        self.__send(username)

    def send_finish(self):
        self.__send('terminate connection')
    
    def __get(self):
        answer = self.q.get()
        return answer

    def get_test_connect(self):
        return self.__get()

    def get_opponent_name(self):
        return self.__get()

    def get_answer(self):
        return self.__get()

    def get_point(self):
        return self.__get()



if __name__ == '__main__':
    client = NetInterface('192.168.0.8')
    client.send('sadads')
    print(client.q.get())

