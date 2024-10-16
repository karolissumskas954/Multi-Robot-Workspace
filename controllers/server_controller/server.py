import socket
import threading
import time
from move_order import data

runing = True
clients = {}

def handle_client(conn, addr):
    time.sleep(0.1)
    identifier = conn.recv(1024).decode('utf-8')
    clients[identifier] = conn
    print(f"Connected by {addr}")
    def process_data():
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                
                # message = data.decode('utf-8')  
                # response = "Received message from: " + identifier
                time.sleep(0.5)
                move_cubes(identifier)
            except BlockingIOError:
                pass
            except ConnectionResetError:
                # print(f"Connection reset by client {identifier}")
                break

        # print(f"Connection closed with {identifier}")
        del clients[identifier]
        conn.close()
    data_thread = threading.Thread(target=process_data)
    data_thread.start()
  
def move_cubes(identifier):
    for item in data:
        if item['robot'] == identifier:
            send_message(item['position'], identifier)
            print(f"Message sent to : {identifier}")
        
    # if identifier == 'Robot0_0':
    #     send_message('0.03', identifier)
    # if identifier == 'Robot0_1':
    #     send_message('0.09', identifier)
    # if identifier == 'Robot0_2':
    #     send_message('0.1', identifier)
    # if identifier == 'Robot7_7':
    #     send_message('0.1', identifier)
    # if identifier == 'Robot0_8':
    #     send_message('0.1', identifier)
 

def send_message(message, identifier):
    target_conn = clients.get(identifier)
    # print(target_conn)
    if target_conn:
        target_conn.sendall(message.encode('utf-8'))
        # print('Message sent')
    else:
        print(f"Client {identifier} not found")
def shutdown_handler(server_socket):
    global runing
    while True:
        try:
            time.sleep(0.1)
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