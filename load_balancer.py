import sys
import socket
import select
import random
from itertools import cycle

# dumb netcat server, short tcp connection
# $ ~  while true ; do nc -l 8888 < server1.html; done
# $ ~  while true ; do nc -l 9999 < server2.html; done
SERVER_POOL = [('localhost', 8888), ('localhost', 8889), ("localhost", 8890)]

# dumb python socket echo server, long tcp connection
# $ ~  while  python server.py
# SERVER_POOL = [('localhost', 6666)]

ITER = cycle(SERVER_POOL)
def round_robin(iter):
    # round_robin([A, B, C, D]) --> A B C D A B C D A B C D ...
    return next(iter)

"""Detalhes da implementação:
– O balanceador de carga deve ter uma opção de configuração para alternar entre as três políticas.
– A implementação dever ser capaz de mostrar como a carga foi distribuída para cada política
utilizada, através de um log ou apresentando as informações das alocações na saída padrão.
– Registre o desempenho do balanceador de carga em diferentes condições de tráfego e nas três
diferentes políticas através de, pelo menos, duas métricas principais: vazão do sistema (th-
roughput), tempo médio de resposta (average response time). Outras métricas poderão ser
utilizadas, por exemplo, utilização do sistema."""

class LoadBalancer(object):
    """ Socket implementation of a load balancer.
    Flow Diagram:
    +---------------+      +-----------------------------------------+      +---------------+
    | client socket | <==> | client-side socket | server-side socket | <==> | server socket |
    |   <client>    |      |          < load balancer >              |      |    <server>   |
    +---------------+      +-----------------------------------------+      +---------------+
    Attributes:
        ip (str): virtual server's ip; client-side socket's ip
        port (int): virtual server's port; client-side socket's port
        algorithm (str): algorithm used to select a server
        flow_table (dict): mapping of client socket obj <==> server-side socket obj
        sockets (list): current connected and open socket obj
    """

    flow_table = dict()
    sockets = list()

    def __init__(self, ip, port, algorithm='random'):
        self.ip = ip
        self.port = port
        self.algorithm = algorithm

        # init a client-side socket
        self.cs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire.
        self.cs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs_socket.bind((self.ip, self.port))
        print(f"init client-side socket: {self.cs_socket.getsockname()}")
        self.cs_socket.listen(10) # max connections
        self.sockets.append(self.cs_socket)

    def start(self):
        while True:
            read_list, write_list, exception_list = select.select(self.sockets, [], [])
            for sock in read_list:
                # new connection
                if sock == self.cs_socket:
                    print(f"{'='*40}flow start{'='*39}")
                    self.on_accept()
                    break
                # incoming message from a client socket
                else:
                    try:
                        # In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        data = sock.recv(4096) # buffer size: 2^n
                        if data:
                            self.on_recv(sock, data)
                        else:
                            self.on_close(sock)
                            break
                    except:
                        sock._closed(sock)
                        break

    def on_accept(self):
        client_socket, client_addr = self.cs_socket.accept()
        print(f"client connected: {client_addr} <==> {self.cs_socket.getsockname()}")

        # select a server that forwards packets to
        server_ip, server_port = self.select_server(SERVER_POOL, self.algorithm)

        # init a server-side socket
        ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ss_socket.connect((server_ip, server_port))
            print(f"init server-side socket: {ss_socket.getsockname()}")
            print(f"server connected: {ss_socket.getsockname()} <==> {(socket.gethostbyname(server_ip), server_port)}")
        except:
            print(f"Can't establish connection with remote server, err: {sys.exc_info()[0]}")
            print(f"Closing connection with client socket {client_addr}")
            client_socket.close()
            return

        self.sockets.append(client_socket)
        self.sockets.append(ss_socket)

        self.flow_table[client_socket] = ss_socket
        self.flow_table[ss_socket] = client_socket

    def on_recv(self, sock, data):
        print(f"recving packets: {sock.getpeername()} ==> {sock.getsockname()}, data: {[data]}")
        # data can be modified before forwarding to server
        # lots of add-on features can be added here
        remote_socket = self.flow_table[sock]
        remote_socket.send(data)
        print(f"sending packets: {remote_socket.getsockname()} ==> {remote_socket.getpeername()}, data: {[data]}")

    def on_close(self, sock):
        print(f"client {sock.getpeername()} has disconnected")
        print(f"{'='*41}flow end{'='*40}")

        ss_socket = self.flow_table[sock]

        self.sockets.remove(sock)
        self.sockets.remove(ss_socket)

        sock.close()  # close connection with client
        ss_socket.close()  # close connection with server

        del self.flow_table[sock]
        del self.flow_table[ss_socket]

    def select_server(self, server_list, algorithm):
        if algorithm == 'random':
            return random.choice(server_list)
        elif algorithm == 'round robin':
            return round_robin(ITER)
        else:
            raise Exception(f"unknown algorithm: {algorithm}")


if __name__ == '__main__':
    try:
        LoadBalancer('localhost', 5555, 'random').start()
    except KeyboardInterrupt:
        print(f"Ctrl C - Stopping load_balancer")
        sys.exit(1)