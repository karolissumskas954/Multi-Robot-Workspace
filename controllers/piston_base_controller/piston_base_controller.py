"""piston_base_controller controller."""
from controller import Robot
import socket

TIME_STEP = 32
VELOCITY = 0.1
DESIRED_POSITION = 0.03
REPEATER = 1
TOLERANCE = 0.001

robot = Robot()
robot_name = robot.getName()
piston_linear_motor = robot.getDevice('piston_top1')
piston_linear_motor.setPosition(0)
piston_linear_motor.setVelocity(0.0)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

i = 0
def listen_to_server():   
    try: 
        response = client_socket.recv(1024)
    except socket.timeout:
        return 0
    if response:
        print(f"{robot_name}: response from server: {response.decode('utf-8')}")
        return float(response.decode('utf-8'))
    return 0
        
while robot.step(TIME_STEP) != -1:
    if i == 0:
        message = "Hello from the " + robot_name
        client_socket.sendall(robot_name.encode('utf-8'))
        client_socket.sendall(message.encode('utf-8'))
        i = 10
        
    client_socket.settimeout(0.1)
    desired_position = listen_to_server()

    if desired_position != 0:
        piston_linear_motor.setVelocity(VELOCITY)
        piston_linear_motor.setPosition(desired_position)
    
client_socket.close()
    
