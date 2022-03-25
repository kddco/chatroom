import socket, threading  # Libraries import

host = '127.0.0.1'  # LocalHost
port = 7976  # Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
server.bind((host, port))  # binding host and port to socket
server.listen(10)

clients = []
client_names = []


def broadcast(message):  # broadcast function declaration
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024)
            broadcast(message)
        except:  # removing clients

            index = clients.index(client)
            # broadcast("client name:  is disconnected".encode('ascii'))
            print("client name:" + client_names[index] + " is disconnected")
            clients.remove(client)
            client.close()
            nickname = client_names[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            client_names.remove(nickname)
            break


def main():  # accepting multiple clients
    while True:
        client, address = server.accept()

        ## client first come
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client_names.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


main()
