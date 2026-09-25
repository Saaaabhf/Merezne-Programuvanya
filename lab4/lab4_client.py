import socket

# Адреса та порт сервера
HOST = '127.0.0.1'
PORT = 65432

# Створюємо TCP-сокет для клієнта
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Інтерфейс англійською
    print(f"Connecting to server {HOST}:{PORT}...")
    
    s.connect((HOST, PORT))
    
    # Повідомлення теж англійською, щоб у сервера в консолі був англійський текст
    message = "Hello, server! This is a test message from the client for Lab 4."
    print(f"Sending: {message}")
    
    s.sendall(message.encode('utf-8'))
    
    data = s.recv(1024)
    
print(f"Received response back: {data.decode('utf-8')}")
