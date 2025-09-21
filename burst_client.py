import socket
import time
import random

class BurstClient:
    def __init__(self, host='localhost', port=5555):
        self.HOST = host
        self.PORT = port
        self.REQUESTS = [
            b'CPU_INTENSIVE',
            b'IO_INTENSIVE',
            b'FAST',
            b'NORMAL',
        ]

    def burst_client(self, num_bursts=5, burst_size=10, burst_interval=3):
        for burst in range(num_bursts):
            print(f"\n--- Iniciando rajada {burst+1} ---")
            for i in range(burst_size):
                req_type = random.choice(self.REQUESTS)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.HOST, self.PORT))
                        s.sendall(req_type + b' | burst=' + str(burst).encode() + b' | id=' + str(i).encode())
                        data = s.recv(1024)
                        print(f"[Rajada {burst+1} - {i}] Enviado: {req_type.decode()} | Recebido: {data.decode().strip()}")
                except Exception as e:
                    print(f"[Rajada {burst+1} - {i}] Erro ao conectar/enviar: {e}")
            print(f"--- Fim da rajada {burst+1}, aguardando {burst_interval}s ---\n")
            time.sleep(burst_interval)

if __name__ == "__main__":
    client = BurstClient()
    client.burst_client()