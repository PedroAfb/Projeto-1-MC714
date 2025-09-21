import socket
import time
import random

"""Simule o tráfego de entrada gerando uma sequência de solicitações.
– Varie as requisições – algumas consumirão mais tempo de CPU, outras menos, outras mais
tempo de I/O.
– Os pedidos devem chegar em intervalos aleatórios, imitando cenários do mundo real.
– Certifique-se de que o balanceador de carga pode lidar com uma variedade de padrões de trá-
fego, incluindo explosões de pedidos e fluxos constantes."""

HOST = 'localhost'
PORT = 5555

# Tipos de requisição simulando diferentes cargas
REQUESTS = [
    b'CPU_INTENSIVE',   # simula processamento pesado
    b'IO_INTENSIVE',    # simula operação de I/O
    b'FAST',            # simula requisição rápida
    b'NORMAL',          # padrão
]

def simulate_client(num_requests=20):
    for i in range(num_requests):
        req_type = random.choice(REQUESTS)
        # Intervalo aleatório entre 0.1s e 1.5s
        interval = random.uniform(0.1, 1.5)
        time.sleep(interval)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(req_type + b' | id=' + str(i).encode())
                data = s.recv(1024)
                print(f"[{i}] Enviado: {req_type.decode()} | Recebido: {data.decode().strip()} | Intervalo: {interval:.2f}s")
        except Exception as e:
            print(f"[{i}] Erro ao conectar/enviar: {e}")

if __name__ == "__main__":
    simulate_client()