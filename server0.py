import socket

""" Simule 3 servidores que possam lidar com as requisições. Defina uma fila para armazenar as re-
quisições e um tempo para o processamento de cada servidor. A capacidade de processamento
e os recursos dos servidores podem ser iguais.
– Deve ser adicionado um ligeiro atraso para simular o tempo real de processamento. Esse atraso
pode ser variável de acordo com a requisição, isto é, se a requisição faz uso intensivo de CPU o
atraso é um, se faz mais I/O o atraso pode ser maior.
– O estado do servidor (ocupado, inativo) e o comprimento da fila devem ser monitorados."""

HOST = 'localhost'
PORT = 8888

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
                conn.sendall(f'Hello from Python backend na porta {PORT}!\n'.encode())