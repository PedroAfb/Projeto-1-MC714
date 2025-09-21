import sys
import socket
import select
import random
import time
from itertools import cycle

SERVER_POOL = [('localhost', 8888), ('localhost', 8889), ("localhost", 8890)]
ITER = cycle(SERVER_POOL)

def round_robin(iter):
    return next(iter)

class LoadBalancer(object):
    flow_table = dict()
    sockets = list()
    server_stats = {srv: 0 for srv in SERVER_POOL}  # Contador de requisições por servidor
    response_times = []  # Lista de tempos de resposta
    conn_start_times = dict()
    total_requests = 0

    def __init__(self, ip, port, algorithm='random'):
        self.ip = ip
        self.port = port
        self.algorithm = algorithm
        self.cs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs_socket.bind((self.ip, self.port))
        print(f"init client-side socket: {self.cs_socket.getsockname()}")
        self.cs_socket.listen(10)
        self.sockets.append(self.cs_socket)

    def start(self):
        start_time = time.time()
        try:
            while True:
                read_list, _, _ = select.select(self.sockets, [], [])
                for sock in read_list:
                    if sock == self.cs_socket:
                        print(f"{'='*40}flow start{'='*39}")
                        self.on_accept()
                        break
                    else:
                        try:
                            data = sock.recv(4096)
                            if data:
                                self.on_recv(sock, data)
                            else:
                                self.on_close(sock)
                                break
                        except Exception as e:
                            print(f"Erro: {e}")
                            self.on_close(sock)
                            break
                # Exibe métricas a cada 10 requisições
                if self.total_requests > 0 and self.total_requests % 10 == 0:
                    self.print_metrics(start_time)
        except KeyboardInterrupt:
            print(f"Ctrl C - Stopping load_balancer")
            self.print_metrics(start_time)
            sys.exit(1)

    def on_accept(self):
        client_socket, client_addr = self.cs_socket.accept()
        print(f"client connected: {client_addr} <==> {self.cs_socket.getsockname()}")
        server_ip, server_port = self.select_server(SERVER_POOL, self.algorithm)
        ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ss_socket.connect((server_ip, server_port))
            print(f"init server-side socket: {ss_socket.getsockname()}")
            print(f"server connected: {ss_socket.getsockname()} <==> {(socket.gethostbyname(server_ip), server_port)}")
            self.server_stats[(server_ip, server_port)] += 1  # Conta requisição para o servidor
        except Exception as e:
            print(f"Can't establish connection with remote server, err: {e}")
            print(f"Closing connection with client socket {client_addr}")
            client_socket.close()
            return
        self.sockets.append(client_socket)
        self.sockets.append(ss_socket)
        self.flow_table[client_socket] = ss_socket
        self.flow_table[ss_socket] = client_socket
        self.conn_start_times[client_socket] = time.time()  # Marca início da requisição

    def on_recv(self, sock, data):
        print(f"recving packets: {sock.getpeername()} ==> {sock.getsockname()}, data: {[data]}")
        remote_socket = self.flow_table[sock]
        remote_socket.send(data)
        print(f"sending packets: {remote_socket.getsockname()} ==> {remote_socket.getpeername()}, data: {[data]}")

    def on_close(self, sock):
        print(f"client {sock.getpeername()} has disconnected")
        print(f"{'='*41}flow end{'='*40}")
        ss_socket = self.flow_table[sock]
        self.sockets.remove(sock)
        self.sockets.remove(ss_socket)
        sock.close()
        ss_socket.close()
        # Métrica global: tempo de resposta por requisição
        start = self.conn_start_times.pop(sock, None)
        if start:
            resp_time = time.time() - start
            self.response_times.append(resp_time)
        self.total_requests += 1
        self.server_stats[(ss_socket.getpeername())] -= 1  # Decrementa contador do servidor
        del self.flow_table[sock]
        del self.flow_table[ss_socket]

    def select_server(self, server_list, algorithm):
        if algorithm == 'random':
            return random.choice(server_list)
        elif algorithm == 'round robin':
            return round_robin(ITER)
        elif algorithm == 'shortest queue':
            return min(self.server_stats.items(), key=lambda x: x[1])[0]
        else:
            raise Exception(f"unknown algorithm: {algorithm}")

    def print_metrics(self, start_time):
        elapsed = time.time() - start_time
        throughput = self.total_requests / elapsed if elapsed > 0 else 0
        avg_response = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        print(f"\n=== MÉTRICAS ===")
        print(f"Total de requisições: {self.total_requests}")
        print(f"Vazão (throughput): {throughput:.2f} req/s")
        print(f"Tempo médio de resposta: {avg_response:.4f} s")
        print("Distribuição de carga por servidor:")
        for srv, count in self.server_stats.items():
            print(f"  {srv}: {count} requisições")
        print("================\n")

if __name__ == '__main__':
    # Permite escolher política via argumento
    alg = 'random'
    if len(sys.argv) > 1:
        alg = sys.argv[1]
    LoadBalancer('localhost', 5555, "round robin").start()