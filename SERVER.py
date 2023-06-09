import socket
PROXY_ADDRESS = "127.0.0.1"
PROXY_PORT = 8080
def handle_request(client_socket, remote_address):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect(remote_address)
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        remote_socket.sendall(data)
        data = remote_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)
    remote_socket.close()
    client_socket.close()
def start_proxy():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    server_socket.listen()
    print(f"Proxy server is listening on {PROXY_ADDRESS}:{PROXY_PORT}...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        request = client_socket.recv(1024).decode("utf-8")
        request_lines = request.split("\n")
        request_method, request_path, request_protocol = request_lines[0].split()
        remote_address = request_path.replace("http://", "").split("/")[0]
        remote_address = (remote_address, 80)
        handle_request(client_socket, remote_address)

if __name__ == "__main__":
    start_proxy()
