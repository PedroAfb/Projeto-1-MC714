import socket
import time
import random

HOST = 'localhost'
PORT = 5555

REQUESTS = [
    b'CPU_INTENSIVE',
    b'IO_INTENSIVE',
    b'FAST',
    b'NORMAL',
]

def burst_client(num_bursts=5, burst_size=10, burst_interval=3):
    for burst in range(num_bursts):
        print(f"\n--- Iniciando rajada {burst+1} ---")
        for i in range(burst_size):
            req_type = random.choice(REQUESTS)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(req_type + b' | burst=' + str(burst).encode() + b' | id=' + str(i).encode())
                    data = s.recv(1024)
                    print(f"[Rajada {burst+1} - {i}] Enviado: {req_type.decode()} | Recebido: {data.decode().strip()}")
            except Exception as e:
                print(f"[Rajada {burst+1} - {i}] Erro ao conectar/enviar: {e}")
        print(f"--- Fim da rajada {burst+1}, aguardando {burst_interval}s ---\n")
        time.sleep(burst_interval)

if __name__ == "__main__":
    burst_client()