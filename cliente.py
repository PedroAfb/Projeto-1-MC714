import socket

"""Simule o tráfego de entrada gerando uma sequência de solicitações.
– Varie as requisições – algumas consumirão mais tempo de CPU, outras menos, outras mais
tempo de I/O.
– Os pedidos devem chegar em intervalos aleatórios, imitando cenários do mundo real.
– Certifique-se de que o balanceador de carga pode lidar com uma variedade de padrões de trá-
fego, incluindo explosões de pedidos e fluxos constantes."""

HOST = 'localhost'
PORT = 5555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, load balancer!\n')
    data = s.recv(1024)
    print(f"Recebido: {data.decode()}")