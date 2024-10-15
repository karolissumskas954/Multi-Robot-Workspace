import socket
import threading
import time

runing = True
clients = {}

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    time.sleep(0.1)
    
    identifier = conn.recv(1024).decode('utf-8')
    clients[identifier] = conn
    # clients[identifier] = addr

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')  
            # print(f"Received message from {identifier}: {message}")

            response = "Received message from: " + identifier
            if identifier == 'Robot0_0':
                send_message('0.03', identifier, conn)
                
            if identifier == 'Robot1_0':
                send_message('0.09', identifier, conn)
                
            
        
        except ConnectionResetError:
            # print(f"Connection reset by client {identifier}")
            break

    # print(f"Connection closed with {identifier}")
    del clients[identifier]
    conn.close()
    
def send_message(message, identifier, conn):
    target_conn = clients.get(identifier)
    # print(target_conn)
    if target_conn:
        target_conn.sendall(message.encode('utf-8'))
    else:
        print(f"Client {identifier} not found")
def shutdown_handler(server_socket):
    global runing
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Received shutdown signal")
            print("Server shutting down...")
            runing = False
            server_socket.shutdown(socket.SHUT_RDWR)
            break

def main():
    host = '127.0.0.1'  # Replace with the server's IP address
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")
    

    shutdown_thread = threading.Thread(target=shutdown_handler, args=(server_socket,))
    shutdown_thread.start()
    
    while runing:  

        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()  
        
    shutdown_thread.join()


if __name__ == "__main__":
    main()