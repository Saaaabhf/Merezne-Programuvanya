import socket

# Налаштування сервера
HOST = '127.0.0.1'  # Локальна адреса (localhost)
PORT = 65432        # Порт для підключення

# Створюємо TCP-сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    # Інтерфейс англійською
    print(f"Server is running and listening on {HOST}:{PORT}...")
    
    # Нескінченний цикл (модифікація Medium)
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"\nClient connected from: {addr}")
            
            while True:
                data = conn.recv(1024)
                
                if not data:
                    print(f"Client {addr} disconnected.")
                    break
                    
                print(f"Received message: {data.decode('utf-8')}")
                conn.sendall(data)
