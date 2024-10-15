import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 10021        # Server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "Hello from the client!"
    s.sendall(message.encode('utf-8'))
    data = s.recv(1024)

print('Received from server:', data.decode('utf-8'))