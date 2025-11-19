import socket
import threading

clients = []

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            broadcast(msg, client)
        except:
            break

    if client in clients:
        clients.remove(client)
    client.close()

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen()

    print("[SERVER] Hacker Chat Server Running on port 9999...")

    while True:
        client, addr = server.accept()
        print(f"[CONNECTED] {addr}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    start_server()
