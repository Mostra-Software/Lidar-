import socket

host = '10.10.24.220'
port = 54000
v_desired=12

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))

print(f"connected: {host}:{port}")

while True:
    

        # Send data to the server
        client_socket.send(str(v_desired).encode('utf-8'))
        

        # Receive three values from the server
        received_data1 = client_socket.recv(1024).decode('utf-8')
       

        print(f"Received values from server: {received_data1}")