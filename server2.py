import socket
import time

""" Simule 3 servidores que possam lidar com as requisições. Defina uma fila para armazenar as re-
quisições e um tempo para o processamento de cada servidor. A capacidade de processamento
e os recursos dos servidores podem ser iguais.
– Deve ser adicionado um ligeiro atraso para simular o tempo real de processamento. Esse atraso
pode ser variável de acordo com a requisição, isto é, se a requisição faz uso intensivo de CPU o
atraso é um, se faz mais I/O o atraso pode ser maior.
– O estado do servidor (ocupado, inativo) e o comprimento da fila devem ser monitorados."""

HOST = 'localhost'
PORT = 8890

# Mapeia tipo de requisição para tempo de processamento (em segundos)
PROCESSING_TIMES = {
    'CPU_INTENSIVE': 1.5,
    'IO_INTENSIVE': 2.0,
    'FAST': 0.2,
    'NORMAL': 0.7,
}

def get_processing_time(request):
    for key in PROCESSING_TIMES:
        if key in request:
            return PROCESSING_TIMES[key]
    return 0.5  # padrão

def main():
    queue = []
    busy = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escutando em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexão de {addr}")
                data = conn.recv(1024)
                if data:
                    req_str = data.decode()
                    queue.append(req_str)
                    print(f"Fila atual: {len(queue)} requisições")
                    busy = True
                    print(f"Servidor ocupado: {busy}")
                    proc_time = get_processing_time(req_str)
                    print(f"Processando '{req_str.strip()}' por {proc_time:.2f}s")
                    time.sleep(proc_time)
                    conn.sendall(f'Processado ({req_str.strip()}) na porta {PORT} em {proc_time:.2f}s\n'.encode())
                    queue.pop(0)
                    busy = False
                    print(f"Servidor ocupado: {busy}")

if __name__ == "__main__":
    main()