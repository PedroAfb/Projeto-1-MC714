import socket

HOST = 'localhost'
PORT = 8890

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